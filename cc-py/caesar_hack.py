#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser(description="Caesar Cipher Cracker")
parser.add_argument("-m", "--message", type=str)

args = parser.parse_args()

SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!?."

message = args.message
symbols_len = len(SYMBOLS)
if message is None:
    message = ""
    for line in sys.stdin:
        message += line.rstrip()

for key in range(symbols_len):
    result = []
    for symbol in message:
        if symbol in SYMBOLS:
            symbol_index = SYMBOLS.find(symbol)
            translated_index = symbol_index - key

            if translated_index < 0:
                translated_index = translated_index + symbols_len

            result += SYMBOLS[translated_index]
        else:
            result += symbol
    print("Message:")
    print(f"{key}:{''.join(result)}")
