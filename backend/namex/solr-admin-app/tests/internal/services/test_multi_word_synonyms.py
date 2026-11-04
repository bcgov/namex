from solr_admin.services.get_multi_word_synonyms import get_multi_word_synonyms
from hamcrest import *

def test_multi_word_synonym():
    synonym_list = 'me, hello world, hello again, stop'

    # split on ','
    values = synonym_list.split(',')

    # Strip leading and trailing spaces.
    values = list(map(str.strip, values))

    disallowed_values = get_multi_word_synonyms(values)

    assert_that(disallowed_values[0], equal_to('hello world'))
    assert_that(disallowed_values[1], equal_to('hello again'))
