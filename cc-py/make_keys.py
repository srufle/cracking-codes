#!/usr/bin/env python3
import argparse

import os
import random as r
import sys

import crypto_math as cm
import prime_num as pn


def main():
    parser = argparse.ArgumentParser(description="Public Key Generator")
    parser.add_argument("-g", "--gen-key", dest="gen_key", type=bool, default=True)
    parser.add_argument("-n", "--name", dest="name", type=str, default="nobody")
    parser.add_argument("-k", "--key-size", dest="key_size", type=int, default=1024)

    args = parser.parse_args()
    gen_key = args.gen_key
    name = args.name
    key_size = args.key_size

    if gen_key:
        print("Making key files")
        make_key_files(name, key_size)
        print("Done making files")
        return 0


def generate_key(key_size):
    p = 0
    q = 0
    print("Step 1: Create two prime numbers, p and q. Calculate n = p * q:")
    print("Generating p and q primes ...")
    while p == q:
        p = pn.generate_large_prime(key_size)
        q = pn.generate_large_prime(key_size)

    n = p * q

    print("Step 2: Create a number e that is relatively prime to (p-1)*(q-1):")
    print("Generating e that is relatively prime to (p-1)*(q-1)...")
    while True:
        e = r.randrange(2 ** (key_size - 1), 2 ** (key_size))
        if cm.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    print("Step 3: Calculate d, the mod inverse of e:")
    print("Calculating d that is mod inverse of e...")
    d = cm.find_mod_inverse(e, (p - 1) * (q - 1))

    public_key = (n, e)
    private_key = (n, d)

    print(f"Public Key:{public_key}")
    print(f"Private Key:{private_key}")

    return (public_key, private_key)


def make_key_files(name, key_size):

    pub_filename = f"pubkey_{name}.pub"
    priv_filename = f"privkey_{name}.priv"

    if os.path.exists(pub_filename) or os.path.exists(priv_filename):
        sys.exit(
            f"WARNING: The file {pub_filename} or {priv_filename} already exists! Rerun with a different name"
        )
    public_key, private_key = generate_key(key_size)
    print()
    print(
        f"The public key is a {len(str(public_key[0]))} and a {len(str(public_key[1]))} digit number."
    )
    print(f"Writing public key to file {pub_filename}")
    with open(pub_filename, "w") as fo:
        fo.write(f"{key_size},{public_key[0]},{public_key[1]}")

    print()
    print(
        f"The private key is a {len(str(private_key[0]))} and a {len(str(private_key[1]))} digit number."
    )
    print(f"Writing private key to file {priv_filename}")
    with open(priv_filename, "w") as fo:
        fo.write(f"{key_size},{private_key[0]},{private_key[1]}")


if __name__ == "__main__":
    main()
