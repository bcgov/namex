#
# Pytests for checking the code that produces the more intricate components of the Solr query string.
#
import string
from urllib import parse

import pytest

from namex.analytics.solr import NO_SYNONYMS_INDICATOR, NO_SYNONYMS_PREFIX, RESERVED_CHARACTERS, SolrQueries

compress_name_test_data = [
    ('Waffle Mania', 'wafflemania'),
    (' Waffle Mania', 'wafflemania'),
    ('Waffle Mania ', 'wafflemania'),
    ('  Waffle   Mania  ', 'wafflemania'),
    ('waffle mania inc.', 'wafflemania'),
    ('waffle mania inc. ', 'wafflemania'),
    ('waffle @mania inc.', 'wafflemania'),
    ('@waffle mania inc.', 'wafflemania'),
    ('waffle mania 123', 'wafflemania'),
    ('waffle a.b.c. ltd.', 'waffleabc'),
    ('i have ulcers', 'ihaveulcers'),  # ULC designation
    ('waffle mania inc. / le wafflemania inc.', 'wafflemanialewafflemania'),
]


@pytest.mark.parametrize('name,expected', compress_name_test_data)
def test_compress_name(name, expected):
    response = SolrQueries._compress_name(name)

    assert expected == response


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
    (
        'my ' + NO_SYNONYMS_INDICATOR + '"happy ' + NO_SYNONYMS_INDICATOR + 'waffle"',
        NO_SYNONYMS_PREFIX + '(%22happy%20waffle%22)',
    ),
]


@pytest.mark.parametrize('search_string,expected', name_copy_test_data)
def test_get_name_copy_clause(search_string, expected):
    response = SolrQueries._get_name_copy_clause(search_string)

    assert expected == response


name_tokenize_data = [
    ('three tokens', ['three', ' ', 'tokens']),
    (
        'skinny garçon "puppy-records" ®',
        ['skinny', ' ', 'gar', 'ç', 'on', ' ', '"', 'puppy', '-', 'records', '"', ' ', '®'],
    ),
    ('skinny "puppy-records" ®', ['skinny', ' ', '"', 'puppy', '-', 'records', '"', ' ', '®']),
    ('waffle', ['waffle']),
    (' waffle', [' ', 'waffle']),
    ('waffle ', ['waffle', ' ']),
    ('waffle mania', ['waffle', ' ', 'mania']),
    (' waffle mania', [' ', 'waffle', ' ', 'mania']),
    ('waffle mania ', ['waffle', ' ', 'mania', ' ']),
    ("dave's auto services ltd.", ['dave', "'", 's', ' ', 'auto', ' ', 'services', ' ', 'ltd', '.']),
]


@pytest.mark.parametrize('name_string, expected', name_tokenize_data)
def test_tokenz(name_string, expected):
    response = SolrQueries._tokenize(
        name_string, [string.digits, string.whitespace, RESERVED_CHARACTERS, string.punctuation, string.ascii_lowercase]
    )

    assert expected == response


name_parse_data = [
    (
        ['skinny', ' ', '"', 'puppy', '-', 'records', '"'],
        ['skinny', 'puppy', 'records', 'skinnypuppy', 'skinnypuppyrecords', 'puppyrecords'],
    ),
    (['skinny', ' ', '-', '"', 'records', '"'], ['skinny']),
    (
        ['skinny', ' ', '"', 'puppy', ' ', 'records', '"'],
        ['skinny', 'puppy', 'records', 'skinnypuppy', 'skinnypuppyrecords', 'puppyrecords'],
    ),
    (
        ['skinny', ' ', '"', 'puppy', '-', 'records', '"'],
        ['skinny', 'puppy', 'records', 'skinnypuppy', 'skinnypuppyrecords', 'puppyrecords'],
    ),
    (
        ['skinny', ' ', 'puppy', '-', 'records'],
        ['skinny', 'puppy', 'records', 'skinnypuppy', 'skinnypuppyrecords', 'puppyrecords'],
    ),
    (['skinny', ' ', 'puppy', ' ', '-', 'records'], ['skinny', 'puppy', 'skinnypuppy']),
    (['skinny', ' ', '@', 'puppy'], ['skinny']),
    (['skinny', ' ', '@', '"', 'puppy', ' ', 'records', '"'], ['skinny']),
    (['skinny', ' ', '@', '"', 'puppy', '-', 'records', '"'], ['skinny']),
    (['skinny', ' ', '@', '"', 'puppy', ' ', 'records', '"', 'chain'], ['skinny', 'chain', 'skinnychain']),
    (
        ['skinny', ' ', '@', ' ', '"', 'puppy', '-', 'records', '"'],
        ['skinny', 'puppy', 'records', 'skinnypuppy', 'skinnypuppyrecords', 'puppyrecords'],
    ),
]


@pytest.mark.parametrize('tokens, expected', name_parse_data)
def test_parse_for_synonym_candidates(tokens, expected):
    synonym_candidates = SolrQueries._parse_for_synonym_candidates(tokens)

    print(synonym_candidates)

    assert expected == synonym_candidates


@pytest.mark.parametrize(
    'search_value, expected_solr_query, expected_nr_number, expected_nr_name',
    [
        (None, '*:*', None, None),
        ('test name one', '(name_copy:*test* AND name_copy:*name* AND name_copy:*one*)', None, 'test name one'),
        ('1234567', 'nr_num:*1234567* OR (name_copy:*1234567*)', '1234567', '1234567'),
        ('nr1234567', 'nr_num:*1234567*', '1234567', ''),
        ('nr 1234567', 'nr_num:*1234567*', '1234567', ''),
        ('NR1234567', 'nr_num:*1234567*', '1234567', ''),
        ('NR 1234567', 'nr_num:*1234567*', '1234567', ''),
        ('NR123 test one', 'nr_num:*123* AND (name_copy:*test* AND name_copy:*one*)', '123', 'test one'),
        ('test 123 one', '(name_copy:*test* AND name_copy:*123* AND name_copy:*one*)', None, 'test 123 one'),
        (
            '123 test on',
            'nr_num:*123* OR (name_copy:*123* AND name_copy:*test* AND name_copy:*on*)',
            '123',
            '123 test on',
        ),
    ],
)
def test_get_parsed_query_name_nr_search(search_value, expected_solr_query, expected_nr_number, expected_nr_name):
    solr_query, nr_number, nr_name = SolrQueries.get_parsed_query_name_nr_search(search_value)
    assert expected_solr_query == parse.unquote(solr_query)
    assert expected_nr_number == nr_number
    assert expected_nr_name == nr_name
