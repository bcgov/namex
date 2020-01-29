from namex.services.name_request.auto_analyse.name_analysis_utils import \
    read_data_frame, dataframe_to_list, clean_name_words, regex_transform, substitution_list, remove_french

from hamcrest import *
text = 'W & M 074 VENTURES INC.'

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


#def test_read_data_frame(client, jwt, app):
    #    read_data_frame()
#    pass


#def test_dataframe_to_list(client, jwt, app):
    # dataframe_to_list()
#    pass


def test_clean_name_words(client, jwt, app):
    #name=clean_name_words(text, stop_words, dsg_any, dsg_end)
    assert_that (clean_name_words(text, stop_words, dsg_any, dsg_end), 'WM 074 VENTURES')

'''
def test_regex_transform(client, jwt, app):
    regex_transform(text, dsg_any, dsg_end)
    pass


def test_substitution_list(client, jwt, app):
    substitution_list(text, subs_list, stop_words)
    pass


def test_remove_french(client, jwt, app):
    remove_french(text, french_desig_list)
    pass
'''