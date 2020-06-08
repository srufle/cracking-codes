#!/bin/bash

cargo build
TEXT="Three can keep a secret, if two of them are dead."
echo "** Morse **"
echo -e ${TEXT} | target/debug/morse
echo "** Caesar 1 (encode) **"
echo -e ${TEXT} | target/debug/caesar

TEXT_2="WKUHH FDQ̃ NHHS D VHFUHW, LI WZR RI WKHP DUH GHDG."
echo "** Caesar 2 (decode) **"
echo -e ${TEXT_2} | target/debug/caesar

TEXT="Three can\u0303 keep a secret, if two of them are dead."
echo "** Reverse 1 (encode) **"
echo -e ${TEXT} | target/debug/reverse

TEXT_2=".daed era meht fo owt fi ,terces a peek ñac eerhT"
echo "** Reverse 2 (decode) **"
echo -e ${TEXT_2} | target/debug/reverse