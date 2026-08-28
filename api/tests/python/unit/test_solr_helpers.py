import pytest
from namex.services.solr.solr_helpers import SolrHlpers
from namex.services.solr import words_to_filter_from_name


def test_name_pre_processing_ampersand_and_punctuation():
    """Verify ampersands and punctuation are normalized cleanly."""
    result = SolrHlpers._name_pre_processing("H. & H. INVESTMENTS LTD.")
    assert result == "h h investments ltd"


def test_name_pre_processing_ampersand_unspaced():
    """Verify unspaced ampersands 'H&H' normalize to 'h h'."""
    result = SolrHlpers._name_pre_processing("H&H DHILLON INVESTMENT")
    assert result == "h h dhillon investment"


def test_name_pre_processing_preserves_2letter_words():
    """Verify 2-letter words like 'AI', 'EV', 'LI' are preserved intact."""
    result = SolrHlpers._name_pre_processing("AI SOLUTIONS EV CHARGING")
    assert result == "ai solutions ev charging"


def test_conflicts_post_process_exact_match_space_insensitive():
    """Verify H. & H. INVESTMENTS LTD is classified as Exact Match for HH query."""
    mock_data = {
        'searchResults': {
            'results': [
                {'name': 'H. & H. INVESTMENTS LTD.', 'name_state': 'CORP'}
            ]
        }
    }
    query_name = SolrHlpers._get_name_without_designation(SolrHlpers._name_pre_processing("HH INVESTMENTS"))
    result = SolrHlpers._conflicts_post_process(mock_data, query_name)
    assert len(result['exactNames']) == 1
    assert result['exactNames'][0]['name'] == 'H. & H. INVESTMENTS LTD.'
