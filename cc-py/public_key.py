#!/usr/bin/env python3
import argparse
import datetime
import os
import random as r
import sys
import math
import time

import crypto_math as cm
import detect_english as de

SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."


def main():
    parser = argparse.ArgumentParser(description="Public Key Cipher")
    parser.add_argument("-m", "--message", type=str)
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-n", "--name", dest="name", type=str, default="nobody")
    parser.add_argument("-e", "--mode", type=str, choices=["enc", "dec"], default="enc")

    args = parser.parse_args()
    message = args.message
    name = args.name
    file_to_use = args.file
    mode = args.mode

    if message is None:
        message = ""
        for line in sys.stdin:
            message += line.rstrip()

    start_time = time.time()
    if mode == "enc":
        mode_name = "Encrypting"
        key_filename = f"pubkey_{name}.pub"
        message_filename = f"{name}_message.enc"
        encrypted_text = encrypt_and_write_file(message_filename, key_filename, message)
        print("Encrypted text:")
        print(encrypted_text)
    elif mode == "dec":
        mode_name = "Decrypting"
        key_filename = f"privkey_{name}.priv"
        message_filename = f"{name}_message.enc"
        decrypted_text = read_from_file_and_decrypt(message_filename, key_filename)
        print("Decrypted text:")
        print(decrypted_text)

    total_time = round(time.time() - start_time, 2)
    print(
        f"Completed {mode_name} ({len(message)}) chars in: {datetime.timedelta(seconds=total_time)}"
    )


def get_blocks_from_text(message, block_size):

    for character in message:
        if character not in SYMBOLS:
            print(f"ERROR: The symbol set does not have the character '{character}'")
            sys.exit(1)

    block_ints = []
    message_len = len(message)
    symbols_len = len(SYMBOLS)

    for block_start in range(0, message_len, block_size):
        block_int = 0
        for i in range(block_start, min(block_start + block_size, message_len)):
            block_int += (SYMBOLS.index(message[i])) * (symbols_len ** (i % block_size))

        block_ints.append(block_int)
    return block_ints


def get_text_from_blocks(block_ints, message_length, block_size):
    message = []
    symbols_len = len(SYMBOLS)
    for block_int in block_ints:
        block_message = []
        for i in range(block_size - 1, -1, -1):
            if len(message) + i < message_length:
                char_index = block_int // (symbols_len ** i)
                block_int = block_int % (symbols_len ** i)
                block_message.insert(0, SYMBOLS[char_index])
        message.extend(block_message)
    return "".join(message)


def encrypt_message(message, key, block_size):
    encrypted_blocks = []
    n, e = key
    for block in get_blocks_from_text(message, block_size):
        encrypted_blocks.append(pow(block, e, n))
    return encrypted_blocks


def decrypt_message(encrypted_blocks, message_length, key, block_size):
    decrypted_blocks = []
    n, d = key
    for block in encrypted_blocks:
        decrypted_blocks.append(pow(block, d, n))
    return get_text_from_blocks(decrypted_blocks, message_length, block_size)


def read_key_file(key_filename):
    with open(key_filename) as fo:
        content = fo.read()

    key_size, n, e_or_d = content.split(",")
    return (int(key_size), int(n), int(e_or_d))


def encrypt_and_write_file(message_filename, key_filename, message, block_size=None):

    key_size, n, e = read_key_file(key_filename)
    key = (n, e)
    if block_size == None:
        block_size = int(math.log(2 ** key_size, len(SYMBOLS)))

    if int(math.log(2 ** key_size, len(SYMBOLS))) < block_size:
        sys.exit(
            "ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?"
        )

    encypted_blocks = encrypt_message(message, key, block_size)

    for i in range(len(encypted_blocks)):
        encypted_blocks[i] = str(encypted_blocks[i])

    encypted_conetnt = ",".join(encypted_blocks)

    encypted_conetnt = f"{len(message)}_{block_size}_{encypted_conetnt}"
    with open(message_filename, "w") as fo:
        fo.write(encypted_conetnt)

    return encypted_conetnt


def read_from_file_and_decrypt(message_filename, key_filename):
    key_size, n, d = read_key_file(key_filename)
    key = (n, d)
    with open(message_filename) as fo:
        content = fo.read()

    message_length, block_size, encrypted_message = content.split("_")
    message_length = int(message_length)
    block_size = int(block_size)

    if int(math.log(2 ** key_size, len(SYMBOLS))) < block_size:
        sys.exit(
            "ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?"
        )

    encrypted_blocks = []
    for block in encrypted_message.split(","):
        encrypted_blocks.append(int(block))

    return decrypt_message(encrypted_blocks, message_length, key, block_size)


if __name__ == "__main__":
    main()
