#!/usr/bin/env python3
import sys
import logging as log
import crypto_math as cm
import random as r
import affine as af
import detect_english as de
import pytest

log.basicConfig(level=log.INFO)


def test_get_key_parts_2894():
    key = 2894
    data = de.load_data()
    assert af.get_key_parts(key, data) == (43, 56)


def test_check_keys_kay_a_1():
    data = de.load_data()
    with pytest.raises(SystemExit) as exc:
        af.check_keys(1, 0, "enc", data)

    assert exc.match("Cipher is weak if Key A is 1") == True


def test_check_keys_key_b_0():
    data = de.load_data()
    with pytest.raises(SystemExit) as exc:
        af.check_keys(7, 0, "enc", data)

    assert exc.match("Cipher is weak if Key B is 0") == True


def test_check_keys_key_a_and_b_less_0():
    data = de.load_data()
    with pytest.raises(SystemExit) as exc:
        af.check_keys(-7, -5, "enc", data)

    assert exc.match("Key A must be greater then 0 and Key B must be between") == True


def test_check_keys_key_gcd_not_equal_1():
    data = de.load_data()
    with pytest.raises(SystemExit) as exc:
        af.check_keys(60, 10, "enc", data)

    assert exc.match("are not relatively prime") == True


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
    SYMBOLS = data["SYMBOLS"]
    for i in range(50):
        message = SYMBOLS * r.randint(4, 40)
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
