#!/usr/bin/env python3
import argparse
import logging as log
import sys
from pathlib import Path

import detect_english as de
import transposition as tr


def main():
    log.basicConfig(level=log.INFO)
    parser = argparse.ArgumentParser(description="Transposition Cipher Cracker")
    parser.add_argument("-f", "--file", type=str)

    args = parser.parse_args()

    words_file = de.get_words_file_path()
    data = de.load_data(words_file)

    encrypted_file_path = args.file
    encrypted_file = Path(encrypted_file_path).resolve()
    if encrypted_file.exists():
        with encrypted_file.open() as fo:
            message = fo.read()
    else:
        print(f"Unable to find {encrypted_file_path}")
        sys.exit(1)

    clear_text = hack_message(message, data)
    if clear_text is None:
        print(f"Failed to hack {encrypted_file_path}")
    else:
        print(f"Hacked Message: {clear_text[:100]}")


def hack_message(message, data):
    log.info("Hacking")

    for key in range(1, len(message)):
        log.debug(f"Trying key: {key}")
        decrypted_text = tr.decrypt_message(key, message)
        if de.is_english(decrypted_text, data, word_percentage=50):
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
