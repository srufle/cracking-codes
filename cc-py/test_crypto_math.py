#!/usr/bin/env python3
import logging as log
import crypto_math as cm

log.basicConfig(level=log.INFO)


def test_gcd_0_0():
    assert cm.gcd(0, 0) == 0


def test_gcd_24_32():
    assert cm.gcd(24, 32) == 8


def test_gcd_409119243_87780243():
    assert cm.gcd(409119243, 87780243) == 6837


def test_gcd_10_15():
    assert cm.gcd(10, 15) == 5


def test_find_mod_inverse_7_26():
    assert cm.find_mod_inverse(7, 26) == 15


def test_find_mod_inverse_8953851_26():
    assert cm.find_mod_inverse(8953851, 26) == 17


# def test_find_key():
#     b = 66
#     for a in range(0, b):
#         ans = cm.gcd(a, b)
#         if ans == 1:
#             print(f"key={a}")
#     pass
