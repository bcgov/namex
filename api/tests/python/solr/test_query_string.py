#
# Pytests for checking the code that produces the more intricate components of the Solr query string.
#

import pytest

from namex.analytics.solr import NO_SYNONYMS_INDICATOR, NO_SYNONYMS_PREFIX, SolrQueries


compress_name_test_data = [
    ('Waffle Mania', 'wafflemania'),
    (' Waffle Mania', 'wafflemania'),
    ('Waffle Mania ', 'wafflemania'),
    ('  Waffle   Mania  ', 'wafflemania'),
    ('waffle mania inc.', 'wafflemania'),
    ('waffle @mania inc.', 'wafflemania'),
    ('@waffle mania inc.', 'wafflemania'),
    ('waffle mania 123', 'wafflemania'),
    ('waffle a.b.c. ltd.', 'waffleabc'),
#    ('i have ulcers', 'ihaveulcers')  # ULC designation
]

tokenize_name_test_data = [
    ('waffle', ['waffle']),
    (' waffle', ['waffle']),
    ('waffle ', ['waffle']),
    ('waffle mania', ['waffle', 'mania']),
    (' waffle mania', ['waffle', 'mania']),
    ('waffle mania ', ['waffle', 'mania']),
    ('   waffle   mania   ', ['waffle', 'mania']),
    ('-waffle mania', ['mania']),
    ('waffle -mania', ['waffle']),
    ('waffle "mania inc"', ['waffle', 'mania inc']),
    ('waffle -"mania inc"', ['waffle']),
    ('   waffle     -"   mania    inc   "    ', ['waffle']),
]

name_copy_test_data = [
    ('waffle corp', ''),
    ('waffle ' + NO_SYNONYMS_INDICATOR + ' corp', ''),
    ('waffle corp ' + NO_SYNONYMS_INDICATOR, ''),
    ('waffle' + NO_SYNONYMS_INDICATOR + ' corp', ''),
    ('waffle corp' + NO_SYNONYMS_INDICATOR, ''),
    ('waffle' + NO_SYNONYMS_INDICATOR + 'corp', NO_SYNONYMS_PREFIX + '(corp)'),
    ('the waffle' + NO_SYNONYMS_INDICATOR + 'corp', NO_SYNONYMS_PREFIX + '(corp)'),
    (NO_SYNONYMS_INDICATOR + '^corp!', NO_SYNONYMS_PREFIX + '(%5Ecorp%21)'),
    (NO_SYNONYMS_INDICATOR + 'waffle corp', NO_SYNONYMS_PREFIX + '(waffle)'),
    ('big ' + NO_SYNONYMS_INDICATOR + 'waffle corp', NO_SYNONYMS_PREFIX + '(waffle)'),
    ('big corp for ' + NO_SYNONYMS_INDICATOR + 'waffle', NO_SYNONYMS_PREFIX + '(waffle)'),
    ('my "happy waffle"', ''),
    ('my "happy ' + NO_SYNONYMS_INDICATOR + 'waffle"', ''),
    ('my ' + NO_SYNONYMS_INDICATOR + '"happy waffle"', NO_SYNONYMS_PREFIX + '(%22happy%20waffle%22)'),
    ('my ' + NO_SYNONYMS_INDICATOR + '"happy ' + NO_SYNONYMS_INDICATOR + 'waffle"', NO_SYNONYMS_PREFIX +
        '(%22happy%20waffle%22)')
]


@pytest.mark.parametrize("name,expected", compress_name_test_data)
def test_compress_name(name, expected):
    response = SolrQueries()._compress_name(name)

    assert expected == response


@pytest.mark.parametrize("search_string,expected", tokenize_name_test_data)
def test_tokenize_name(search_string, expected):
    response = SolrQueries()._tokenize_name(search_string)

    assert expected == response


@pytest.mark.parametrize("search_string,expected", name_copy_test_data)
def test_get_name_copy_clause(search_string, expected):
    response = SolrQueries()._get_name_copy_clause(search_string)

    assert expected == response
