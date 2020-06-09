#!/usr/bin/env python3

import random as r
import argparse

parser = argparse.ArgumentParser(description='Example')
parser.add_argument('-m', '--message', type=str)
parser.add_argument('-o', '--offset', type=int , default=3)

args = parser.parse_args()
print(f"{args} move: {args.message.split(' ')} over {args.offset}")

