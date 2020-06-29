#!/usr/bin/env python3
import argparse
import datetime
import os
import logging as log

import re
import itertools
import sys
import time
import vigenere as v
import freq_analysis as fa

import detect_english as de

MAX_KEY_LENGTH = 16
NUM_MOST_FREQ_LETTERS = 4
SILENT_MODE = True
NONLETTERS_PATTERN = re.compile("[^A-Z]")


def main():
    parser = argparse.ArgumentParser(description="Vigenere Cipher Hack")
    parser.add_argument("-m", "--message", type=str)
    parser.add_argument(
        "-t", "--type", type=str, choices=["dict", "kski"], default="dict"
    )
    # parser.add_argument("-f", "--file", type=str)

    args = parser.parse_args()
    message = args.message
    hack_type = args.type
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
    if hack_type == "dict":
        hacked_messages = hack_vigenere_dict(message, data)
        if len(hacked_messages) == 0:
            total_time = round(time.time() - start_time, 2)
            print(f"Completed in: {datetime.timedelta(seconds=total_time)}")
            for word in hacked_messages.keys():
                print(f"{word}: {hacked_messages[word]}")
        else:
            print("Failed to decrypt")
    elif hack_type == "kski":
        _is_done, hacked_messages = hack_vigenere_kasiski(message, data)
        if len(hacked_messages) == 0:
            total_time = round(time.time() - start_time, 2)
            print(f"Completed in: {datetime.timedelta(seconds=total_time)}")
            for word in hacked_messages.keys():
                print(f"{word}: {hacked_messages[word]}")
        else:
            print("Failed to decrypt")
    else:
        print("Hack type unknown")


def find_repeat_sequences_spacings(message):
    # Goes through the message and finds any 3- to 5-letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).

    message = NONLETTERS_PATTERN.sub("", message.upper())
    message_len = len(message)

    seq_spacings = {}
    for seq_len in range(3, 6):
        for seq_start in range(message_len - seq_len):
            seq = message[seq_start : seq_start + seq_len]

            for i in range(seq_start + seq_len, message_len - seq_len):
                if message[i : i + seq_len] == seq:
                    if seq not in seq_spacings:
                        seq_spacings[seq] = []

                    seq_spacings[seq].append(i - seq_start)

    return seq_spacings


def get_useful_factors(num):
    # Returns a list of useful factors of num. By "useful" we mean factors
    # less than MAX_KEY_LENGTH + 1 and not 1. For example,
    # getUsefulFactors(144) returns [2, 3, 4, 6, 8, 9, 12, 16].

    if num < 2:
        return []

    factors = []
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            other_factor = int(num / i)
            if other_factor < MAX_KEY_LENGTH + 1 and other_factor != 1:
                factors.append(other_factor)

    return list(set(factors))


def get_item_at_index_one(x):
    return x[1]


def get_most_common_factors(seq_factors):
    factor_counts = {}

    for seq in seq_factors:
        factor_list = seq_factors[seq]
        for factor in factor_list:
            if factor not in factor_counts:
                factor_counts[factor] = 0

            factor_counts[factor] += 1

    factors_by_count = []

    for factor in factor_counts:
        if factor <= MAX_KEY_LENGTH:
            factors_by_count.append((factor, factor_counts[factor]))

    factors_by_count.sort(key=get_item_at_index_one, reverse=True)

    return factors_by_count


def kasiski_examination(message):
    repeated_seq_spacings = find_repeat_sequences_spacings(message)

    seq_factors = {}
    for seq in repeated_seq_spacings:
        seq_factors[seq] = []
        for spacing in repeated_seq_spacings[seq]:
            seq_factors[seq].extend(get_useful_factors(spacing))

    factors_by_count = get_most_common_factors(seq_factors)

    all_likely_lengths = []
    for two_int_tuple in factors_by_count:
        all_likely_lengths.append(two_int_tuple[0])

    return all_likely_lengths


def get_nth_subkeys_letters(nth, key_length, message):
    # Returns every nth letter for each key_length set of letters in text.
    # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'

    message = NONLETTERS_PATTERN.sub("", message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += key_length

    return "".join(letters)


def attempt_hack_with_key_length(message, likely_key_length, data):
    possible_decrypted_texts = {}
    message_upper = message.upper()

    all_freq_scores = []
    for nth in range(1, likely_key_length + 1):
        nth_letters = get_nth_subkeys_letters(nth, likely_key_length, message_upper)

        freq_scores = []
        LETTERS = data["LETTERS"]
        for possible_key in LETTERS:
            decrypted_text = v.decrypt_message(possible_key, nth_letters, data)
            key_and_freq_match_tuple = (
                possible_key,
                fa.english_freq_match(decrypted_text, data),
            )
            freq_scores.append(key_and_freq_match_tuple)

        freq_scores.sort(key=get_item_at_index_one, reverse=True)

        all_freq_scores.append(freq_scores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(all_freq_scores)):
            # Use i + 1 so the first letter is not called the "0th" letter:
            print(f"Possible letters for letter {i+1} of the key: ", end="")
            for freq_score in all_freq_scores[i]:
                print(f"{freq_score[0]} ", end="")
            print()  # Print a newline.

    for indexes in itertools.product(
        range(NUM_MOST_FREQ_LETTERS), repeat=likely_key_length
    ):
        possible_key = ""
        for i in range(likely_key_length):
            log.debug(f"i={i}, indexes[{i}]={indexes[i]}, {all_freq_scores}")
            possible_key += all_freq_scores[i][indexes[i]][0]

        if not SILENT_MODE:
            print(f"Attempting with key: ({possible_key})")
        decrypted_text = v.decrypt_message(possible_key, message_upper, data)

        if de.is_english(decrypted_text, data):
            orig_case = []
            for i in range(len(message)):
                if message[i].isupper():
                    orig_case.append(decrypted_text[i].upper())
                else:
                    orig_case.append(decrypted_text[i].lower())

            decrypted_text = "".join(orig_case)
            possible_decrypted_texts[possible_key] = decrypted_text
            print("Possible encryption hack with key %s:" % (possible_key))
            print(decrypted_text[:200])  # Only show first 200 characters.
            print()
            print("Enter D if done, anything else to continue hacking:")
            response = input("> ")
            if response.strip().upper().startswith("D"):
                return (True, possible_decrypted_texts)
    return (False, {})


def hack_vigenere_kasiski(message, data):
    is_done = False
    possible_decrypted_texts = {}
    likely_key_lengths = kasiski_examination(message)
    if not SILENT_MODE:
        key_length_str = ""
        for key_length in likely_key_lengths:
            key_length_str += "%s " % (key_length)
        print(
            f"Kasiski examination results say the most likely key lengths are: {key_length_str}"
        )

    for likely_key_length in likely_key_lengths:
        if not SILENT_MODE:
            print(
                f"Attempting hack with key length {likely_key_length} ({NUM_MOST_FREQ_LETTERS ** likely_key_length} possible keys)..."
            )
        is_done, possible_decrypted_texts = attempt_hack_with_key_length(
            message, likely_key_length, data
        )
        if not is_done and len(possible_decrypted_texts) == 0:
            if not SILENT_MODE:
                print(
                    "Unable to hack message with likely key length(s). Brute-forcing key length..."
                )
            for key_length in range(1, MAX_KEY_LENGTH + 1):
                if key_length not in likely_key_lengths:
                    if not SILENT_MODE:
                        print(
                            f"Attempting hack with key length {key_length} ({NUM_MOST_FREQ_LETTERS ** key_length} possible keys)..."
                        )
                    is_done, possible_decrypted_texts = attempt_hack_with_key_length(
                        message, key_length, data
                    )
                if is_done and len(possible_decrypted_texts) != 0:
                    return (is_done, possible_decrypted_texts)
        else:
            return (is_done, possible_decrypted_texts)

    return (is_done, possible_decrypted_texts)


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
