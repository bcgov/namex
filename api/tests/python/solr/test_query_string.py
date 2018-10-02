#
# I desperately needed tests but had no time to figure out pytest in Pycharm. It's hacked together for now, but the
# tests at least are written.
#

from namex.analytics.solr import NO_SYNONYMS_INDICATOR, NO_SYNONYMS_PREFIX, SolrQueries


def test_plain_search():
    response = SolrQueries()._get_name_copy_clause('waffle corp')
    print(response)
    assert response == ''


def test_empty_term():
    response = SolrQueries()._get_name_copy_clause('waffle ' + NO_SYNONYMS_INDICATOR + ' corp')
    print(response)
    assert response == ''


def test_empty_term_end():
    response = SolrQueries()._get_name_copy_clause('waffle corp ' + NO_SYNONYMS_INDICATOR)
    print(response)
    assert response == ''


def test_trailing_indicator():
    response = SolrQueries()._get_name_copy_clause('waffle' + NO_SYNONYMS_INDICATOR + ' corp')
    print(response)
    assert response == ''


def test_trailing_indicator_end():
    response = SolrQueries()._get_name_copy_clause('waffle corp' + NO_SYNONYMS_INDICATOR)
    print(response)
    assert response == ''


def test_one_term_first():
    response = SolrQueries()._get_name_copy_clause(NO_SYNONYMS_INDICATOR + 'waffle corp')

    assert response == NO_SYNONYMS_PREFIX + 'waffle'


def test_one_term_middle():
    response = SolrQueries()._get_name_copy_clause('big ' + NO_SYNONYMS_INDICATOR + 'waffle corp')

    assert response == NO_SYNONYMS_PREFIX + 'waffle'


def test_one_term_last():
    response = SolrQueries()._get_name_copy_clause('big corp for ' + NO_SYNONYMS_INDICATOR + 'waffle')

    assert response == NO_SYNONYMS_PREFIX + 'waffle'


def test_quoted():
    response = SolrQueries()._get_name_copy_clause('my "happy waffle"')

    assert response == ''


def test_quoted_ignore_embedded_indicator():
    response = SolrQueries()._get_name_copy_clause('my "happy ' + NO_SYNONYMS_INDICATOR + 'waffle"')

    assert response == ''


def test_indicatored_quoted():
    response = SolrQueries()._get_name_copy_clause('my ' + NO_SYNONYMS_INDICATOR + '"happy waffle"')

    assert response == NO_SYNONYMS_PREFIX + '%22happy%20waffle%22'


def test_quoted_ignore_embedded_indicator2():
    response = SolrQueries()._get_name_copy_clause('my ' + NO_SYNONYMS_INDICATOR + '"happy ' + NO_SYNONYMS_INDICATOR +
                                                   'waffle"')

    assert response == NO_SYNONYMS_PREFIX + '%22happy%20waffle%22'


# No idea how to get the tests running, so do it manually for now.
try:
    test_plain_search()
    test_empty_term()
    test_empty_term_end()
    test_trailing_indicator()
    test_trailing_indicator_end()
    test_one_term_first()
    test_one_term_middle()
    test_one_term_last()
    test_quoted()
    test_quoted_ignore_embedded_indicator()
    test_indicatored_quoted()
    test_quoted_ignore_embedded_indicator2()
except AssertionError as exception:
    pass  # (for a breakpoint)
    raise exception
