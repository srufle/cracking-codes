#!/usr/bin/env python3
import sys
import math
import random
import transposition
import pytest


def test_trans_all():
    random.seed(42)

    for i in range(20):
        message = (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!? \n."
            * random.randint(4, 40)
        )
        message = list(message)
        random.shuffle(message)
        message = "".join(message)

        print(f"Test {i+1}: {message[:50]}")
        for key in range(1, int(len(message) / 2)):
            encrypted = transposition.encrypt_message(key, message)
            decrypted = transposition.decrypt_message(key, encrypted)

            if message != decrypted:
                print(f"Mismatch with {key} and message {message}")
                print(f"Decrypted as: {decrypted}")
                sys.exit()
