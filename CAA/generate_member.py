#!/usr/bin/env python3
import argparse
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
from datetime import datetime
from loguru import logger
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

#don't  change the key
AES_KEY=b"1234567890abcdef1234567890abccaa"
nonce = b"\x05" * 12

def encrypt_chacha20(data: str, key: bytes) -> str:
    chacha = ChaCha20Poly1305(key)
    encrypted_data = chacha.encrypt(nonce, data.encode(), None)
    return urlsafe_b64encode(encrypted_data).decode()

def decrypt_chacha20(token: str, key: bytes) -> str:
    encrypted_data = urlsafe_b64decode(token.encode())
    chacha = ChaCha20Poly1305(key)
    decrypted_data = chacha.decrypt(nonce, encrypted_data, None)
    return decrypted_data.decode()

def get_card_type_str(card_type):
    if card_type == "Family": 
       return "家庭会员卡"
    else:
        return "个人会员卡"

def get_card_type_enc_str(card_type):
    if card_type == "Family": 
       return "F"
    else:
        return "S"
    
def generate_member_card(template_path, output_path, 
                         card_no, issue_date, name, chinese_name, valid_till, issued_by, card_type):
    # Load the blank template
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    
    # Load a font (modify path as needed)
      # Load a font that supports Chinese characters (modify path as needed)
    font_path = "./Noto_Sans_SC/static/NotoSansSC-Bold.ttf"
    font_size = 28
    font = ImageFont.truetype(font_path, font_size)

    
    # Define text positions (adjust as needed)
    positions = {
        "card_no": (350, 320),  "issue_date": (880, 320),
        "name": (300, 385), "chinese_name": (750, 385),
        "valid_till": (200, 455), "issued_by": (750, 455),
    }
    
    # Insert text
    draw.text(positions["card_no"], card_no, fill="black", font=font)
    draw.text(positions["issue_date"], issue_date, fill="black", font=font)
    draw.text(positions["name"], name, fill="black", font=font)
    draw.text(positions["chinese_name"], chinese_name, fill="black", font=font)
    draw.text(positions["valid_till"], valid_till, fill="black", font=font)
    draw.text(positions["issued_by"], issued_by, fill="black", font=font)
    
    qr_data = f"{card_no}:{issue_date}:{name}:{chinese_name}:{valid_till}:{issued_by}:{get_card_type_str(card_type)}"
    logger.info(f"QR Data: \n{qr_data}")

    pt = f"{card_no}:{issue_date}:{get_card_type_enc_str(card_type)}"
    encrypt_data = encrypt_chacha20(pt, AES_KEY)
    decrypted_data = decrypt_chacha20(encrypt_data, AES_KEY)

    assert decrypted_data == pt, "Encryption and Decryption failed"
    logger.info(f"encrypted: \n{encrypt_data}")

    qr = qrcode.make(qr_data)
    qr = qr.resize((200, 200))  # Resize as needed
    image.paste(qr, (360, 510))  # Adjust position

    draw.text((700, 550), get_card_type_str(card_type), fill="black", font=font)
    draw.text((100, 700), encrypt_data, fill="black", font=font)

    
    # Save the output image
    image.save(output_path)
    print(f"Member card saved as {output_path}")

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a filled membership card.")
    parser.add_argument("--template", default="./empty_member_card.jpg", help="Path to the blank member card template")
    parser.add_argument("--output", default=None , help="Path to save the generated member card")
    parser.add_argument("--card_no", default="1234", help="Membership card number")

    default_issue_date = datetime.today().strftime("%Y-%m-%d")
    parser.add_argument("--issue_date", default=default_issue_date, help="Issue date")
    parser.add_argument("--name", default="Jack", help="Member name")
    parser.add_argument("--chinese_name", default="测试姓名", help="Member Chinese name")
    default_valid_till = datetime.today().strftime("%Y") + "-12-31"
    parser.add_argument("--valid_till", default=default_valid_till, help="Validity date")
    parser.add_argument("--issued_by", default="CAA", help="Issuer name")
    parser.add_argument("--card_type", default="Single", help="Card type:Single or Family")
    parser.add_argument("--excel", default="./2025.xlsx", help="grap infrmation from excel")

    parser.add_argument("--verify", default=None, help="verify the card with decode")


    args = parser.parse_args()
    if args.card_type not in ["Single", "Family"]:
        raise ValueError("Card type must be 'Single' or 'Family'")


    if args.output is None: 
        c_name = args.chinese_name if args.chinese_name else args.name
        args.output = f"{args.card_no}_{c_name}.jpg"
    return args

def main():
    args = parse_args()
    if not args.verify:
        generate_member_card(
            args.template, args.output, args.card_no, args.issue_date,
            args.name, args.chinese_name, args.valid_till, args.issued_by, args.card_type)
    else:
        decrypted_data = decrypt_chacha20(args.verify, AES_KEY)
        logger.info(f"Decrypted data: {decrypted_data}")

if __name__ == "__main__":
    main()

