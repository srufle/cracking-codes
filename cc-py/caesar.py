#!/usr/bin/env python3

import sys

source_text = "abcdefghijklmnopqrstuvwxyz1234567890"


def create_lookup(source, offset=3):
    encoding_lookup = {}
    encoding_lookup['offset'] = offset
    source_len = len(source)
    for index in range(len(source)):
        new_index = (index+offset) % source_len
        print(f"{source[index]} = {source[new_index]}")
        encoding_lookup[source[index].upper()] = source[new_index].upper()
    return encoding_lookup


def encode(char):
    upper_char = char.upper()
    if upper_char in encoding_lookup.keys():
        encoded_char = encoding_lookup[upper_char]
    else:
        encoded_char = char

    return (upper_char, encoded_char)


result = []
encoding_lookup = create_lookup(source_text)
for line in sys.stdin:
    chars = line.rstrip()
    for char in chars:
        encoded = encode(char)
        print(f"{encoded[0]} = {encoded[1]}")
        result += [encoded[1]]


print("Message:")
print(f"{encoding_lookup['offset']}{''.join(result)}")
