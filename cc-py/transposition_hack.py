#!/usr/bin/env python3
import sys
import argparse
import math


def main():
    parser = argparse.ArgumentParser(description="Transposition Cipher Cracker")
    parser.add_argument("-m", "--message", type=str)
    parser.add_argument("-k", "--key", type=int, default=8)

    args = parser.parse_args()
    message = args.message
    key = args.key
    if message == None:
        message = ""
        for line in sys.stdin:
            message += line.rstrip()

    clear_text = decrypt_message(key, message)
    print(f"Cipher:{clear_text}|")


def decrypt_message(key, message):
    num_of_columns = int(math.ceil(len(message) / float(key)))
    num_of_rows = key
    num_of_shaded_boxes = (num_of_columns * num_of_rows) - len(message)

    clear_text = [""] * num_of_columns
    column = 0
    row = 0

    # Loop through each column if cipher text
    for symbol in message:
        clear_text[column] += symbol
        column += 1
        no_more_columns = column == num_of_columns
        at_shaded_box = (
            column == num_of_columns - 1 and row >= num_of_rows - num_of_shaded_boxes
        )
        if no_more_columns or at_shaded_box:
            column = 0
            row += 1

    return "".join(clear_text)


if __name__ == "__main__":
    main()
