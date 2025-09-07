#include "encdec_demo.h"
#include <iostream>
#include <string>
#include <vector>
#include "../../lib/enc_dec/encode_decode.hpp"

EncodeDemoCmdApp::EncodeDemoCmdApp() : CLI::App("Show encode usage demo", "encode-demo") {
    this->callback([this]() { this->run(); });
}

void EncodeDemoCmdApp::run() {
    std::string input = "hello world";
    std::cout << "Input: " << input << std::endl;

    std::string encoded2 = encdec::EncodeBase2(input);
    std::cout << "Base2 Encoded:  " << encoded2 << std::endl;

    std::string encoded4 = encdec::EncodeBase4(input);
    std::cout << "Base4 Encoded:  " << encoded4 << std::endl;

    std::string encoded8 = encdec::EncodeBase8(input);
    std::cout << "Base8 Encoded:  " << encoded8 << std::endl;

    std::string encoded16 = encdec::EncodeBase16(input);
    std::cout << "Base16 Encoded: " << encoded16 << std::endl;

    std::string encoded32 = encdec::EncodeBase32(input);
    std::cout << "Base32 Encoded: " << encoded32 << std::endl;

    std::string encoded64 = encdec::EncodeBase64(input);
    std::cout << "Base64 Encoded: " << encoded64 << std::endl;
}

DecodeDemoCmdApp::DecodeDemoCmdApp() : CLI::App("Show decode usage demo", "decode-demo") {
    this->callback([this]() { this->run(); });
}

void DecodeDemoCmdApp::run() {
    std::string input = "hello world";
    std::string encoded2 = encdec::EncodeBase2(input);
    std::string encoded4 = encdec::EncodeBase4(input);
    std::string encoded8 = encdec::EncodeBase8(input);
    std::string encoded16 = encdec::EncodeBase16(input);
    std::string encoded32 = encdec::EncodeBase32(input);
    std::string encoded64 = encdec::EncodeBase64(input);

    std::cout << "Base2 Decoded:  " << encdec::DecodeBase2(encoded2) << std::endl;
    std::cout << "Base4 Decoded:  " << encdec::DecodeBase4(encoded4) << std::endl;
    std::cout << "Base8 Decoded:  " << encdec::DecodeBase8(encoded8) << std::endl;
    std::cout << "Base16 Decoded: " << encdec::DecodeBase16(encoded16) << std::endl;
    std::cout << "Base32 Decoded: " << encdec::DecodeBase32(encoded32) << std::endl;
    std::cout << "Base64 Decoded: " << encdec::DecodeBase64(encoded64) << std::endl;
}
