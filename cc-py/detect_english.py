#!/usr/bin/env python3
import sys
import argparse
import math
import time, os, datetime
import logging as log
from pathlib import Path


def load_data(words_file=None):
    UPPER_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LETTERS_AND_SPACE = UPPER_LETTERS + UPPER_LETTERS.lower() + " \t\n"
    data = {}
    data["WORDS"] = load_words(words_file)
    data["UPPER_LETTERS"] = UPPER_LETTERS
    data["LETTERS_AND_SPACE"] = LETTERS_AND_SPACE

    return data


def load_words(words_file=None):
    words = {}
    if words_file != None:

        words_file = Path(words_file).resolve()
        if words_file.exists():
            with words_file.open() as fo:
                for word in fo.read().split("\n"):
                    words[word.lower()] = None
        else:
            print(f"Unable to find {words_file}")
            sys.exit(1)

    return words


def get_english_count(message, data):
    WORDS = data["WORDS"]

    message = message.lower()
    message = remove_non_letters(message, data)
    possible_words = message.split()
    if possible_words == []:
        log.debug("No words")
        return 0.0

    matches = 0.0
    for word in possible_words:
        if word in WORDS:
            matches += 1

    return float(matches) / len(possible_words)


def remove_non_letters(message, data):
    LETTERS_AND_SPACE = data["LETTERS_AND_SPACE"]
    letters_only = []
    for symbol in message:
        if symbol in LETTERS_AND_SPACE:
            letters_only.append(symbol)
    return "".join(letters_only)


def is_english(message, data, word_percentage=20, letter_percentage=85):
    words_match = get_english_count(message, data) * 100 >= word_percentage
    num_letters = len(remove_non_letters(message, data))
    message_letter_percentage = 0.0
    message_len = len(message)
    if message_len > 0:
        message_letter_percentage = (float(num_letters) / message_len) * 100
    letters_match = message_letter_percentage >= letter_percentage
    return words_match and letters_match
