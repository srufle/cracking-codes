#!/usr/bin/env python3
import argparse
import datetime
import os
import logging as log
import random as r
import sys
import time

import detect_english as de


def main():
    parser = argparse.ArgumentParser(description="Vigenere Cipher")
    parser.add_argument("-m", "--message", type=str)
    # parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-e", "--mode", type=str, choices=["enc", "dec"], default="enc")
    parser.add_argument("-k", "--key", type=str, default="ASIMOV")
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
    if not is_key_valid(key, data):
        sys.exit("There is an error in the key or symbol set.")
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


def encrypt_message(key, message, data):
    return translate_message(key, message, data, "enc")


def decrypt_message(key, message, data):
    return translate_message(key, message, data, "dec")


def translate_message(key, message, data, mode):
    translated = []
    key_index = 0
    key = key.upper()
    LETTERS = data["LETTERS"]

    for symbol in message:
        num = LETTERS.find(symbol.upper())
        if num != -1:
            key_letter = key[key_index]
            # print(f" {key}[{key_index}] = {key_letter}")
            if mode == "enc":
                num += LETTERS.find(key_letter)
            elif mode == "dec":
                num -= LETTERS.find(key_letter)
            num %= len(LETTERS)

            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            key_index += 1
            if key_index == len(key):
                key_index = 0

        else:
            translated.append(symbol)

    return "".join(translated)


def get_random_key(data, length=14):
    key = list(data["LETTERS"])
    r.shuffle(key)
    return "".join(key)[:length]


if __name__ == "__main__":
    main()
