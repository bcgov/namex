from namex.services.name_request.auto_analyse.name_analysis_utils import \
    data_frame_to_list, clean_name_words, regex_transform, remove_french, get_substitution_list

from hamcrest import *
import pandas as pd

text = 'WM 4MULA VENTURES INC.'
#text = 'W & M MOUNTAIN VENTURES INC.'

name = ['WM', 'MOUNTAIN', 'VENTURES']

subs_word = 'MOUNTAIN'
list_dist = ['WM', '4BY4']
list_desc = ['VENTURES']
list_none = []

stop_words = ['an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', \
              'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', \
              'such', 'that', 'the', 'their', 'then', 'there', 'these', \
              'they', 'this', 'to']
dsg_any = ['association', 'assoc', 'assoc.', 'assn', 'assn.', 'society', 'soc', \
           'soc.', 'foundation', 'co-operative', 'co-op', 'coop', 'cooperative']

dsg_end = ['llc', 'l.l.c', 'limited liability company', 'llp', 'limited liability partnership', \
           'limited partnership', 'limited', 'ltd', 'ltd.', 'incorporated', 'inc', 'inc.', \
           'corporation', 'corp', 'corp.', 'ulc.', 'ulc', 'unlimited liability company', \
           'company', 'co', 'co.', 'liability']

subs_list = [['accelerate', ' xlr8', ' xlreight'], ['access', ' axis', ' axys'], \
             ['cosi', ' cosy', ' cozi', ' cozy'], ['acqua', ' acwa', ' aqua'], \
             ['aerial', ' arial', ' ariel']]

french_desig_list = ["societe a responsabilite limitee", "societe en nom collectif a responsabilite limitee", \
                     "limitee", "ltee", "ltee.", "incorporee", "slr", "sencrl"]

data = [['WM', 'Distinctive', 12], ['079', 'Distinctive', 3], ['VENTURES', 'Descriptive', 1000]]
df = pd.DataFrame(data, columns=['word', 'word_classification', 'frequency'])

'''
def test_data_frame_to_list(client, jwt, app):
    assert_that(data_frame_to_list(df), list_dist)
    assert_that(data_frame_to_list(df), list_desc)
    assert_that(data_frame_to_list(df), list_none)
'''


def test_remove_french(client, jwt, app):
    assert_that(remove_french(text, french_desig_list), 'W & M 074 VENTURES INC.')


def test_get_substitution_list(client, jwt, app):
    assert_that(get_substitution_list(subs_word), ['mount', 'mountain', 'mt', 'mtn'])


def test_regex_transform(client, jwt, app):
    assert_that(regex_transform(text, stop_words, dsg_any, dsg_end, subs_list), 'WM 4MULA VENTURES')


def test_clean_name_words(client, jwt, app):
    assert_that(clean_name_words(text, stop_words, dsg_any, dsg_end, subs_list), 'WM 074 VENTURES')
