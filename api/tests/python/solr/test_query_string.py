#
# Pytests for checking the code that produces the "name_copy" portion of the Solr query string.
#

import pytest

from namex.analytics.solr import NO_SYNONYMS_INDICATOR, NO_SYNONYMS_PREFIX, SolrQueries


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


@pytest.mark.parametrize("search_string,expected", name_copy_test_data)
def test_get_name_copy_clause(search_string, expected):
    response = SolrQueries()._get_name_copy_clause(search_string)

    assert response == expected
