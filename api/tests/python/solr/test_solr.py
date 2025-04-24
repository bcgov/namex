import urllib

import pytest

from namex.analytics.solr import SolrQueries, SYNONYMS_PREFIX, current_app
from tests.python import integration_synonym_api


solr_name_test_data = [
    ('some name', 'somename', 'some%20name', 'some%20name%20somename'),
    (
        'a longer name jesus and the mary chain',
        'alongernamejesusandthemarychain',
        'a%20longer%20name%20jesus%20and%20the%20mary%20chain',
        'a%20longer%20name%20jesus%20and%20the%20mary%20chain%20alonger%20alongername%20longername%20longernamejesus%20namejesus%20namejesusand%20jesusand%20jesusandthe%20andthe%20andthemary%20themary%20themarychain%20marychain',
    ),
]


# setting this up as a parameterized test, maybe not needed to check permutations
# if we do / need to do a more interesting thing for the synonyms call, the parameters will be handy
@pytest.mark.parametrize('name, compresed_name, escaped_name, synonym_tokens', solr_name_test_data)
def test_get_results_query_to_solr(mocker, monkeypatch, name, compresed_name, escaped_name, synonym_tokens):
    """
    This tests the creation of the query string sent to SOLR
    as such, anything outside of that is not tested and ignored within this test
    (eg. environment variable and getting synonym from other services are mocked out)
    """
    #
    # SETUP for the test
    #

    #  patch out the calls made to get the SOLR environment variables
    def mock_env(env_name, default):
        if env_name == 'SOLR_BASE_URL':
            return 'http://not_a_real_server_just_mock'

        elif env_name == 'SOLR_SYNONYMS_API_URL':
            return 'http://not_a_real_server_just_mock'

        return default

    monkeypatch.setattr(current_app.config, 'get', mock_env)

    # patch out the call to the solr synonyms API
    def mock_synonym(name_token, stemmed_name=''):
        return True

    monkeypatch.setattr(SolrQueries, '_synonyms_exist', mock_synonym)

    # The query string that should be created in the call to the Solr API
    query = (
        'http://not_a_real_server_just_mock/solr/possible.conflicts/select?defType=edismax&hl.fl=name'
        '&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&indent=on&q='
        + compresed_name
        + '%20OR%20'
        + escaped_name
        + '&qf=name_compressed^6%20name_with_synonyms&wt=json'
        '&start=0&rows=10&fl=source,id,name,score,start_date,jurisdiction&sort=score%20desc'
        '&fq=name_with_synonyms:(' + synonym_tokens.upper() + ')'
    )

    #
    # ACTUAL TEST
    #

    # mock the urlopen call so that we can catch what is passed to it
    # in the SolrQueries get_results method
    mocker.patch('urllib.request.urlopen')
    response = SolrQueries.get_results(SolrQueries.CONFLICTS, name)
    urllib.request.urlopen.assert_called_once_with(query)


solr_get_synonym_test_data = [
    (
        "DAVE'S AUTO SERVICES LTD.",
        'dave%20%27%20s%20auto%20services%20ltd%20.%20dave%27%20dave%27s%20%27s%20%27sauto%20sauto%20sautoservices%20autoservices%20autoservicesltd%20servicesltd%20servicesltd.%20ltd.',
    ),
]


@pytest.mark.parametrize('name, expected', solr_get_synonym_test_data)
def test_solr__get_synonyms_clause(monkeypatch, name, expected):
    def mock_solr__synonyms_exist(token, col='synonyms_text'):
        return True

    monkeypatch.setattr(SolrQueries, '_synonyms_exist', mock_solr__synonyms_exist)

    syn = SolrQueries._get_synonyms_clause(name, '')

    print(syn)

    assert (SYNONYMS_PREFIX + '(' + expected + ')').upper() == syn.upper()
