def get_letter_count(message, data):
    LETTERS = data["LETTERS"]
    letter_count = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 0,
        "F": 0,
        "G": 0,
        "H": 0,
        "I": 0,
        "J": 0,
        "K": 0,
        "L": 0,
        "M": 0,
        "N": 0,
        "O": 0,
        "P": 0,
        "Q": 0,
        "R": 0,
        "S": 0,
        "T": 0,
        "U": 0,
        "V": 0,
        "W": 0,
        "X": 0,
        "Y": 0,
        "Z": 0,
    }
    for letter in message.upper():
        if letter in LETTERS:
            letter_count[letter] += 1

    return letter_count


def get_item_at_index_zero(items):
    return items[0]


def get_frequency_order(message, data):
    # Returns a string of the alphabet letters arranged in order of most
    # frequently occurring in the message parameter.

    letter_to_freq = get_letter_count(message, data)
    LETTERS = data["LETTERS"]
    ETAOIN = data["ETAOIN"]
    freq_to_letter = {}
    for letter in LETTERS:
        if letter_to_freq[letter] not in freq_to_letter:
            freq_to_letter[letter_to_freq[letter]] = [letter]
        else:
            freq_to_letter[letter_to_freq[letter]].append(letter)

    for freq in freq_to_letter:
        freq_to_letter[freq].sort(key=ETAOIN.find, reverse=True)
        freq_to_letter[freq] = "".join(freq_to_letter[freq])

    freq_pairs = list(freq_to_letter.items())
    freq_pairs.sort(key=get_item_at_index_zero, reverse=True)

    freq_order = []
    for freq_pair in freq_pairs:
        freq_order.append(freq_pair[1])

    return "".join(freq_order)


def english_freq_match(message, data):
    # Return the number of matches that the string in the message
    # parameter has when its letter frequency is compared to English
    # letter frequency. A "match" is how many of its six most frequent
    # and six least frequent letters are among the six most frequent and
    # six least frequent letters for English.
    ETAOIN = data["ETAOIN"]

    freq_order = get_frequency_order(message, data)
    match_score = 0
    for common_letter in ETAOIN[:6]:
        if common_letter in freq_order[:6]:
            match_score += 1

    for uncommon_letter in ETAOIN[:-6]:
        if uncommon_letter in freq_order[:-6]:
            match_score += 1

    return match_score
