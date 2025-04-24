import json
import os
import urllib

import pytest
import requests

from namex.models import User
from tests.python import integration_solr

token_header = {'alg': 'RS256', 'typ': 'JWT', 'kid': 'flask-jwt-oidc-test-client'}
claims = {
    'iss': 'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc',
    'sub': '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
    'aud': 'NameX-Dev',
    'exp': 31531718745,
    'iat': 1531718745,
    'jti': 'flask-jwt-oidc-test-support',
    'typ': 'Bearer',
    'username': 'test-user',
    'realm_access': {'roles': ['{}'.format(User.EDITOR), '{}'.format(User.APPROVER), 'viewer', 'user']},
}
SOLR_URL = os.getenv('SOLR_TEST_URL')


@pytest.fixture(scope='session', autouse=True)
def reload_schema(request):
    url = SOLR_URL + '/solr/admin/cores?action=RELOAD&core=possible.conflicts&wt=json'
    r = requests.get(url)

    assert r.status_code == 200


@integration_solr
def test_solr_available(app, client, jwt):
    url = SOLR_URL + '/solr/possible.conflicts/admin/ping'
    r = requests.get(url)

    assert r.status_code == 200


def clean_database(client, jwt):
    url = SOLR_URL + '/solr/possible.conflicts/update?commit=true'
    headers = {'content-type': 'text/xml'}
    data = '<delete><query>id:*</query></delete>'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200


def seed_database_with(client, jwt, name, id='1', source='2'):
    clean_database(client, jwt)
    url = SOLR_URL + '/solr/possible.conflicts/update?commit=true'
    headers = {'content-type': 'application/json'}
    data = '[{"source":"' + source + '", "name":"' + name + '", "id":"' + id + '"}]'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200


def verify(data, expected):
    print(data['names'])

    assert expected == data['names']


def verify_exact_match_results(client, jwt, query, expected):
    data = search_exact_match(client, jwt, query)
    verify(data, expected)


def verify_exact_match(client, jwt, query, expected):
    data = search_exact_match(client, jwt, query)
    expect = [{'name': expected, 'id': '1', 'source': '2'}]
    if expected == None:
        expect = []
    verify(data, expect)


def search_exact_match(client, jwt, query):
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    url = '/api/v1/exact-match?query=' + urllib.parse.quote(query)
    print(url)
    rv = client.get(url, headers=headers)

    assert rv.status_code == 200
    return json.loads(rv.data)


@integration_solr
def test_find_same_name(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt, query='JM Van Damme inc', expected='JM Van Damme inc')


@integration_solr
def test_resist_empty(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt, query='', expected=None)


@integration_solr
def test_resists_different_type(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt, query='JM Van Damme ltd', expected='JM Van Damme inc')


@integration_solr
def test_case_insensitive(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt, query='JM VAN DAMME INC', expected='JM Van Damme inc')


@integration_solr
def test_no_match(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt, query='Hello BC inc', expected=None)


@integration_solr
def test_ignores_and(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt, query='J and M Van Damme inc', expected='JM Van Damme inc')


@integration_solr
def test_ignores_dots(client, jwt, app):
    seed_database_with(client, jwt, 'J.M. Van Damme Inc')
    verify_exact_match(client, jwt, query='JM Van Damme Inc', expected='J.M. Van Damme Inc')


@integration_solr
def test_ignores_ampersand(client, jwt, app):
    seed_database_with(client, jwt, 'J&M & Van Damme Inc')
    verify_exact_match(client, jwt, query='JM Van Damme Inc', expected='J&M & Van Damme Inc')


@integration_solr
def test_ignores_comma(client, jwt, app):
    seed_database_with(client, jwt, 'JM, Van Damme Inc')
    verify_exact_match(client, jwt, query='JM Van Damme Inc', expected='JM, Van Damme Inc')


@integration_solr
def test_ignores_exclamation_mark(client, jwt, app):
    seed_database_with(client, jwt, 'JM! Van Damme Inc')
    verify_exact_match(client, jwt, query='JM Van Damme Inc', expected='JM! Van Damme Inc')


@integration_solr
def test_no_match_because_additional_initial(client, jwt, app):
    seed_database_with(client, jwt, 'J.M.J. Van Damme Trucking Inc')
    verify_exact_match(client, jwt, query='J.M. Van Damme Trucking Inc', expected=None)


@integration_solr
def test_no_match_because_additional_word(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme Trucking Inc')
    verify_exact_match(client, jwt, query='JM Van Damme Trucking International Inc', expected=None)


@integration_solr
def test_no_match_because_missing_one_word(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme Physio inc')
    verify_exact_match(client, jwt, query='JM Van Damme inc', expected=None)


@integration_solr
def test_no_match_star(client, jwt, app):
    seed_database_with(client, jwt, 'SCHOLARSHIP')
    verify_exact_match(client, jwt, query='SCHOL*', expected=None)


@integration_solr
def test_duplicated_letters(client, jwt, app):
    seed_database_with(client, jwt, 'Damme Trucking Inc')
    verify_exact_match(client, jwt, query='Dame Trucking Inc', expected='Damme Trucking Inc')


@integration_solr
def test_entity_suffixes(client, jwt, app):
    suffixes = [
        'limited',
        'ltd.',
        'ltd',
        'incorporated',
        'inc',
        'inc.',
        'corporation',
        'corp.',
        'limitee',
        'ltee',
        'incorporee',
        'llc',
        'l.l.c.',
        'limited liability company',
        'limited liability co.',
        'llp',
        'limited liability partnership',
        'societe a responsabilite limitee',
        'societe en nom collectif a responsabilite limitee',
        'srl',
        'sencrl',
        'ulc',
        'unlimited liability company',
        'association',
        'assoc',
        'assoc.',
        'assn',
        'co',
        'co.',
        'society',
        'soc',
        'soc.',
    ]
    for suffix in suffixes:
        seed_database_with(client, jwt, 'Van Trucking ' + suffix)
        verify_exact_match(client, jwt, query='Van Trucking', expected='Van Trucking ' + suffix)


@integration_solr
def test_numbers_preserved(client, jwt, app):
    seed_database_with(client, jwt, 'Van 4 Trucking Inc')
    verify_exact_match(client, jwt, query='Van 4 Trucking ltd', expected='Van 4 Trucking Inc')


@integration_solr
@pytest.mark.parametrize(
    'criteria, seed',
    [
        ('J M HOLDINGS', 'J M HOLDINGS INC'),
        ('JM Van Damme Inc', 'J&M & Van Damme Inc'),
        ('J&M HOLDINGS', 'JM HOLDINGS INC'),
        ('J. & M. HOLDINGS', 'JM HOLDINGS INC'),
        ('J and M HOLDINGS', 'J and M HOLDINGS'),
        ('J AND M HOLDINGS', 'J AND M HOLDINGS'),
        ('J or M HOLDINGS', 'J. & M. HOLDINGS'),
        ('J-M HOLDINGS', 'J. & M. HOLDINGS'),
        ("J'M HOLDINGS", 'J. & M. HOLDINGS'),
        ('J_M HOLDINGS', 'J. & M. HOLDINGS'),
        ("J_'_-M HOLDINGS", 'J. & M. HOLDINGS'),
        ('J@M HOLDINGS', 'J. & M. HOLDINGS'),
        ('J=M HOLDINGS', 'J. & M. HOLDINGS'),
        ('J!M HOLDINGS', 'J. & M. HOLDINGS'),
        ('J!=@_M HOLDINGS', 'J. & M. HOLDINGS'),
        ('J+M HOLDINGS', 'J. & M. HOLDINGS'),
        (r'J\M HOLDINGS', 'J. & M. HOLDINGS'),
        ('GREAT NORTH OIL AND GAS LIMITED', 'GREAT NORTH OIL AND GAS LIMITED'),
    ],
)
def test_explore_complex_cases(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_exact_match(client, jwt, query=criteria, expected=seed)


@integration_solr
def test_returns_all_fields_that_we_need(client, jwt, app):
    seed_database_with(client, jwt, 'Van Trucking Inc', 'any-id', 'any-source')
    verify_exact_match_results(
        client,
        jwt,
        query='Van Trucking ltd',
        expected=[{'name': 'Van Trucking Inc', 'id': 'any-id', 'source': 'any-source'}],
    )


@pytest.mark.skip(reason='dont know how to make solr handle those scenarios')
@integration_solr
@pytest.mark.parametrize(
    'criteria, seed',
    [
        ('{JM} HOLDINGS', 'J. & M. HOLDINGS'),
        ('[JM] HOLDINGS', 'J. & M. HOLDINGS'),
        ('(JM) HOLDINGS', 'J.M HOLDINGS'),
        ('J^M HOLDINGS', 'J. & M. HOLDINGS'),
        ('J~M HOLDINGS', 'J. & M. HOLDINGS'),
        ('J*M HOLDINGS', 'J. & M. HOLDINGS'),
        ('J:M HOLDINGS', 'J. & M. HOLDINGS'),
        ('J?M HOLDINGS', 'J. & M. HOLDINGS'),
    ],
)
def test_special_characters(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_exact_match(client, jwt, query=criteria, expected=seed)
