#!/usr/bin/env python3
import logging as log

import detect_english as de
import simple_sub as ss
import simple_sub_hack as ssh

log.basicConfig(level=log.INFO)


def test_detect_english_make_word_patterns():
    words_file = de.get_words_file_path()
    data = de.load_data(words_file)
    data = de.make_word_patterns(data)

    print(f"WORD_PATTERNS len = {len(data['WORD_PATTERNS'])}")
    pattern_values = []
    index = 0
    limit = 5
    for key in data["WORD_PATTERNS"].keys():
        value = data["WORD_PATTERNS"][key]
        pattern_values.append((key, value))
        index += 1
        if index == limit:
            break

    print(f"WORD_PATTERNS = {pattern_values}")
    assert len(data["WORD_PATTERNS"]) != 0


def test_simple_sub_hack_simple():

    words_file = de.get_words_file_path("content/dictionary.txt")
    # words_file = de.get_words_file_path()
    data = de.load_data(words_file)
    data = de.make_word_patterns(data)

    message = "OLQIHXIRCKGNZ PLQRZKBZB MPBKSSIPLC"
    clear_message = "UNCOMFORTABLE INCREASES DISAPPOINT"
    possible_mapping = ssh.hack_possible_mapping(message, data)
    print(f"possible_mapping={possible_mapping}")
    hacked_message = ssh.decrypt_with_hacked_key(message, possible_mapping, data)
    print(f"message={message}")
    print(f"hacked_message={hacked_message}")
    assert hacked_message != message

    assert hacked_message == clear_message


def test_simple_sub_hack_quote():

    words_file = de.get_words_file_path("content/dictionary.txt")
    # words_file = de.get_words_file_path()
    data = de.load_data(words_file)
    data = de.make_word_patterns(data)

    # Valid Quote keys:
    # LxWOAYUISxxMNXPxxCRJTQExxZ - from /home/srufle/Downloads/CrackingCodesFiles/
    # lxwoayuisxxmnxpxxcrjtqexxz - from our own calculation
    # Full good: LFWOAYUISVKMNXPBDCRJTQEGHZ - default test key

    message = """Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm
        rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra
        jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor
        l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax
        px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh.
        -Facjclxo Ctrramm"""

    clear_message = """If a man is offered a fact which goes against his instincts, he will
        scrutinize it closel_, and unless the evidence is overwhelming, he will refuse
        to _elieve it. If, on the other hand, he is offered something which affords
        a reason for acting in accordance to his instincts, he will acce_t it even
        on the slightest evidence. The origin of m_ths is e__lained in this wa_.
        -_ertrand Russell"""
    possible_mapping = ssh.hack_possible_mapping(message, data)
    print(f"possible_mapping={possible_mapping}")
    hacked_message = ssh.decrypt_with_hacked_key(message, possible_mapping, data)
    print(f"message={message}")
    print(f"hacked_message={hacked_message}")
    assert hacked_message != message

    assert hacked_message == clear_message


# def test_simple_sub_hack_add_letters_to_mapping():
#     letter_mapping = {}
#     cipher_word = "HGHHU"
#     mapping = "0.1.0.0.2"

#     ssh.add_letters_to_mapping(letter_mapping, cipher_word, "PUPPY")
