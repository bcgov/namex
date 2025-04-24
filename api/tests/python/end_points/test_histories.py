import json
import os

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
    url = SOLR_URL + '/solr/admin/cores?action=RELOAD&core=names&wt=json'
    r = requests.get(url)

    assert r.status_code == 200


@integration_solr
def test_solr_available(app, client, jwt):
    url = SOLR_URL + '/solr/names/admin/ping'
    r = requests.get(url)

    assert r.status_code == 200


def clean_database(client, jwt):
    url = SOLR_URL + '/solr/names/update?commit=true'
    headers = {'content-type': 'text/xml'}
    data = '<delete><query>id:*</query></delete>'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200


def seed_database_with(client, jwt, name, id='1', name_state_type_cd='A', submit_count='1', nr_num='NR 12345'):
    clean_database(client, jwt)
    url = SOLR_URL + '/solr/names/update?commit=true'
    headers = {'content-type': 'application/json'}
    data = (
        '[{"name":"'
        + name
        + '", "id":"'
        + id
        + '", "name_state_type_cd":"'
        + name_state_type_cd
        + '", "submit_count":"'
        + submit_count
        + '", "nr_num":"'
        + nr_num
        + '"}]'
    )

    r = requests.post(url, headers=headers, data=data)
    assert r.status_code == 200


def verify(data, expected):
    assert expected == data


def verify_same_or_similar(client, jwt, query, expected):
    data = search_histories(client, jwt, query)
    result = None
    if len(data['names']) > 0:
        result = data['names'][0]['name']

    verify(result, expected)


def extract_list_of_values_for_key(array_of_dictionaries, key):
    values = []

    for dictionary in array_of_dictionaries:
        for k in dictionary:
            if k == key:
                values.append(dictionary[k])
                break

    return values


def search_histories(client, jwt, query):
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    url = '/api/v1/documents:histories'

    content = {'type': 'plain_text', 'content': query}
    rv = client.post(url, data=json.dumps(content), headers=headers)

    assert rv.status_code == 200
    return json.loads(rv.data)


@integration_solr
def test_find_same_name(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_same_or_similar(client, jwt, query='JM Van Damme inc', expected='JM Van Damme inc')


@integration_solr
def test_resists_different_type(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_same_or_similar(client, jwt, query='JM Van Damme ltd', expected='JM Van Damme inc')


@integration_solr
def test_case_insensitive(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_same_or_similar(client, jwt, query='JM VAN DAMME INC', expected='JM Van Damme inc')


@integration_solr
def test_no_match(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_same_or_similar(client, jwt, query='Hello BC inc', expected=None)


@integration_solr
def test_ignores_and(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_same_or_similar(client, jwt, query='J and M Van Damme inc', expected='JM Van Damme inc')


@integration_solr
def test_ignores_dots(client, jwt, app):
    seed_database_with(client, jwt, 'J.M. Van Damme Inc')
    verify_same_or_similar(client, jwt, query='JM Van Damme Inc', expected='J.M. Van Damme Inc')


@integration_solr
def test_ignores_ampersand(client, jwt, app):
    seed_database_with(client, jwt, 'J&M & Van Damme Inc')
    verify_same_or_similar(client, jwt, query='JM Van Damme Inc', expected='J&M & Van Damme Inc')


@integration_solr
def test_ignores_comma(client, jwt, app):
    seed_database_with(client, jwt, 'JM, Van Damme Inc')
    verify_same_or_similar(client, jwt, query='JM Van Damme Inc', expected='JM, Van Damme Inc')


@integration_solr
def test_ignores_exclamation_mark(client, jwt, app):
    seed_database_with(client, jwt, 'JM! Van Damme Inc')
    verify_same_or_similar(client, jwt, query='JM Van Damme Inc', expected='JM! Van Damme Inc')


@integration_solr
def test_no_match_because_additional_initial(client, jwt, app):
    seed_database_with(client, jwt, 'J.M.J. Van Damme Trucking Inc')
    verify_same_or_similar(client, jwt, query='J.M. Van Damme Trucking Inc', expected=None)


@integration_solr
def test_no_match_because_additional_word(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme Trucking Inc')
    verify_same_or_similar(client, jwt, query='JM Van Damme Trucking International Inc', expected=None)


@integration_solr
def test_no_match_because_missing_one_word(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme Physio inc')
    verify_same_or_similar(client, jwt, query='JM Van Damme inc', expected=None)


@integration_solr
def test_no_match_star(client, jwt, app):
    seed_database_with(client, jwt, 'SCHOLARSHIP')
    verify_same_or_similar(client, jwt, query='SCHOL*', expected=None)


@integration_solr
def test_no_match_because_stemmed_word(client, jwt, app):
    seed_database_with(client, jwt, 'GREAT NORTH OIL AND GAS LIMITED')
    verify_same_or_similar(client, jwt, query='GREAT NORTHERN OIL AND GAS LIMITED', expected=None)


@integration_solr
def test_duplicated_letters(client, jwt, app):
    seed_database_with(client, jwt, 'Damme Trucking Inc')
    verify_same_or_similar(client, jwt, query='Dame Trucking Inc', expected='Damme Trucking Inc')


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
        verify_same_or_similar(client, jwt, query='Van Trucking', expected='Van Trucking ' + suffix)


@integration_solr
def test_numbers_preserved(client, jwt, app):
    seed_database_with(client, jwt, 'Van 4 Trucking Inc')
    verify_same_or_similar(client, jwt, query='Van 4 Trucking ltd', expected='Van 4 Trucking Inc')


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
        ('JM HOLDINGS', 'J   \t \r M HOLDINGS INC'),
        ('J AND M Van AND Damme Inc', 'JM Van Damme Ltd'),
        ("J&M's HOLDINGS", 'JM HOLDINGS INC'),
        ('J. M. HOLDINGS', 'JM HOLDINGS INC'),
        ('J OR M HOLDINGS', 'J AND M HOLDINGS'),
        ('J AND M HOLDINGS', "J's AND M's HOLDINGS"),
        (
            "J's AND M's HOLDINGS",
            'J AND M HOLDINGS',
        ),
        ('J OR M HOLDINGS', 'JJM HOLDINGS'),
        ('JM HOLDINGS', 'JJJ AND MMMM HOLDINGS'),
        ('JVD HOLDINGS', 'J V D++ HOLDINGS'),
    ],
)
def test_explore_complex_cases(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_same_or_similar(client, jwt, query=criteria, expected=seed)


@integration_solr
def test_multiple_similar_results_cases(client, jwt, app):
    clean_database(client, jwt)
    url = SOLR_URL + '/solr/names/update?commit=true'
    headers = {'content-type': 'application/json'}
    data = [
        {'name': 'J.J. TRUCKING', 'id': '7', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 1'},
        {
            'name': "J.J.'s TRUCKING INCORPORATED",
            'id': '8',
            'name_state_type_cd': 'R',
            'submit_count': '1',
            'nr_num': 'NR 2',
        },
        {'name': 'J & J TRUCKING LTD', 'id': '9', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 3'},
        {'name': 'JJ TRUCKING LTD', 'id': '10', 'name_state_type_cd': 'A', 'submit_count': '1', 'nr_num': 'NR 10002'},
        {'name': 'J OR J TRUCKING INC', 'id': '11', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 4'},
        {'name': "J J'S TRUCKING LTD", 'id': '12', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 5'},
        {'name': 'J&J TRUCKING LLC', 'id': '13', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 10007'},
        {'name': "J&J's TRUCKING INC", 'id': '14', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 6'},
        {'name': "JJ's TRUCKING LTD", 'id': '15', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 12346'},
        {'name': 'J. J. TRUCKING LTD', 'id': '16', 'name_state_type_cd': 'A', 'submit_count': '1', 'nr_num': 'NR 8'},
        {'name': "J & J's TRUCKING INC", 'id': '17', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 9'},
        {'name': "J and J'S TRUCKING LTD", 'id': '18', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': '5'},
        {'name': 'J-J TRUCKING LTD', 'id': '19', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 12347'},
        {'name': 'J. and J. TRUCKING LTD', 'id': '20', 'name_state_type_cd': 'A', 'submit_count': '1', 'nr_num': '11'},
        {
            'name': "J's and J's TRUCKING INC",
            'id': '21',
            'name_state_type_cd': 'R',
            'submit_count': '1',
            'nr_num': '12',
        },
        {'name': "J-J'S TRUCKING LTD", 'id': '22', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 13'},
        {
            'name': "J 'n' J'S TRUCKING LTD",
            'id': '23',
            'name_state_type_cd': 'R',
            'submit_count': '1',
            'nr_num': 'NR 14',
        },
    ]

    r = requests.post(url, headers=headers, data=json.dumps(data))
    assert r.status_code == 200

    result = extract_list_of_values_for_key(search_histories(client, jwt, 'J J TRUCKING LTD')['names'], 'name')
    assert result
    assert len(result) == len(data)


@integration_solr
def test_multiletter_similar_results_cases(client, jwt, app):
    clean_database(client, jwt)
    url = SOLR_URL + '/solr/names/update?commit=true'
    headers = {'content-type': 'application/json'}
    data = [
        {
            'name': "JJJJESSSSICAAA'SSS STALK EXCHANGE",
            'id': '7',
            'name_state_type_cd': 'R',
            'submit_count': '1',
            'nr_num': 'NR 1',
        },
        {'name': 'JESICA STALK EXCHANGE', 'id': '8', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 2'},
        {'name': 'JESICAS TALK EXCHANGE', 'id': '9', 'name_state_type_cd': 'R', 'submit_count': '1', 'nr_num': 'NR 3'},
    ]
    r = requests.post(url, headers=headers, data=json.dumps(data))
    assert r.status_code == 200

    result = extract_list_of_values_for_key(
        search_histories(client, jwt, "JESSICA'S STALK EXCHANGE LTD")['names'], 'name'
    )
    assert result
    assert len(result) == len(data)


@integration_solr
def test_possessive_ignored(client, jwt, app):
    seed_database_with(client, jwt, "Susan's Talk Exchange")
    verify_same_or_similar(client, jwt, query='Susan Stalk Exchange', expected=None)
