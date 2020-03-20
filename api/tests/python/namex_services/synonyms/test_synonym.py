import pytest
from hamcrest import assert_that

from tests.python.namex_services.synonyms import syn_svc, designation_all_regex, prefixes, ordinal_suffixes, exceptions_ws, numbers, stand_alone_words

from unittest import TestCase


class TestSynonymService(TestCase):
    '''
    1. - Replace with non - space
        A. -.com: internet_domains
        B. - Commas in numbers: 50, 000 --> 50000
        B. - Set together words followed by punctuation and a character
        C. - Designations anywhere
    '''

    def test_regex_remove_designations(self):
        companies = ["TOBI.COM CANADA OPERATIONS LTD.", "ONE AND 1,000 NIGHTS GROUP", "AB-C HOMES LTD.",
                     "MOUNTAIN VIEW INC. FOOD"]
        expected = ["TOBI CANADA OPERATIONS", "ONE 1000 NIGHTS GROUP", "ABC HOMES", "MOUNTAIN VIEW FOOD"]
        for idx, name in enumerate(companies):
            assert_that(syn_svc.regex_remove_designations(name, designation_all_regex),
                        expected[idx])

    '''
    2.- Search for prefixes followed by punctuation and a word (re/max) and set them together
    '''

    def test_regex_prefixes(self):
        companies = ["MONTESSORI PRE-SCHOOL LTD.", "HOME STAGING & RE-DESIGN INC.", "DIS-DRESS BEAD & GIFT STORE LTD"]
        expected = ["MONTESSORI PRESCHOOL LTD.", "HOME STAGING & REDESIGN INC.", "DISDRESS BEAD & GIFT STORE LTD"]
        for idx, name in enumerate(companies):
            assert_that(syn_svc.regex_prefixes(name, prefixes),
                        expected[idx])

    '''
    3.- Replace with space the following:
            A.- Word with possesive such as Reynold's
        	B.- (NO. 111),NO. 465,(LOT 111),LOT 27,LOT( 100-2),(100)
    '''

    def test_regex_numbers_lot(self):
        companies = ["REYNOLD'S HAIR SALON", "NO. 346 CATHEDRAL VENTURES LTD.", "STONEWATER VENTURES (NO. 133) LTD.",
                     "LOT 30 DESIGN STUDIO", "SAAS FEE (LOT 1) HOLDINGS INC."]
        expected = ["REYNOLD HAIR SALON", " CATHEDRAL VENTURES LTD.", "STONEWATER VENTURES  LTD.", " DESIGN STUDIO",
                    "SAAS FEE  HOLDINGS INC."]
        for idx, name in enumerate(companies):
            assert_that(syn_svc.regex_numbers_lot(name),
                        expected[idx])

    '''
    4.- Remove repeated strings with minimum two characters.
    '''

    def test_regex_repeated_strings(self):
        companies = ["LE-LA-LA PRODUCTIONS INC."]
        expected = ["LE-LA PRODUCTIONS INC."]
        for idx, name in enumerate(companies):
            assert_that(syn_svc.regex_repeated_strings(name),
                        expected[idx])

    '''
    5.- Separate ordinal numbers from words (4THGEN --> 4TH GEN):
    '''

    def test_regex_separate_ordinals(self):
        companies = ["4THGEN PHARMACIES INC.", "4THGENFALLING LTD."]
        expected = ["4TH GEN PHARMACIES INC.", "4TH GENFALLING LTD."]
        for idx, name in enumerate(companies):
            assert_that(syn_svc.regex_separated_ordinals(name, ordinal_suffixes),
                        expected[idx])

    '''
    6.- Replace with space: 
        Alphanumeric strings separating strings from letters as long as they are not in exception list (substitution list):
        For instance 1st,h20 are not separated because they are in substitution list, but P8 is transformed to P 8 
    '''

    def test_regex_keep_together_abv(self):
        companies = ["ACTIV8 RECRUITMENT", "COASTAL PURE H20", "H24 HOTEL RESORT"]
        expected = ["ACTIV8 RECRUITMENT", "COASTAL PURE H20", "H 24 HOTEL RESORT"]
        for idx, name in enumerate(companies):
            assert_that(syn_svc.regex_keep_together_abv(name, exceptions_ws),
                        expected[idx])

    '''
    7.- Replace with space:
            Punctuation including ampersand, slash, hyphen used for separation
    '''

    def test_regex_punctuation(self):
        companies = ["WESTMOUNT PLUMBING & HEATING LTD."]
        expected = ["WESTMOUNT PLUMBING   HEATING LTD."]
        for idx, name in enumerate(companies):
            assert_that(syn_svc.regex_punctuation(name),
                        expected[idx])

    '''
    8.- Replace with non-space:
        Set together letter of length one separated by spaces: (?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)
        Trailing and leading spaces in string: ^\s+|\s+$
    '''

    def test_regex_together_one_letter(self):
        companies = ["S J FENCING LTD.", "A D ALTERNATIVE SOLUTIONS LTD."]
        expected = ["SJ FENCING LTD.", "AD ALTERNATIVE SOLUTIONS LTD."]
        for idx, name in enumerate(companies):
            assert_that(syn_svc.regex_together_one_letter(name),
                        expected[idx])

    '''
    9.- Replace with non-space:
        Remove numbers and numbers in words at the beginning or keep them as long as the last string is 
        any BC|HOLDINGS|VENTURES:    
    '''

    def test_regex_numbers_standalone(self):
        companies = ["ONE TWO THREE HOLDINGS", "123 HOLDINGS", "FIRST SECOND HOLDINGS", "1ST 2ND HOLDINGS",
                     "ONE TWO THREE CANADA",
                     "123 CANADA", "FIRST SECOND THIRD CANADA", "1ST 2ND 3RD CANADA"]
        expected = ["ONE TWO HOLDINGS", "123 HOLDINGS", "FIRST SECOND HOLDINGS", "1ST 2ND HOLDINGS", " CANADA",
                    " CANADA", " CANADA", " CANADA"]
        for idx, name in enumerate(companies):
            assert_that(syn_svc.regex_numbers_standalone(name, ordinal_suffixes, numbers, stand_alone_words),
                        expected[idx])

