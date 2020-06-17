#!/usr/bin/env python3
import sys
import argparse
import math
import time, os, datetime
import logging as log
from pathlib import Path


def gcd(a, b):
    # Greatest Common Divisor
    # https://en.wikipedia.org/wiki/Euclidean_algorithm
    while a != 0:
        a, b = b % a, a

    return b


def find_mod_inverse(a, m):
    # Modular inverse
    # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm

    # Return the modular inverse of a % m, which is
    # the number x such that a*x % m = 1.
    if gcd(a, m) != 1:
        return None

    # Calculate using the extended Euclidean algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3

    return u1 % m
