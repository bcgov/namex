"""Unit tests for possible-conflicts query preprocessing."""

from unittest.mock import Mock, patch

from namex.services.solr.solr_client import SolrClient
from namex.services.solr.solr_helpers import SolrHlpers


def test_possible_conflicts_sends_raw_query_to_solr():
    """Skip words stay in the Solr payload so ranking/boosts can see BE KIND."""
    captured = {}

    def fake_get_possible_conflicts(name, start=0, rows=100, exact_phrase='', distinctive='', descriptive=''):
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


def _sent_query(**kwargs):
    """Return the query SolrClient sends to namex-solr-api for these arguments."""
    resp = Mock(status_code=200)
    resp.json.return_value = {'searchResults': {'results': []}}
    with (
        patch.object(SolrClient, '_get_bearer_token', return_value='token'),
        patch.object(SolrClient, '_get_solr_api_url', return_value='http://solr-api'),
        patch('namex.services.solr.solr_client.requests.post', return_value=resp) as post,
    ):
        SolrClient.get_possible_conflicts('british columbia deconstructionists', **kwargs)
    return post.call_args.kwargs['json']['query']


def test_name_search_query_has_no_distinctive():
    """A plain Name Search sends no distinctive or descriptive terms."""
    assert _sent_query() == {'value': 'british columbia deconstructionists'}


def test_distinctive_and_descriptive_are_passed_to_solr_api():
    assert _sent_query(distinctive='british columbia', descriptive='deconstructionists') == {
        'value': 'british columbia deconstructionists',
        'distinctive': 'british columbia',
        'descriptive': 'deconstructionists',
    }
