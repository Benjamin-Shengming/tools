#!/usr/bin/env python3

import socket
import argparse
import time
import ssl
import json

BLOCK_SIZE = 4096

def create_ssl_context():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context


def send_json_request(sock, bytes_requested):
    """
    Send a JSON request over the socket.
    """
    # send request to server sock
    request = (
        json.dumps(
            {
                "number_of_bytes": bytes_requested,
            }
        )
        + "\n"
    ).encode()
    sock.send(request)

    # Receive the response header from entropy-broker
    expected_response_header = '''{"random_bytes_b64":"'''
    response_header = sock.recv(len(expected_response_header))
    print(f"Received response header: {response_header.decode()}")
    assert response_header.decode() == expected_response_header

    # Find expected length of b64 string in response
    num_expected_characters = int((bytes_requested * 4 / 3) + 3) & ~3
    # Receive encoded bytes
    b64_data = ""
    while len(b64_data) < num_expected_characters:
        bytes_required = num_expected_characters - len(b64_data)
        byte_request = min(BLOCK_SIZE, bytes_required)
        chunk = sock.recv(byte_request)
        print(f"Received {len(b64_data)} bytes")
        chunk_len = len(chunk)
        assert chunk_len != 0
        b64_data += chunk.decode()

    assert (
        len(b64_data) == num_expected_characters
    ), f"Expected {num_expected_characters} characters, but got {len(b64_data)} characters"


def send_raw_request(sock, bytes_requested):
    read_bytes = 0
    while read_bytes < bytes_requested:
        to_read = min(bytes_requested - read_bytes, BLOCK_SIZE)
        data = sock.recv(to_read)
        if not data:
            print("Connection closed by peer.")
            break
        read_bytes += len(data)
        print(f"Read {len(data)} bytes")
    assert (
        read_bytes == bytes_requested
    ), f"Expected {bytes_requested} bytes, but read {read_bytes} bytes"


def main():
    parser = argparse.ArgumentParser(description="Connect to a port and read data.")
    parser.add_argument("--ip", default="127.0.0.1", help="IP address to connect to")
    parser.add_argument(
        "--port", default=10001, type=int, help="Port number to connect to"
    )
    parser.add_argument(
        "--size", default=125 * 1024 * 1024, type=int, help="bytes to read"
    )
    parser.add_argument(
        "--tls", default=False, action="store_true", help="Use TLS connection"
    )
    parser.add_argument(
        "--json", default=False, action="store_true", help="Use json to send request "
    )
    args = parser.parse_args()

    # measure the time to connect and read data
    print(f"Connecting to {args.ip}:{args.port} with get size {args.size}")
    start_time = time.time()
    with socket.create_connection((args.ip, args.port)) as sock:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        if args.tls:
            print("Using TLS connection")
            ssl_context = create_ssl_context()
            sock = ssl_context.wrap_socket(sock, server_hostname=args.ip)
        print(f"Connected to {args.ip}:{args.port}")

        if args.json:
            send_json_request(sock, args.size)
        else:
            print("Using raw request")
            send_raw_request(sock, args.size)

    end_time = time.time()
    print(f"data read {args.size/(1024*1024)} MB")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"rate: {args.size / (end_time - start_time) / (1024 * 1024):.2f} MB/s")


if __name__ == "__main__":
    main()
