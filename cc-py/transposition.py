#!/usr/bin/env python3
import argparse
import datetime
import math
import os
import sys
import time


def main():
    parser = argparse.ArgumentParser(description="Transposition Cipher")
    parser.add_argument("-m", "--message", type=str)
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-e", "--mode", type=str, choices=["enc", "dec"], default="enc")
    parser.add_argument("-k", "--key", type=int, default=8)

    args = parser.parse_args()
    message = args.message
    file_to_use = args.file
    key = args.key
    mode = args.mode

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
    if mode == "enc":
        mode_name = "Encrypting"
        out_file = gen_outfile_name(mode, file_to_use)
        translated_text = encrypt_message(key, message)
        if file_to_use is None:
            print(f"Cipher:{translated_text}|")
    elif mode == "dec":
        mode_name = "Decrypting"
        out_file = gen_outfile_name(mode, file_to_use)
        translated_text = decrypt_message(key, message)
        if file_to_use is None:
            print(f"Clear Text:{translated_text}|")

    total_time = round(time.time() - start_time, 2)
    print(
        f"Completed {mode_name} ({len(message)}) chars in: {datetime.timedelta(seconds=total_time)}"
    )

    with open(out_file, "w") as fo:
        fo.write(translated_text)


def gen_outfile_name(mode, filename):
    parts = filename.split(".")

    last_ext = "txt"
    if len(parts) > 1:
        last_ext = parts.pop()

    if mode == "enc":
        parts.append("encrypted")
    elif mode == "dec":
        parts.append("decrypted")
    else:
        parts.append(last_ext)

    out_name = f"{'.'.join(parts)}"
    return out_name


def encrypt_message(key, message):
    cipher_text = [""] * key

    # Loop through each column if cipher text
    for colmun in range(key):
        current_index = colmun
        # Keep looping until current index goes past message length
        while current_index < len(message):
            cipher_text[colmun] += message[current_index]
            current_index += key
    return "".join(cipher_text)


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
        at_shaded_box = column == (num_of_columns - 1) and row >= (
            num_of_rows - num_of_shaded_boxes
        )
        if no_more_columns or at_shaded_box:
            column = 0
            row += 1

    return "".join(clear_text)


if __name__ == "__main__":
    main()
