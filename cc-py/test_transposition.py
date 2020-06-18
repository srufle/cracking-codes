#!/usr/bin/env python3
import random
import sys

import detect_english as de
import transposition


def test_detect_english_empty():
    data = de.load_data()
    assert not de.is_english("", data)


def test_detect_english_encrypted_text():
    words_file = de.get_words_file_path()
    data = de.load_data(words_file)
    encrypted_text = """
OI FEO
leN
oico p P t a  TtshVea e n p Sr e-le r arhIS e pnCIoa e c r sp  Meo  MehrCIhn
a  shICnehIe c r locCXhtm  K
aIli  OthVn p p t ahXho pISl pI  t  Le
oheor  IthIet r d  CS e orhIi e k  e  shXea  Tt d  D r shIf p K  e oDF
oico
e
ssmww ihf,  i
thiwe l  o, sa
tnpai , iretf
 ntvw iew tookreh n ti nv  leagco
wi    pchele wa uh nrFIcs
y depsvftneeletefrhsndySltrdntapai tea eebb,mhi e aeeaanaeeowgLniE n nnunrrgsehtiytsue i or s
 f e ECd, stj :
t moom yi ery s n.ef w eiai et wemsiirad hnettearewh
m iuahtieup  rvuanohtnaponh h,iof a lhrnord,wwe fao
 boF wendarvawaaieirs tthsoeh dt,wlrwtyustii  yatyy
mtasthrtlB  t, rswenetttwfarfhenstywsactuE aem nc
 to bem hbtcel imeito thoei easctwnr aiid sces-ahesttals  dd ly oago ng m e s fomnrt beafo,r omsdrnenahi
ia fsenLagl u   ldri otstlvpdcf fl
ros tithn amd e kf ,bu eecfm. ftmrnwasiai rurmni nhaS  kunnphate   tefnlaninoedr deade el  hlmtilnaet unt
eeeodrkeooashefat thnne rig dahsndyoha,r r-eocet-tsae
T
    """
    assert not de.is_english(
        encrypted_text, data, word_percentage=80, letter_percentage=80
    )


def test_detect_english_simple():
    words_file = de.get_words_file_path()
    data = de.load_data(words_file)
    clear_text = "Is this sentence English text?"
    assert de.is_english(clear_text, data, word_percentage=80, letter_percentage=80)


def test_trans_all():
    random.seed(42)

    for i in range(5):
        message = (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!? \n."
            * random.randint(4, 40)
        )
        message = list(message)
        random.shuffle(message)
        message = "".join(message)

        print(f"Test {i+1}: {message[:50]}")
        for key in range(1, int(len(message) / 2)):
            encrypted = transposition.encrypt_message(key, message)
            decrypted = transposition.decrypt_message(key, encrypted)

            if message != decrypted:
                print(f"Mismatch with {key} and message {message}")
                print(f"Decrypted as: {decrypted}")
                sys.exit()
