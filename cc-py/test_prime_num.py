#!/usr/bin/env python3
import logging as log

import prime_num as pn
import pytest

log.basicConfig(level=log.INFO)


def test_prime_num_is_prime():
    assert not pn.is_prime(1)
    assert pn.is_prime(2)
    assert pn.is_prime(3)
    assert pn.is_prime(5)
    assert not pn.is_prime(14)
    assert pn.is_prime(101)
    assert pn.is_prime(4093)
    assert pn.is_prime(104729)


def test_prime_num_is_prime_trial_div():
    assert not pn.is_prime_trial_div(1)
    assert pn.is_prime_trial_div(2)
    assert pn.is_prime_trial_div(3)
    assert pn.is_prime_trial_div(5)
    assert not pn.is_prime_trial_div(14)
    assert pn.is_prime_trial_div(101)
    assert pn.is_prime_trial_div(4093)
    assert pn.is_prime_trial_div(104729)


def test_prime_num_prime_sieve():
    assert pn.prime_sieve(1) == []
    assert pn.prime_sieve(2) == []
    assert pn.prime_sieve(3) == [2]
    assert pn.prime_sieve(14) == [2, 3, 5, 7, 11, 13]


def test_prime_num_rabin_miller():
    assert not pn.rabin_miller(1)
    assert not pn.rabin_miller(2)
    assert pn.rabin_miller(3)
    assert not pn.rabin_miller(14)
    assert pn.rabin_miller(104729)


def test_prime_num_generate_large_prime_1024_default():
    large_prime = pn.generate_large_prime()
    assert pn.is_prime(large_prime)


def test_prime_num_generate_large_prime_2048():
    assert pn.is_prime(pn.generate_large_prime(key_size=2048))


def test_prime_num_generate_large_prime_512():
    assert pn.is_prime(pn.generate_large_prime(key_size=512))

