#!/usr/bin/env python3
import logging as log
import random as r
import sys

import pytest

import affine as af
import crypto_math as cm
import detect_english as de

log.basicConfig(level=log.INFO)


def test_get_key_parts_2894():
    key = 2894
    data = de.load_data()
    assert af.get_key_parts(key, data) == (43, 56)


def test_check_keys_kay_a_1():
    data = de.load_data()
    with pytest.raises(SystemExit) as exc:
        af.check_keys(1, 0, "enc", data)

    assert exc.match("Cipher is weak if Key A is 1")


def test_check_keys_key_b_0():
    data = de.load_data()
    with pytest.raises(SystemExit) as exc:
        af.check_keys(7, 0, "enc", data)

    assert exc.match("Cipher is weak if Key B is 0")


def test_check_keys_key_a_and_b_less_0():
    data = de.load_data()
    with pytest.raises(SystemExit) as exc:
        af.check_keys(-7, -5, "enc", data)

    assert exc.match("Key A must be greater then 0 and Key B must be between")


def test_check_keys_key_gcd_not_equal_1():
    data = de.load_data()
    with pytest.raises(SystemExit) as exc:
        af.check_keys(60, 10, "enc", data)

    assert exc.match("are not relatively prime")


def test_affine_encrypt_message():
    data = de.load_data()
    key = 2894
    message = """"A computer would deserve to be called intelligent
          if it could deceive a human into believing that it was human."
          -Alan Turing"""
    message_enc = af.encrypt_message(key, message, data)
    assert message_enc != message
    message_dec = af.decrypt_message(key, message_enc, data)
    assert message_dec == message


def test_affine_all():
    r.seed(42)
    data = de.load_data()
    symbols_data = data["SYMBOLS"]
    for i in range(50):
        message = symbols_data * r.randint(4, 40)
        message = list(message)
        r.shuffle(message)
        message = "".join(message)

        print(f"Test {i+1}: {message[:50]}")
        key = af.get_random_key(data)
        encrypted = af.encrypt_message(key, message, data)
        decrypted = af.decrypt_message(key, encrypted, data)

        if message != decrypted:
            print(f"Mismatch with {key} and message {message}")
            print(f"Decrypted as: {decrypted}")
            sys.exit()


@pytest.mark.xfail
def test_affine_key_test():
    message = "Make things as simple as possible, but not simpler."
    data = de.load_data()
    symbols_data = data["SYMBOLS"]
    test_messages = {}
    for key_a in range(2, 80):
        key = key_a * len(symbols_data) + 1

        if cm.gcd(key_a, len(symbols_data)) == 1:
            cipher_text = af.encrypt_message(key, message, data)
            # print(f"{key_a}, {cipher_text}")
            if cipher_text in test_messages:
                print(
                    f"Key: {key_a} is a duplicate of key {test_messages[cipher_text]}"
                )
                pytest.fail()
            test_messages[cipher_text] = key_a
