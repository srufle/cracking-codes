#!/usr/bin/env python3

import sys

result = []
for line in sys.stdin:
    chars = line.strip()
    index = len(chars) - 1
    while index >= 0:
        char = chars[index]
        result += [char]
        index -= 1


print("Message:")
print(f"{''.join(result)}")
