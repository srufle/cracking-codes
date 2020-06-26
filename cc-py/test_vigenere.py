#!/usr/bin/env python3
import logging as log

import detect_english as de
import vigenere as v
import freq_analysis as fa

log.basicConfig(level=log.INFO)
test_quote = """Alan Mathison Turing was a British mathematician, logician, cryptanalyst, and computer
            scientist. He was highly influential in the development of computer science, providing a
            formalisation of the concepts of "algorithm" and "computation" with the Turing machine. Turing
            is widely considered to be the father of computer science and artificial intelligence. During
            World War II, Turing worked for the Government Code and Cypher School (GCCS) at Bletchley Park,
            Britain's codebreaking centre. For a time he was head of Hut 8, the section responsible for
            German naval cryptanalysis. He devised a number of techniques for breaking German ciphers,
            including the method of the bombe, an electromechanical machine that could find settings
            for the Enigma machine. After the war he worked at the National Physical Laboratory, where
            he created one of the first designs for a stored-program computer, the ACE. In 1948 Turing
            joined Max Newman's Computing Laboratory at Manchester University, where he assisted in the
            development of the Manchester computers and became interested in mathematical biology. He wrote
            a paper on the chemical basis of morphogenesis, and predicted oscillating chemical reactions
            such as the Belousov-Zhabotinsky reaction, which were first observed in the 1960s. Turing's
            homosexuality resulted in a criminal prosecution in 1952, when homosexual acts were still
            illegal in the United Kingdom. He accepted treatment with female hormones (chemical castration)
            as an alternative to prison. Turing died in 1954, just over two weeks before his 42nd birthday,
            from cyanide poisoning. An inquest determined that his death was suicide; his mother and some
            others believed his death was accidental. On 10 September 2009, following an Internet campaign,
            British Prime Minister Gordon Brown made an official public apology on behalf of the British
            government for "the appalling way he was treated." As of May 2012 a private member's bill was
            before the House of Lords which would grant Turing a statutory pardon if enacted."""


def test_vigenere_gen_key_default():

    data = de.load_data()
    key = v.get_random_key(data)

    assert len(key) == 14
    assert key.isalpha()


def test_freq_get_letter_count():

    data = de.load_data()
    message = test_quote
    letter_count = fa.get_letter_count(message, data)
    expected_letter_count = {
        "A": 135,
        "B": 30,
        "C": 74,
        "D": 58,
        "E": 196,
        "F": 37,
        "G": 39,
        "H": 87,
        "I": 139,
        "J": 2,
        "K": 8,
        "L": 62,
        "M": 58,
        "N": 122,
        "O": 113,
        "P": 36,
        "Q": 2,
        "R": 106,
        "S": 89,
        "T": 140,
        "U": 37,
        "V": 14,
        "W": 30,
        "X": 3,
        "Y": 21,
        "Z": 1,
    }
    assert letter_count == expected_letter_count


def test_freq_get_frequency_order():
    data = de.load_data()
    message = test_quote
    frequency_order = fa.get_frequency_order(message, data)
    assert frequency_order == "ETIANORSHCLMDGFUPBWYVKXQJZ"


def test_vigenere_quote():
    data = de.load_data()
    key = "ASIMOV"
    message = test_quote

    encrypted_message = v.encrypt_message(key, message, data)
    assert encrypted_message != message
    print(encrypted_message)

    decrypt_message = v.decrypt_message(key, encrypted_message, data)
    assert decrypt_message == message

