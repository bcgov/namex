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
