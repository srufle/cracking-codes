#!/usr/bin/env python3
import logging as log

import detect_english as de
import vigenere_hack as vh
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


def test_vigenere_hack():
    words_file = de.get_words_file_path("content/dictionary.txt")
    data = de.load_data(words_file)

    message = """Tzx isnz eccjxkg nfq lol mys bbqq I lxcz."""
    hacked_messages = vh.hack_vigenere_dict(message, data)
    for word in hacked_messages.keys():
        print(f"{word}: {hacked_messages[word]}")
    expected_key = "ASTRONOMY"
    expected_message = "The real secrets are not the ones I tell."
    assert expected_key in hacked_messages.keys()
    assert expected_message in hacked_messages.values()

