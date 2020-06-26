#!/usr/bin/env python3
import logging as log

import detect_english as de
import vigenere as v

log.basicConfig(level=log.INFO)


def test_vigenere_gen_key_default():

    data = de.load_data()
    key = v.get_random_key(data)

    assert len(key) == 14
    assert key.isalpha()


def test_vigenere_quote():
    data = de.load_data()
    key = "ASIMOV"
    message = """Alan Mathison Turing was a British mathematician,
            logician, cryptanalyst, and computer scientist."""

    encrypted_message = v.encrypt_message(key, message, data)
    assert encrypted_message != message
    print(encrypted_message)

    decrypt_message = v.decrypt_message(key, encrypted_message, data)
    assert decrypt_message == message

