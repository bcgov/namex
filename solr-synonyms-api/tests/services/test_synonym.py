import pytest

from . import (
    designation_all_regex,
    exceptions_ws,
    internet_domains,
    numbers,
    ordinal_suffixes,
    prefixes,
    stand_alone_words,
    syn_svc,
)

# class TestSynonymService(TestCase):
"""
1. - Replace with non - space
    A. -.com: internet_domains
    B. - Commas in numbers: 50, 000 --> 50000
    B. - Set together words followed by punctuation and a character
    C. - Designations anywhere
"""


@pytest.mark.parametrize("name, expected",
                         [
                             ("TOBI.COM CANADA OPERATIONS LTD.", "TOBI CANADA OPERATIONS"),
                             ("TOBI.ORG CANADA OPERATIONS LTD.", "TOBI CANADA OPERATIONS"),
                             ("TOBI.NET CANADA OPERATIONS LTD.", "TOBI CANADA OPERATIONS"),
                             ("TOBI.EDU CANADA OPERATIONS LTD.", "TOBI CANADA OPERATIONS"),
                             ("ONE AND 1,000 NIGHTS GROUP", "ONE AND 1000 NIGHTS GROUP"),
                             ("AB-C HOMES LTD.", "ABC HOMES"),
                             ("MOUNTAIN VIEW INC. FOOD", "MOUNTAIN VIEW FOOD")
                         ]
                         )
def test_regex_remove_designations(name, expected):
    assert syn_svc.regex_remove_designations(name, internet_domains, designation_all_regex) == expected


"""
2.- Search for prefixes followed by punctuation and a word (re/max) and set them together
"""


@pytest.mark.parametrize("name, expected",
                         [
                             ("MONTESSORI PRE-SCHOOL LTD.", "MONTESSORI PRESCHOOL LTD."),
                             ("HOME STAGING & RE-DESIGN INC.", "HOME STAGING & REDESIGN INC."),
                             ("DIS-DRESS BEAD & GIFT STORE LTD", "DISDRESS BEAD & GIFT STORE LTD")
                         ])
def test_regex_prefixes(name, expected):
    assert syn_svc.regex_prefixes(name, prefixes) == expected


"""
3.- Replace with space the following:
        A.- Word with possesive such as Reynold's
        B.- (NO. 111),NO. 465,(LOT 111),LOT 27,LOT( 100-2),(100)
"""


@pytest.mark.parametrize("name, expected",
                         [
                             ("REYNOLD'S HAIR SALON", "REYNOLD HAIR SALON"),
                             ("NO. 346 CATHEDRAL VENTURES LTD.", "CATHEDRAL VENTURES LTD"),
                             ("STONEWATER VENTURES (NO. 133) LTD.", "STONEWATER VENTURES LTD"),
                             ("LOT 30 DESIGN STUDIO", "DESIGN STUDIO"),
                             ("SAAS FEE (LOT 1) HOLDINGS INC.", "SAAS FEE HOLDINGS INC")
                         ])
def test_regex_numbers_lot(name, expected):
    assert syn_svc.regex_numbers_lot(name) == expected


"""
4.- Remove repeated strings with minimum two characters.
"""


@pytest.mark.parametrize("name, expected",
                         [
                             ("LE-LA-LA PRODUCTIONS INC.", "LE-LA PRODUCTIONS INC.")
                         ])
def test_regex_repeated_strings(name, expected):
    assert syn_svc.regex_repeated_strings(name) == expected


"""
5.- Separate ordinal numbers from words (4THGEN --> 4TH GEN):
"""


@pytest.mark.parametrize("name, expected",
                         [
                             ("4THGEN PHARMACIES INC.", "4TH GEN PHARMACIES INC."),
                             ("4THGENFALLING LTD.", "4TH GENFALLING LTD.")
                         ])
def test_regex_separate_ordinals(name, expected):
    assert syn_svc.regex_separated_ordinals(name, ordinal_suffixes) == expected


"""
6.- Replace with space: 
    Alphanumeric strings separating strings from letters as long as they are not in exception list (substitution list):
    For instance 1st,h20 are not separated because they are in substitution list, but P8 is transformed to P 8 
"""


@pytest.mark.parametrize("name, expected",
                         [
                             ("ACTIV8 RECRUITMENT", "ACTIV8 RECRUITMENT"),
                             ("COASTAL PURE H20", "COASTAL PURE H20"),
                             ("H24 HOTEL RESORT", "H 24 HOTEL RESORT")
                         ])
def test_regex_keep_together_abv(name, expected):
    assert syn_svc.regex_keep_together_abv(name, exceptions_ws) == expected


"""
7.- Replace with space:
        Punctuation including ampersand, slash, hyphen used for separation
"""


@pytest.mark.parametrize("name, expected",
                         [
                             ("WESTMOUNT PLUMBING & HEATING LTD.", "WESTMOUNT PLUMBING HEATING LTD.")
                         ])
def test_regex_punctuation(name, expected):
    assert syn_svc.regex_punctuation(name) == expected


"""
8.- Replace with non-space:
    Set together letter of length one separated by spaces.
    Trailing and leading spaces in string
"""


@pytest.mark.parametrize("name, expected",
                         [
                             ("S J FENCING LTD.", "SJ FENCING LTD."),
                             ("A D ALTERNATIVE SOLUTIONS LTD.", "AD ALTERNATIVE SOLUTIONS LTD.")
                         ])
def test_regex_together_one_letter(name, expected):
    assert syn_svc.regex_together_one_letter(name) == expected


"""
9.- Replace with non-space the following:
         Remove cardinal and ordinal numbers from string in the middle and end: (?<=[A-Za-z]\b )([ 0-9]*(ST|[RN]D|TH)?\b)
"""


@pytest.mark.parametrize("name, expected",
                         [
                             ("ARMSTRONG 111 PLUMBING", "ARMSTRONG PLUMBING"),
                             ("ARMSTRONG PLUMBING 111", "ARMSTRONG PLUMBING"),
                             ("ARMSTRONG 111 PLUMBING 111", "ARMSTRONG PLUMBING"),
                             ("123 HOLDINGS 2020", "123 HOLDINGS"),
                             ("ARMSTRONG 20 20 VISION", "ARMSTRONG VISION"),
                             ("ARMSTRONG VISION 20 20", "ARMSTRONG VISION"),
                             ("ARMSTRONG ONE HUNDRED ELEVEN PLUMBING","ARMSTRONG PLUMBING"),
                             ("ARMSTRONG PLUMBING ONE HUNDRED ELEVENTH", "ARMSTRONG PLUMBING")
                         ])
def test_regex_strip_out_numbers_middle_end(name, expected):
    assert syn_svc.regex_strip_out_numbers_middle_end(name,ordinal_suffixes, numbers) == expected


"""
10.- Replace with non-space:
    Remove numbers and numbers in words at the beginning or keep them as long as the last string is 
    any BC|HOLDINGS|VENTURES:    
"""


@pytest.mark.parametrize("name, expected",
                         [
                             ("ONE TWO THREE HOLDINGS", "ONE TWO THREE HOLDINGS"),
                             ("123 HOLDINGS", "123 HOLDINGS"),
                             ("FIRST SECOND HOLDINGS", "FIRST SECOND HOLDINGS"),
                             ("1ST 2ND HOLDINGS", "1ST 2ND HOLDINGS"),
                             ("ONE TWO THREE CANADA", "CANADA"),
                             ("123 CANADA", "CANADA"),
                             ("FIRST SECOND THIRD CANADA", "CANADA"),
                             ("1ST 2ND 3RD CANADA", "CANADA"),
                             ("123 CATHEDRAL VENTURES","CATHEDRAL VENTURES"),
                             ("123 VENTURES", "123 VENTURES"),
                             ("ONE ARMSTRONG PLUMBING AND HEATING", "ARMSTRONG PLUMBING AND HEATING")
                         ])
def test_regex_numbers_standalone(name, expected):
    assert syn_svc.regex_numbers_standalone(name, ordinal_suffixes, numbers, stand_alone_words) == expected
