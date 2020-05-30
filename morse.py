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


for line in sys.stdin:
    chars = line.rstrip()
    for c in chars:
        upper_char = c.upper()
        if not (upper_char in encoding_lookup.keys()):
            upper_char = "0"
        morse_char = encoding_lookup[upper_char]
        print(f"{upper_char} = {morse_char}")
