"""Unit tests for possible-conflicts query preprocessing."""

from unittest.mock import patch

from namex.services.solr.solr_client import SolrClient
from namex.services.solr.solr_helpers import SolrHlpers


def test_possible_conflicts_sends_raw_query_to_solr():
    """Skip words stay in the Solr payload so ranking/boosts can see BE KIND."""
    captured = {}

    def fake_get_possible_conflicts(name, start=0, rows=100, exact_phrase=''):
        captured['name'] = name
        return {'searchResults': {'results': []}}

    with patch.object(SolrClient, 'get_possible_conflicts', fake_get_possible_conflicts):
        SolrHlpers.get_possible_conflicts('be kind')

    assert captured['name'] == 'be kind'


def test_possible_conflicts_exact_match_still_uses_stripped_query():
    """Exact Match comparison still drops skip words (BE) and designations (LTD)."""
    results = {
        'searchResults': {
            'results': [
                {
                    'name': 'KIND INC.',
                    'name_state': 'CORP',
                    'highlighting': {},
                },
                {
                    'name': 'BE KIND CONTRACTING LTD.',
                    'name_state': 'CORP',
                    'highlighting': {'exact': ['KIND']},
                },
            ]
        }
    }

    with patch.object(SolrClient, 'get_possible_conflicts', return_value=results):
        payload = SolrHlpers.get_possible_conflicts('be kind')

    exact_names = [item['name'] for item in payload['exactNames']]
    similar_names = [item['name'] for item in payload['names']]
    assert 'KIND INC.' in exact_names
    assert 'BE KIND CONTRACTING LTD.' in similar_names
    assert 'BE KIND CONTRACTING LTD.' not in exact_names
