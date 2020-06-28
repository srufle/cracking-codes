#!/usr/bin/env python3
import argparse
import datetime
import os
import logging as log
import random as r
import sys
import time
import vigenere as v
import freq_analysis as fa

import detect_english as de


def main():
    parser = argparse.ArgumentParser(description="Vigenere Cipher Hack")
    parser.add_argument("-m", "--message", type=str)
    # parser.add_argument("-f", "--file", type=str)

    args = parser.parse_args()
    message = args.message
    file_to_use = None  # args.file

    words_file = de.get_words_file_path("content/dictionary.txt")
    data = de.load_data(words_file)

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
    hacked_messages = hack_vigenere_dict(message, data)
    if len(hacked_messages) == 0:
        total_time = round(time.time() - start_time, 2)
        print(f"Completed in: {datetime.timedelta(seconds=total_time)}")
        for word in hacked_messages.keys():
            print(f"{word}: {hacked_messages[word]}")
    else:
        print("Failed to decrypt")


def hack_vigenere_dict(message, data):
    possible_decrypted_texts = {}
    WORDS = data["WORDS"]
    for word in WORDS.keys():
        word = word.strip().upper()
        if len(word) > 0:
            decrypted_text = v.decrypt_message(word, message, data)
            if de.is_english(decrypted_text, data, word_percentage=40):
                possible_decrypted_texts[word] = decrypted_text
    return possible_decrypted_texts


if __name__ == "__main__":
    main()
