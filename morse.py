#!/usr/bin/env python3

import sys
encoding_lookup = {
    "A": "*-",
    "B": "-***",
    "C": "-*-*",
    "D": "-**",
    "E": "*",
    "F": "**-*",
    "G": "--*",
    "H": "****",
    "I": "**",
    "J": "*---",
    "K": "-*-",
    "L": "*-**",
    "M": "--",
    "N": "-*",
    "O": "---",
    "P": "*--*",
    "Q": "--*-",
    "R": "*-*",
    "S": "***",
    "T": "-",
    "U": "**-",
    "V": "***-",
    "W": "*--",
    "X": "-**-",
    "Y": "-*---",
    "Z": "--**",
    "1": "*----",
    "2": "**---",
    "3": "***--",
    "4": "****-",
    "5": "*****",
    "6": "-****",
    "7": "--***",
    "8": "---**",
    "9": "----*",
    "0": "-----",
}


def encode(char):
    upper_char = char.upper()
    if not (upper_char in encoding_lookup.keys()):
        upper_char = "0"
    encoded_char = encoding_lookup[upper_char]
    return (upper_char, encoded_char)


for line in sys.stdin:
    chars = line.rstrip()
    for char in chars:
        encoded = encode(char)
        print(f"{encoded[0]} = {encoded[1]}")
