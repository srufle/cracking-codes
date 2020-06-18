#!/usr/bin/env python3
import argparse
import datetime
import os
import random as r
import sys
import time

import crypto_math as cm
import detect_english as de


def main():
    parser = argparse.ArgumentParser(description="Affine Cipher")
    parser.add_argument("-m", "--message", type=str)
    # parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-e", "--mode", type=str, choices=["enc", "dec"], default="enc")
    parser.add_argument("-k", "--key", type=int, default=2894)
    parser.add_argument("-g", "--gen-key", dest="gen_key", type=bool, default=False)

    args = parser.parse_args()
    message = args.message
    file_to_use = None  # args.file
    key = args.key
    mode = args.mode
    gen_key = args.gen_key
    data = de.load_data()

    if gen_key:
        key = get_random_key(data)
        print(f"Generated Key: {key}")
        return 0

    if file_to_use is None:
        if message is None:
            message = ""
            for line in sys.stdin:
                message += line.rstrip()
    else:
        if not os.path.exists(file_to_use):
            print(f"'{file_to_use}' does not exist'")
            sys.exit(1)

        with open(file_to_use) as fo:
            message = fo.read()

    start_time = time.time()
    if mode == "enc":
        mode_name = "Encrypting"
        translated_text = encrypt_message(key, message, data)
        if file_to_use is None:
            print(f"Key:{key}")
            print(f"{mode_name}")
            print(f"Cipher:{translated_text}|")
    elif mode == "dec":
        mode_name = "Decrypting"
        translated_text = decrypt_message(key, message, data)
        if file_to_use is None:
            print(f"Key:{key}")
            print(f"{mode_name}")
            print(f"Clear Text:{translated_text}|")

    total_time = round(time.time() - start_time, 2)
    print(
        f"Completed {mode_name} ({len(message)}) chars in: {datetime.timedelta(seconds=total_time)}"
    )


def get_key_parts(key, data):
    key_a = key // len(data["SYMBOLS"])
    key_b = key % len(data["SYMBOLS"])
    return (key_a, key_b)


def check_keys(key_a, key_b, mode, data):
    symbol_length = len(data["SYMBOLS"])
    if key_a == 1 and mode == "enc":
        sys.exit("Cipher is weak if Key A is 1. Choose a different key.")
    if key_b == 0 and mode == "enc":
        sys.exit("Cipher is weak if Key B is 0. Choose a different key.")
    if key_a < 0 or key_b < 0 or key_b > symbol_length - 1:
        sys.exit(
            f"Key A must be greater then 0 and Key B must be between 0 and {symbol_length}."
        )
    if cm.gcd(key_a, symbol_length) != 1:
        err = f"Key A ({key_a}) and symbol set size ({symbol_length}) are not relatively prime.  Choose a different key."
        sys.exit(err)


def encrypt_message(key, message, data):
    key_a, key_b = get_key_parts(key, data)
    check_keys(key_a, key_b, "enc", data)

    cipher_text = ""
    symbols_data = data["SYMBOLS"]
    for symbol in message:
        if symbol in symbols_data:
            symbol_index = symbols_data.find(symbol)
            new_index = (symbol_index * key_a + key_b) % len(symbols_data)
            cipher_text += symbols_data[new_index]
        else:
            cipher_text += symbol

    return cipher_text


def decrypt_message(key, message, data):
    key_a, key_b = get_key_parts(key, data)
    check_keys(key_a, key_b, "dec", data)
    clear_text = ""
    symbols_data = data["SYMBOLS"]
    mod_inverse_of_key_a = cm.find_mod_inverse(key_a, len(symbols_data))
    for symbol in message:
        if symbol in symbols_data:
            symbol_index = symbols_data.find(symbol)
            new_index = (
                (symbol_index - key_b) * mod_inverse_of_key_a % len(symbols_data)
            )
            clear_text += symbols_data[new_index]
        else:
            clear_text += symbol

    return clear_text


def get_random_key(data):
    symbols_data = data["SYMBOLS"]
    symbols_len = len(symbols_data)
    while True:
        key_a = r.randint(2, symbols_len)
        key_b = r.randint(2, symbols_len)
        if cm.gcd(key_a, symbols_len) == 1:
            return key_a * symbols_len + key_b


if __name__ == "__main__":
    main()
