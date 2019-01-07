
def match_consonate(c1, c2):
    if set(['C', 'K']) == set([c1, c2]):
        return True
    if set(['CR', 'KR']) == set([c1, c2]):
        return True
    if set(['CHR', 'KR']) == set([c1, c2]):
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
    if set(['PS', 'S']) == set([c1, c2]):
        return True
    if set(['WR', 'R']) == set([c1, c2]):
        return True
    if set(['RH', 'R']) == set([c1, c2]):
        return True
    if set(['WH', 'W']) == set([c1, c2]):
        return True

    return c1 == c2


def first_vowels(word, leading_vowel = False):
    vowels = ['A', 'E', 'I', 'O', 'U', 'Y']
    value = ''
    first_vowel_found = False
    for letter in word:
        if letter not in vowels and first_vowel_found:
            break
        if letter in vowels:
            value += letter
            first_vowel_found = True

    if leading_vowel == False:
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
        if value == 'UE':
            value = 'U'
    else:
        if value == 'OY':
            value = 'OI'


    if 'AA' in value:
        value = value.replace('AA', 'A')

    return value


def first_consonants(word):
    consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'X', 'W', 'V', 'Z']
    value = ''
    first_consonant_found = False
    for letter in word:
        if letter not in consonants and first_consonant_found:
            break
        if letter in consonants:
            value += letter
            first_consonant_found = True

    if 'GG' in value:
        value = value.replace('GG', 'G')

    return value


def has_leading_vowel(word):
    if word[0] in ['A', 'E', 'I', 'O', 'U', 'Y']:
        return True
    else:
        return False


def designations():
    return [
        'AN',
        'AND',
        'ARE',
        'AS',
        'AT',
        'BE',
        'BUT',
        'BY',
        'FOR',
        'IF',
        'IN',
        'INTO',
        'IS',
        'IT',
        'NO',
        'NOT',
        'O',
        'ON',
        'OR',
        'SUCH',
        'THAT',
        'THE',
        'THEIR',
        'THEN',
        'THERE',
        'THESE',
        'THEY',
        'THIS',
        'TO',
        'ASSOCIATION',
        'ASSOC',
        'ASSOC.',
        'ASSN',
        'ASSN.',
        'COMPANY',
        'CO',
        'CO.',
        'CORPORATION',
        'CORP',
        'CORP.',
        'INCORPORATED',
        'INC',
        'INC.',
        'INCORPOREE',
        'LIABILITY',
        'LIMITED',
        'LTD',
        'LTD.',
        'LIMITEE',
        'LTEE',
        'LTEE.',
        'SOCIETY',
        'SOC',
        'SOC.'
    ]
