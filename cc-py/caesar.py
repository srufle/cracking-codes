#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser(description="Caesar Cipher")
parser.add_argument("-m", "--message", type=str)
parser.add_argument("-e", "--mode", type=str, choices=["enc", "dec"], default="enc")
parser.add_argument("-o", "--offset", type=int, default=3)

args = parser.parse_args()

SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!?."

message = args.message
symbols_len = len(SYMBOLS)
offset = args.offset
mode = args.mode
if message is None:
    message = ""
    for line in sys.stdin:
        message += line.rstrip()

result = []
for symbol in message:
    if symbol in SYMBOLS:
        symbol_index = SYMBOLS.find(symbol)
        if mode == "enc":
            translated_index = symbol_index + offset
        elif mode == "dec":
            translated_index = symbol_index - offset

        if translated_index >= symbols_len:
            translated_index = translated_index - symbols_len
        elif translated_index < 0:
            translated_index = translated_index + symbols_len
        result += SYMBOLS[translated_index]
    else:
        result += symbol

print("Message:")
print(f"{offset}:{''.join(result)}")
