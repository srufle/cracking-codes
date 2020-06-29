#!/usr/bin/env python3
import logging as log

import detect_english as de
import vigenere_hack as vh
import freq_analysis as fa
import pytest

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
            as an alternative to prison. Turing
             died in 1954, just over two weeks before his 42nd birthday,
            from cyanide poisoning. An inquest determined that his death was suicide; his mother and some
            others believed his death was accidental. On 10 September 2009, following an Internet campaign,
            British Prime Minister Gordon Brown made an official public apology on behalf of the British
            government for "the appalling way he was treated." As of May 2012 a private member's bill was
            before the House of Lords which would grant Turing a statutory pardon if enacted."""


def test_vigenere_hack_dict():
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


def test_vigenere_hack_kasiski():
    words_file = de.get_words_file_path("content/dictionary.txt")
    data = de.load_data(words_file)

    message = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi, lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum. Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg (GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi 1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg, ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz 1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""
    _is_done, hacked_messages = vh.hack_vigenere_kasiski(message, data)
    # for word in hacked_messages.keys():
    #     print(f"{word}: {hacked_messages[word]}")
    expected_key = "ASIMOV"
    expected_message = """Alan Mathison Turing was a British mathematician, logician, cryptanalyst, and computer scientist. He was highly influential in the development of computer science, providing a formalisation of the concepts of "algorithm" and "computation" with the Turing machine. Turing is widely considered to be the father of computer science and artificial intelligence. During World War II, Turing worked for the Government Code and Cypher School (GCCS) at Bletchley Park, Britain's codebreaking centre. For a time he was head of Hut 8, the section responsible for German naval cryptanalysis. He devised a number of techniques for breaking German ciphers, including the method of the bombe, an electromechanical machine that could find settings for the Enigma machine. After the war he worked at the National Physical Laboratory, where he created one of the first designs for a stored-program computer, the ACE. In 1948 Turing joined Max Newman's Computing Laboratory at Manchester University, where he assisted in the development of the Manchester computers and became interested in mathematical biology. He wrote a paper on the chemical basis of morphogenesis, and predicted oscillating chemical reactions such as the Belousov-Zhabotinsky reaction, which were first observed in the 1960s. Turing's homosexuality resulted in a criminal prosecution in 1952, when homosexual acts were still illegal in the United Kingdom. He accepted treatment with female hormones (chemical castration) as an alternative to prison. Turing died in 1954, just over two weeks before his 42nd birthday, from cyanide poisoning. An inquest determined that his death was suicide; his mother and some others believed his death was accidental. On 10 September 2009, following an Internet campaign, British Prime Minister Gordon Brown made an official public apology on behalf of the British government for "the appalling way he was treated." As of May 2012 a private member's bill was before the House of Lords which would grant Turing a statutory pardon if enacted."""
    assert expected_key in hacked_messages.keys()
    assert expected_message in hacked_messages.values()


def test_vigenere_hack_get_useful_factors():
    factors = vh.get_useful_factors(144)
    expected_factors = [2, 3, 4, 6, 8, 9, 12, 16]
    assert expected_factors == factors


def test_vigenere_hack_get_nth_subkeys_letters():
    assert vh.get_nth_subkeys_letters(1, 3, "ABCABCABC") == "AAA"
    assert vh.get_nth_subkeys_letters(2, 3, "ABCABCABC") == "BBB"
    assert vh.get_nth_subkeys_letters(3, 3, "ABCABCABC") == "CCC"
    assert vh.get_nth_subkeys_letters(1, 5, "ABCDEFGHI") == "AF"
