#!/usr/bin/env python3
import logging as log


import detect_english as de
import simple_sub as ss

log.basicConfig(level=log.INFO)


def test_simple_sub_encrypt_message_known_key():
    data = de.load_data()
    key = "LFWOAYUISVKMNXPBDCRJTQEGHZ"
    message = """"A computer would deserve to be called intelligent
          if it could deceive a human into believing that it was human."
          -Alan Turing"""
    message_enc = ss.encrypt_message(key, message, data)
    assert message_enc != message
    message_dec = ss.decrypt_message(key, message_enc, data)
    assert message_dec == message


def test_simple_sub_encrypt_message_generated_key():
    data = de.load_data()

    for i in range(50):
        key = ss.get_random_key(data)
        message = """"A computer would deserve to be called intelligent
            if it could deceive a human into believing that it was human."
            -Alan Turing"""
        message_enc = ss.encrypt_message(key, message, data)
        assert message_enc != message
        message_dec = ss.decrypt_message(key, message_enc, data)
        assert message_dec == message


def test_simple_sub_encrypt_message_is_key_valid_too_short():
    data = de.load_data()
    key = "ABC"
    assert not ss.is_key_valid(key, data)


def test_simple_sub_encrypt_message_is_key_valid_all_A():
    data = de.load_data()
    key = "A" * 26
    assert not ss.is_key_valid(key, data)


def test_simple_sub_encrypt_message_is_key_valid_valid():
    data = de.load_data()
    key = "LFWOAYUISVKMNXPBDCRJTQEGHZ"
    assert ss.is_key_valid(key, data)


def test_simple_sub_encrypt_message_is_key_valid_too_long():
    data = de.load_data()
    key = "LFWOAYUISVKMNXPBDCRJTQEGHZ" * 2
    assert not ss.is_key_valid(key, data)
