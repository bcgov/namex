_VOWELS = ['A', 'E', 'I', 'O', 'U', 'Y']
_NON_LEADING_VOWEL_FOLDS = {
    'EY': 'A',
    'EI': 'A',
    'EA': 'A',
    'AY': 'A',
    'AI': 'A',
    'Y': 'I',
    'UE': 'U',
}
_CONSONANTS = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'X', 'W', 'V', 'Z']
_CONSONANT_FOLDS = (
    ('CHR', 'KR'),
    ('GG', 'G'),
    ('C', 'K'),
    ('CR', 'KR'),
    ('CL', 'KL'),
    ('PH', 'F'),
    ('GH', 'G'),
    ('GN', 'N'),
    ('KN', 'N'),
    ('PN', 'N'),
    ('PS', 'S'),
    ('WR', 'R'),
    ('RH', 'R'),
    ('WH', 'W'),
)


def first_vowels(word, leading_vowel=False):
    value = ''
    first_vowel_found = False
    for letter in word:
        if letter not in _VOWELS and first_vowel_found:
            break
        if letter in _VOWELS:
            value += letter
            first_vowel_found = True

    if not leading_vowel:
        value = _NON_LEADING_VOWEL_FOLDS.get(value, value)
    elif value == 'OY':
        value = 'OI'

    if 'AA' in value:
        value = value.replace('AA', 'A')

    return value


def first_consonants(word):
    value = ''
    first_consonant_found = False
    for letter in word:
        if letter not in _CONSONANTS and first_consonant_found:
            break
        if letter in _CONSONANTS:
            value += letter
            first_consonant_found = True

    for old, new in _CONSONANT_FOLDS:
        if old in value:
            value = value.replace(old, new)

    return value


def has_leading_vowel(word):
    return word[0] in _VOWELS


def replace_special_leading_sounds(word):
    for special_leading_sound, replacement in [['QU', 'KW'], ['EX', 'X'], ['MAC', 'MC']]:
        if word[: len(special_leading_sound)] == special_leading_sound:
            word = replacement + word[len(special_leading_sound) :]

    return word


def keep_phonetic_match(word, query):
    word = (word or "").upper()
    query = (query or "").upper()
    if not word or not query:
        return False

    word = replace_special_leading_sounds(word)
    query = replace_special_leading_sounds(query)
    if not word or not query:
        return False

    word_has_leading_vowel = has_leading_vowel(word)
    query_has_leading_vowel = has_leading_vowel(query)

    word_first_consonant = first_consonants(word)
    query_first_consonant = first_consonants(query)

    query_first_vowels = first_vowels(query, query_has_leading_vowel)
    word_first_vowels = first_vowels(word, word_has_leading_vowel)

    if query_has_leading_vowel:
        query_sound = query_first_vowels + query_first_consonant
    else:
        query_sound = query_first_consonant + query_first_vowels

    if word_has_leading_vowel:
        word_sound = word_first_vowels + word_first_consonant
    else:
        word_sound = word_first_consonant + word_first_vowels

    return word_sound == query_sound
