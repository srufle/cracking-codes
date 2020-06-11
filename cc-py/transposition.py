#!/usr/bin/env python3
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Transposition Cipher")
    parser.add_argument("-m", "--message", type=str)
    parser.add_argument("-k", "--key", type=int, default=8)

    args = parser.parse_args()
    message = args.message
    key = args.key
    if message == None:
        message = ""
        for line in sys.stdin:
            message += line.rstrip()

    cipher_text = encrypt_message(key, message)
    print(f"Cipher:{cipher_text}|")


def encrypt_message(key, message):
    cipher_text = [""] * key

    # Loop through each column if cipher text
    for colmun in range(key):
        current_index = colmun
        # Keep looping until current index goes past message length
        while current_index < len(message):
            cipher_text[colmun] += message[current_index]
            current_index += key
    return "".join(cipher_text)


if __name__ == "__main__":
    main()
