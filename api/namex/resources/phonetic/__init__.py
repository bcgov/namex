import pronouncing

def match_consons(c1, c2):

    if set(['C', 'G']) == set([c1, c2]):
        return True
    if set(['C', 'K']) == set([c1, c2]):
        return True
    if set(['CR', 'KR']) == set([c1, c2]):
        return True
    if set(['CL', 'KL']) == set([c1, c2]):
        return True
    if set(['PH', 'F']) == set([c1, c2]):
        return True
    if set(['GH', 'G']) == set([c1, c2]):
        return True
    if set(['GN', 'N']) == set([c1, c2]):
        return True
    if set(['KN', 'N']) == set([c1, c2]):
        return True
    if set(['PN', 'N']) == set([c1, c2]):
        return True
    if set(['WR', 'R']) == set([c1, c2]):
        return True
    if set(['RH', 'R']) == set([c1, c2]):
        return True

    return c1 == c2


def first_vowels(word):
    vowels = ['A', 'E', 'I', 'O', 'U', 'Y']
    value = ''
    first_vowel_found = False
    for letter in word:
        if letter not in vowels and first_vowel_found:
            break
        if letter in vowels:
            value += letter
            first_vowel_found = True

    if value == 'EY':
        value = 'A'
    if value == 'EI':
        value = 'A'
    if value == 'EA':
        value = 'A'
    if value == 'AY':
        value = 'A'
    if value == 'AI':
        value = 'A'
    if value == 'Y':
        value = 'I'

    return value


def first_consonants(word):
    consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'X']
    value = ''
    first_consonant_found = False
    for letter in word:
        if letter not in consonants and first_consonant_found:
            break
        if letter in consonants:
            value += letter
            first_consonant_found = True

    return value


def first_arpabet(word):
    arpabet = pronouncing.phones_for_word(word)
    if not arpabet:
        return word
    return arpabet
