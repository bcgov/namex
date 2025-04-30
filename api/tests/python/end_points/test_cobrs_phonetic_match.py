import json
import os

import pytest
import requests

from namex.models import User

from .. import integration_solr, integration_synonym_api

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
SOLR_SYNONYMS_API_URL = os.getenv('SOLR_SYNONYMS_API_URL')


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


def seed_database_with(client, jwt, name, id='1', source='2', clean=True):
    if clean:
        clean_database(client, jwt)

    url = SOLR_URL + '/solr/possible.conflicts/update?commit=true'
    headers = {'content-type': 'application/json'}
    data = '[{"source":"' + source + '", "name":"' + name + '", "id":"' + id + '"}]'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200


def verify(data, expected=[], not_expected=None):
    # expected + not_expected lists should be tested separately
    if expected and not_expected:
        assert False

    verified = False
    print(data['names'])
    print('EXPECTED ', expected)
    print('NOT EXPECTED ', not_expected)
    for result in data['names']:
        name = result['name_info']
        print('ACTUAL ', name['name'])

        if expected == []:
            # check that the name is the title of a query sent (no real names were returned from solr)
            if name['name'].find('----') == -1:
                verified = False
                break
            else:
                verified = True
        # if the expected name is in the names returned this will set 'verified' to true before the loop finishes
        elif expected.lower().find(name['name'].lower()) != -1:
            verified = True
            break

        elif not_expected:
            verified = True
            if not_expected.lower().find(name['name'].lower()) != -1:
                verified = False
                break

    assert verified


# def verify_match_results(client, jwt, query, expected):
#     data = search_cobrs_phonetic_match(client, jwt, query)
#     verify(data, expected)


def verify_match(client, jwt, query, expected_list=[], not_expected_list=None):
    data = search_cobrs_phonetic_match(client, jwt, query)
    if expected_list == [] or expected_list:
        if expected_list == []:
            verify(data, [])
        else:
            for expected in expected_list:
                verify(data, expected)

    elif not_expected_list:
        for not_expected in not_expected_list:
            verify(data, None, not_expected)


def search_cobrs_phonetic_match(client, jwt, query):
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    url = '/api/v1/requests/cobrsphonetics/' + query + '/*'
    print(url)
    rv = client.get(url, headers=headers)

    assert rv.status_code == 200
    return json.loads(rv.data)


@integration_synonym_api
@integration_solr
def test_resist_empty(client, jwt):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    seed_database_with(client, jwt, 'SOME RANDOM NAME', clean=False)
    verify_match(client, jwt, query='*', expected_list=None)


@integration_synonym_api
@integration_solr
def test_no_match(client, jwt, app):
    seed_database_with(client, jwt, 'JM VAN DAMME INC')
    verify_match(client, jwt, query='Hello BC inc', expected_list=None)


@integration_synonym_api
@integration_solr
def test_designation_removal(client, jwt, app):
    seed_database_with(client, jwt, 'DESIGNATION TEST')
    verify_match(
        client,
        jwt,
        query='DESIGNATION LIMITED',
        expected_list=['----DESIGNATION'],
        not_expected_list=['----DESIGNATION LIMITED '],
    )


@integration_synonym_api
@integration_solr
def test_duplicated_letters(client, jwt, app):
    seed_database_with(client, jwt, 'Damme Trukking Inc')
    verify_match(client, jwt, query='Dame Truccing Inc', expected_list=['Damme Trukking Inc'])


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize(
    'criteria, seed',
    [
        ('JM HOLDING', 'JM HOLDING'),
        ('SWAP TESTING EXAMPLE', 'TESTING SWAP EXAMPLE'),
    ],
)
def test_non_phonetic_match_does_not_return(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_match(
        client,
        jwt,
        query=criteria,
        expected_list=[],
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize(
    'criteria, seed',
    [
        ('zoccer', 'soccer'),
        ('something needz tezts', 'zomething needs tests'),
        ('realiti treaty wycked', 'realyty treati wicked'),
        ('pacifico apple trees', 'pocifica opple trees'),
        ('pacifika west coast skill', 'pacifica west koast scill'),
        ('pacifika west coast skill', 'pacifica west koast scill'),
        ('skhool for dummies school', 'school for dummies scool'),
        ('extrodinary index indxing', 'xtrodinary indx indexing'),
        ('macdonalds mcdouble with somemacwordmc', 'mcdonalds macdouble with somemcwordmac'),
        ('phor famous truffles wiphe ruph', 'for phamous truphles wife ruff'),
    ],
)
def test_phonetic_letter_swaps(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_match(client, jwt, query=criteria, expected_list=[seed])


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize(
    'criteria, seed',
    [
        ('0 one 2', 'zero 1 two'),
        ('3 four 5', 'three 4 five'),
        ('6 seven 8 nine', 'six 7 eight 9'),
    ],
)
def test_phonetic_number_swaps(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_match(client, jwt, query=criteria, expected_list=[seed])


@integration_synonym_api
@integration_solr
def test_stack_ignores_wildcards(client, jwt, app):
    verify_match(
        client,
        jwt,
        query='TESTING* @WILDCARDS',
        expected_list=['----TESTING WILDCARDS'],
        not_expected_list=['----TESTING* @WILDCARDS'],
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize(
    'criteria, seed',
    [
        ('JMACK', 'J-MAC'),
        ('JMACK', 'j-mac'),
        ('JMAK', 'J-MAC'),
        ('JMAK', 'j-mac'),
        ('JMC', 'J-MAC'),
        ('JMC', 'j-mac'),
    ],
)
def test_all_macs_are_equal(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_match(client, jwt, query=criteria, expected_list=[seed])


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize(
    'criteria, seed',
    [
        ('EMPACK', 'EMPAK'),
    ],
)
def test_ck_and_k(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_match(client, jwt, query=criteria, expected_list=[seed])


@integration_synonym_api
@integration_solr
def test_stack_contains_synonyms(client, jwt, app):
    seed_database_with(client, jwt, 'PACIFIC LUMBER PRODUCTS LTD.', id='1')
    seed_database_with(client, jwt, 'PACIFIC FOREST PRODUCTS LTD.', id='2', clean=False)

    verify_match(
        client,
        jwt,
        query='PACIFIK LUMBER',
        expected_list=[
            '----PACIFIK LUMBER',
            'PACIFIC LUMBER PRODUCTS LTD.',
            '----PACIFIK synonyms:(LUMBER)',
            'PACIFIC FOREST PRODUCTS LTD.',
        ],
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize(
    'query',
    [
        ('T.H.E.'),
        ('COMPANY'),
        ('ASSN'),
        ('THAT'),
        ('LIMITED CORP.'),
    ],
)
def test_query_stripped_to_empty_string(client, jwt, query):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    seed_database_with(client, jwt, 'SOME RANDOM NAME', id='2', source='2', clean=False)
    verify_match(client, jwt, query=query, expected_list=None)
