#!/usr/bin/env python3
import sys
import argparse
import random as r
import logging as log
import time, os, datetime
import crypto_math as cm
import affine as af
import detect_english as de


def main():
    log.basicConfig(level=log.INFO)

    parser = argparse.ArgumentParser(description="Affine Cipher Cracker")
    parser.add_argument("-m", "--message", type=str)

    args = parser.parse_args()
    message = args.message
    file_to_use = None  # args.file

    words_file = de.get_words_file_path()
    data = de.load_data(words_file)

    if file_to_use == None:
        if message == None:
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

    translated_text = hack_message(message, data)
    if translated_text != None:
        print(f"Message: {translated_text}|")
    else:
        print("Failed to decrypt message")

    total_time = round(time.time() - start_time, 2)
    print(
        f"Completed cracking ({len(message)}) chars in: {datetime.timedelta(seconds=total_time)}"
    )


def hack_message(message, data):
    SYMBOLS = data["SYMBOLS"]
    symbols_len = len(SYMBOLS)
    for key in range(symbols_len ** 2):
        key_a = af.get_key_parts(key, data)[0]
        if cm.gcd(key_a, symbols_len) != 1:
            continue

        decrypted_text = af.decrypt_message(key, message, data)
        log.debug(f"Tried key: {key}, {decrypted_text[:40]}")

        if de.is_english(
            decrypted_text, data, word_percentage=90, letter_percentage=90
        ):
            print()
            print(f"Key:{key}, {decrypted_text[:25]}")
            print()
            print("Enter D if done, anything else will continue hacking:")
            response = input(">")

            if response.strip().upper().startswith("D"):
                return decrypted_text

    return None


if __name__ == "__main__":
    main()
