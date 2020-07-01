#!/usr/bin/env python3
import logging as log
import os

import public_key as pk

log.basicConfig(level=log.INFO)


def test_pub_key_get_blocks_from_text():
    message = "Howdy"
    block_size = 66
    block_ints = pk.get_blocks_from_text(message, block_size)
    assert block_ints == [957285919]


def test_pub_get_text_from_blocks():
    expected_message = "Howdy"
    message_len = len(expected_message)
    block_ints = [957285919]
    block_size = 66
    message = pk.get_text_from_blocks(block_ints, message_len, block_size)
    assert message == expected_message


def test_pub_key_encrypt_message():
    message = "Howdy"
    n = 116284564958604315258674918142848831759
    e = 13805220545651593223
    key = (n, e)
    block_size = 66
    block_ints = pk.encrypt_message(message, key, block_size)
    assert block_ints == [43924807641574602969334176505118775186]


def test_pub_key_decrypt_message():
    expected_message = "Howdy"
    n = 116284564958604315258674918142848831759
    d = 72424475949690145396970707764378340583
    key = (n, d)
    message_len = len(expected_message)
    block_ints = [43924807641574602969334176505118775186]
    block_size = 66
    message = pk.decrypt_message(block_ints, message_len, key, block_size)
    assert message == expected_message


def test_pub_key_long_message():
    message_filename = "test_message_long.enc"
    key_filename = "pubkey_nobody.pub"
    message = "Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets. Gerald Priestland. The Founding Fathers gave the free press the protection it must have to bare the secrets of government and inform the people. Hugo Black."
    encrypted_content = pk.encrypt_and_write_file(
        message_filename, key_filename, message
    )

    key_filename = "privkey_nobody.priv"
    decrypted_content = pk.read_from_file_and_decrypt(message_filename, key_filename)
    assert decrypted_content == message


def test_pub_key_encrypt_and_write_file():
    message_filename = "test_message.enc"
    key_filename = "pubkey_nobody.pub"
    message = "Howdy"
    encrypted_content = pk.encrypt_and_write_file(
        message_filename, key_filename, message
    )
    assert os.path.exists(key_filename)
    assert encrypted_content.count("_") == 2


def test_pub_key_read_from_file_and_decrypt():
    message_filename = "test_message.enc"
    key_filename = "privkey_nobody.priv"
    message = "Howdy"
    decrypted_content = pk.read_from_file_and_decrypt(message_filename, key_filename)
    assert decrypted_content == message
