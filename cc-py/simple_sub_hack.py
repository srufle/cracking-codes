#!/usr/bin/env python3
import argparse
import logging as log
import datetime
import copy
import os
import simple_sub as ss
import re
import random as r
import sys
import time

import detect_english as de

non_letter_or_space_pattern = re.compile("[^a-z\\s]")


def main():
    parser = argparse.ArgumentParser(description="Simple Substitution Cipher Hack")
    parser.add_argument("-m", "--message", type=str)
    # parser.add_argument("-f", "--file", type=str)

    args = parser.parse_args()
    message = args.message
    file_to_use = None  # args.file

    words_file = de.get_words_file_path()
    data = de.load_data(words_file)
    data = de.make_word_patterns(data)

    start_time = time.time()
    possible_mapping = hack_possible_mapping(message, data)
    clear_text = decrypt_with_hacked_key(message, possible_mapping, data)
    if clear_text is None:
        print(f"Failed to hack {message}")
    else:
        print(f"Hacked Message: {clear_text[:100]}")

    total_time = round(time.time() - start_time, 2)
    print(
        f"Completed hack ({len(message)}) chars in: {datetime.timedelta(seconds=total_time)}"
    )


def hack_possible_mapping(message, data):
    log.info("Hacking")
    all_word_patterns = data["WORD_PATTERNS"]
    intersected_map = get_blank_cipher_letter_mapping()
    cipher_word_list = non_letter_or_space_pattern.sub("", message.lower()).split()

    for cipher_word in cipher_word_list:
        candidate_map = get_blank_cipher_letter_mapping()

        word_pattern = de.get_word_pattern(cipher_word)
        if word_pattern not in all_word_patterns:
            log.debug(f"Word: {cipher_word} NOT in our map")
            continue

        for candidate in all_word_patterns[word_pattern]:
            add_letters_to_mapping(candidate_map, cipher_word, candidate)

        intersected_map = intersect_mappings(intersected_map, candidate_map, data)

    return remove_solved_letters_from_mapping(intersected_map, data)


def add_letters_to_mapping(letter_mapping, cipher_word, candidate):
    # The letter_mapping parameter takes a dictionary value that
    # stores a cipher_letter mapping, which is copied by the function.
    # The cipher_word parameter is a string value of the ciphertext word.
    # The candidate parameter is a possible English word that the
    # cipher_word could decrypt to.

    # This function adds the letters in the candidate as potential
    # decryption letters for the cipher_letters in the cipher_letter
    # mapping.
    for i in range(len(cipher_word)):
        lmw = cipher_word[i]
        # log.debug(
        #     f"cipher_word[{i}]={lmw}, candidate[{i}]={candidate[i]}, letter_mapping[{lmw}]={letter_mapping[lmw]}"
        # )
        if candidate[i] not in letter_mapping[lmw]:
            letter_mapping[lmw].append(candidate[i])
            # log.debug(f"letter_mapping[{lmw}]={letter_mapping[lmw]}")


def intersect_mappings(mapA, mapB, data):
    intersected_map = get_blank_cipher_letter_mapping()
    LETTERS = data["LETTERS"]
    for letter in LETTERS:
        letter = letter.lower()
        if mapA[letter] == []:
            intersected_map[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersected_map[letter] = copy.deepcopy(mapA[letter])
        else:
            for mapped_letter in mapA[letter]:
                if mapped_letter in mapB[letter]:
                    intersected_map[letter].append(mapped_letter)
    return intersected_map


def remove_solved_letters_from_mapping(letter_mapping, data):
    # Cipherletters in the mapping that map to only one letter are
    # "solved" and can be removed from the other letters.
    # For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
    # maps to ['N'], then we know that 'B' must map to 'N', so we can
    # remove 'N' from the list of what 'A' could map to. So 'A' then maps
    # to ['M']. Note that now that 'A' maps to only one letter, we can
    # remove 'M' from the list of letters for every other letter.
    # (This is why there is a loop that keeps reducing the map.)
    loop_again = True
    LETTERS = data["LETTERS"]
    while loop_again:
        loop_again = False

        solved_letters = []
        for cipher_letter in LETTERS:
            cipher_letter = cipher_letter.lower()
            if len(letter_mapping[cipher_letter]) == 1:
                solved_letters.append(letter_mapping[cipher_letter][0])

        for cipher_letter in LETTERS:
            cipher_letter = cipher_letter.lower()
            for s in solved_letters:
                if (
                    len(letter_mapping[cipher_letter]) != 1
                    and s in letter_mapping[cipher_letter]
                ):
                    letter_mapping[cipher_letter].remove(s)
                    if len(letter_mapping[cipher_letter]) == 1:
                        loop_again = True
    return letter_mapping


def decrypt_with_hacked_key(cipher_text, letter_mapping, data):
    LETTERS = data["LETTERS"]
    key = ["x"] * len(LETTERS)
    log.debug(f"letter_mapping={letter_mapping}")

    for cipher_letter in LETTERS:
        cipher_letter = cipher_letter.lower()
        if len(letter_mapping[cipher_letter]) == 1:
            find_char = letter_mapping[cipher_letter][0].upper()
            key_index = LETTERS.find(find_char)
            key[key_index] = cipher_letter
            log.debug(
                f"key={key}, cipher_letter={cipher_letter}, find_char={find_char}, key_index={key_index}"
            )
        else:
            log.debug(f"cipher_text={cipher_text}, replace={cipher_letter}, with=_")
            cipher_text = cipher_text.replace(cipher_letter.lower(), "_")
            cipher_text = cipher_text.replace(cipher_letter.upper(), "_")
    key = "".join(key)
    print(f"key={key}")
    return ss.decrypt_message(key, cipher_text, data)


# Valid Quote keys:
# LxWOAYUISxxMNXPxxCRJTQExxZ - from /home/srufle/Downloads/CrackingCodesFiles/
# lxwoayuisxxmnxpxxcrjtqexxz - from our own calculation
# Full good: LFWOAYUISVKMNXPBDCRJTQEGHZ - default test key


def get_blank_cipher_letter_mapping():
    return {
        "a": [],
        "b": [],
        "c": [],
        "d": [],
        "e": [],
        "f": [],
        "g": [],
        "h": [],
        "i": [],
        "j": [],
        "k": [],
        "l": [],
        "m": [],
        "n": [],
        "o": [],
        "p": [],
        "q": [],
        "r": [],
        "s": [],
        "t": [],
        "u": [],
        "v": [],
        "w": [],
        "x": [],
        "y": [],
        "z": [],
    }


if __name__ == "__main__":
    main()
