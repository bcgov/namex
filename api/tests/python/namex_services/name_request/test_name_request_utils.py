from namex.services.name_request.auto_analyse.name_analysis_utils import \
    data_frame_to_list, clean_name_words, regex_transform, remove_french, get_substitution_list, get_stop_word_list, \
    get_prefix_list, get_en_designation_any_list, get_en_designation_end_list, get_fr_designation_end_list, \
    get_stand_alone_list, is_substitution_word, get_classification

from hamcrest import *
import pandas as pd

text = 'WM H20 VENTURES INC'
# text = 'W & M MOUNTAIN VENTURES INC.'
word = 'MOUNTAIN'

name = ['WM', 'MOUNTAIN', 'VENTURES']

substitution_word = '4mula'
list_dist = []
list_desc = []
list_none = ['MOUNTAIN','VIEW','FOOD','GROWERS']

stop_words = ['an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', \
              'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', \
              'such', 'that', 'the', 'their', 'then', 'there', 'these', \
              'they', 'this', 'to']
en_designation_any_list = ['association', 'assoc', 'assoc.', 'assn', 'assn.', 'society', 'soc', \
                           'soc.', 'foundation', 'co-operative', 'co-op', 'coop', 'cooperative']

en_designation_end_list = ['llc', 'l.l.c', 'limited liability company', 'llp', 'limited liability partnership', \
                           'limited partnership', 'limited', 'ltd', 'ltd.', 'incorporated', 'inc', 'inc.', \
                           'corporation', 'corp', 'corp.', 'ulc.', 'ulc', 'unlimited liability company', \
                           'company', 'co', 'co.', 'liability']

fr_designation_end_list = ['ltee', 'ltee.', 'incorporee', ' societe a responsabilite limitee', \
                           'societe en nom collectif a responsabilite limitee', 'slr', 'sencrl', \
                           'limitee', 'incorporee']

stand_alone_list = ['bc', 'holdings', 'ventures', 'solutions', 'enterprise', 'industries']

prefix_list = ['un', 're', 'in', 'dis', 'en', 'non', 'in', 'over', 'mis', 'sub', 'pre', 'inter', 'fore', 'de', 'trans', \
               'super', 'semi', 'anti', 'mid', 'under', 'ante', 'bene', 'circum', 'co', 'com', 'con', 'col', 'dia', \
               'ex', 'homo', 'hyper', 'mal', 'micro', 'multi', 'para', 'poly', 'post', 'pro', 'retro', 'tele', \
               'therm', 'trans', 'uni']

data = [['WM', 'distinctive', 12], ['079', 'distinctive', 3], ['VENTURES', 'descriptive', 1000]]
df = pd.DataFrame(data, columns=['word', 'word_classification', 'frequency'])


def test_data_frame_to_list(client, jwt, app):
    assert_that(data_frame_to_list(df), list_dist)
    assert_that(data_frame_to_list(df), list_desc)
    assert_that(data_frame_to_list(df), list_none)


def test_remove_french(client, jwt, app):
    assert_that(remove_french(text, fr_designation_end_list), 'W & M 074 VENTURES INC.')


def test_get_substitution_list(client, jwt, app):
    assert_that(get_substitution_list(substitution_word), ['mount', 'mountain', 'mt', 'mtn'])


def test_is_substitution_word(client, jwt, app):
    assert_that(is_substitution_word(substitution_word), True)


def test_get_stop_word_list(client, jwt, app):
    assert_that(get_stop_word_list(), stop_words)


def test_get_prefix_list(client, jwt, app):
    assert_that(get_prefix_list(), prefix_list)


def test_get_en_designation_any_list(client, jwt, app):
    assert_that(get_en_designation_any_list(), en_designation_any_list)


def test_get_en_designation_end_list(client, jwt, app):
    assert_that(get_en_designation_end_list(), en_designation_end_list)


def test_get_fr_designation_end_list(client, jwt, app):
    assert_that(get_fr_designation_end_list(), fr_designation_end_list)


def test_get_stand_alone_list(client, jwt, app):
    assert_that(get_stand_alone_list(), stand_alone_list)


def test_get_classification(client, jwt, app):
    assert_that(get_classification(word), 'none')


def test_regex_transform(client, jwt, app):
    assert_that(regex_transform(text, en_designation_any_list, en_designation_end_list, prefix_list), 'WM H VENTURES')


def test_clean_name_words(client, jwt, app):
    assert_that(clean_name_words(text, stop_words, en_designation_any_list, en_designation_end_list, fr_designation_end_list, \
                                 prefix_list), 'WM 074 VENTURES')
