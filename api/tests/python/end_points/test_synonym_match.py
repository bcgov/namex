from namex.models import User
import os
import requests
import json
import pytest
from tests.python import integration_solr, integration_synonym_api
import urllib

token_header = {
                "alg": "RS256",
                "typ": "JWT",
                "kid": "flask-jwt-oidc-test-client"
               }
claims = {
            "iss": "https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc",
            "sub": "43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc",
            "aud": "NameX-Dev",
            "exp": 31531718745,
            "iat": 1531718745,
            "jti": "flask-jwt-oidc-test-support",
            "typ": "Bearer",
            "username": "test-user",
            "realm_access": {
                "roles": [
                    "{}".format(User.EDITOR),
                    "{}".format(User.APPROVER),
                    "viewer",
                    "user"
                ]
            }
         }
SOLR_URL = os.getenv('SOLR_TEST_URL')
SOLR_SYNONYMS_API_URL = os.getenv('SOLR_SYNONYMS_API_URL')

@pytest.fixture(scope="session", autouse=True)
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
    data = '[{"source":"' + source + '", "name":"' + name + '", "id":"'+ id +'"}]'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200

def verify(data, expected):
    verified = False
    print(data['names'])
    for name in data['names']:
        print('ACTUAL ', name['name'])
        print('EXPECTED ',expected)

        if expected == None:
        # check that the name is the title of a query sent (no real names were returned from solr)
            if name['name'].find('----') == -1:
                print('HERE')
                verified = False
                break
            else:
                verified = True
            print(verified)
        # if the expected name is in the names returned this will set 'verified' to true before the loop finishes
        elif expected.find(name['name']) != -1:
            verified = True
            break

    assert verified

# def verify_synonym_match_results(client, jwt, query, expected):
#     data = search_synonym_match(client, jwt, query)
#     verify(data, expected)

def verify_synonym_match(client, jwt, query, expected_list):
    data = search_synonym_match(client, jwt, query)
    if expected_list:
        for expected in expected_list:
            verify(data, expected)
    else:
        verify(data, None)

def search_synonym_match(client, jwt, query):
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    url = '/api/v1/requests/synonymbucket/' + query
    print(url)
    rv = client.get(url, headers=headers)

    assert rv.status_code == 200
    return json.loads(rv.data)

@integration_synonym_api
@integration_solr
def test_find_with_first_word(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_synonym_match(client, jwt,
        query='JM',
        expected_list=['----JM* ','JM Van Damme inc ']
    )

@pytest.mark.skip(reason="frontend handles empty string for now")
@integration_synonym_api
@integration_solr
def test_resist_empty(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_synonym_match(client, jwt,
        query='',
        expected_list=None
    )

@integration_synonym_api
@integration_solr
def test_returns_names_for_all_queries(client, jwt, app):
    seed_database_with(client, jwt, 'JM VAN DAMME INC')
    verify_synonym_match(client, jwt,
        query='JM VAN DAMME INC',
        expected_list=['----JM VAN DAMME INC* ', 'JM VAN DAMME INC', '----JM VAN DAMME* ', 'JM VAN DAMME INC',
                '----JM VAN* ', 'JM VAN DAMME INC', '----JM* ', 'JM VAN DAMME INC']
    )

@integration_synonym_api
@integration_solr
def test_case_insensitive(client, jwt, app):
    seed_database_with(client, jwt, 'JacKlEs')
    verify_synonym_match(client, jwt,
        query='jackles',
        expected_list=['----JACKLES* ', 'JacKlEs']
    )

@integration_synonym_api
@integration_solr
def test_no_match(client, jwt, app):
    seed_database_with(client, jwt, 'JM VAN DAMME INC')
    verify_synonym_match(client, jwt,
        query='Hello BC inc',
        expected_list=None
    )

@integration_synonym_api
@integration_solr
def test_numbers_preserved(client, jwt, app):
    seed_database_with(client, jwt, 'VAN 4 TRUCKING INC')
    verify_synonym_match(client, jwt,
       query='VAN 4 TRUCKING',
       expected_list=['VAN 4 TRUCKING INC']
    )

@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('JAM\' HOLDING', 'JAM HOLDING'),
    ('JAM\'S HOLDING', 'JAM HOLDING'),
    ('JAM HOLDING', 'JAM\'S HOLDING'),
    ('JAM\'S HOLDING', 'JAM\'S HOLDING'),
    ('JAMS HOLDING', 'JAM HOLDING'),
    ('JAM HOLDING', 'JAMS HOLDING'),
    ('JAMS HOLDING', 'JAMS HOLDING'),
    ('JAMS HOLDINGS', 'JAM HOLDING'),
    ('JAM HOLDING', 'JAMS HOLDINGS'),
    ('JAMS\' HOLDINGS\'', 'JAM HOLDINGS'),
    ('JAM HOLDINGS', 'JAMS\' HOLDINGS\''),
    ('JASONS HOLSTERS', 'JASON HOLSTER'),
    ('A.S. HOLDERS', 'AS HOLDER'),
    ('A.S\'S HOLDERS', 'AS HOLDER'),
])
def test_handles_s_and_possession(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )

@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('J.M. HOLDING', 'JM HOLDING'),
    ('J M HOLDING', 'JM HOLDING'),
    ('J. M. HOLDING', 'JM HOLDING'),
    ('J&M HOLDING', 'JM HOLDING'),
    ('J & M HOLDING', 'JM HOLDING'),
    ('J. & M. HOLDING', 'JM HOLDING'),
    ('J-M HOLDING', 'JM HOLDING'),
])
def test_finds_variations_on_initials(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )

@pytest.mark.skip(reason="'and' not handled yet")
@integration_synonym_api
@integration_solr
def test_ignores_and(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_synonym_match(client, jwt,
       query='J and M Van and Damme inc',
       expected_list=None
    )

@pytest.mark.skip(reason="duplicates not handled yet")
@integration_synonym_api
@integration_solr
def test_duplicated_letters(client, jwt, app):
    seed_database_with(client, jwt, 'Damme Trucking Inc')
    verify_synonym_match(client, jwt,
       query='Dame Trucking Inc',
       expected_list=None
    )

@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('J M HOLDINGS', 'J M HOLDINGS INC'),
    ('JM Van Damme Inc', 'J&M & Van Damme Inc'),
    ('J&M HOLDINGS', 'JM HOLDINGS INC'),
    ('J. & M. HOLDINGS', 'JM HOLDING INC'),
    ('J AND M HOLDINGS', 'J AND M HOLDINGS'),
    ('J-M HOLDINGS', 'J. & M. HOLDINGS'),
    # ('J\'M HOLDINGS', 'J. & M. HOLDINGS'),
    # ('J_M HOLDINGS', 'J. & M. HOLDINGS'),
    # ('J_\'_-M HOLDINGS', 'J.M. HOLDINGS'),
    # ('J@M HOLDINGS', 'J.M. HOLDINGS'),
    # ('J=M HOLDINGS', 'J. M. HOLDINGS'),
    ('J!M HOLDINGS', 'J. & M. HOLDINGS'),
    # ('J!=@_M HOLDINGS', 'J. M. HOLDINGS'),
    ('J+M HOLDINGS', 'J. & M. HOLDING\'S'),
    ('J\M HOLDINGS', 'J. & M. HOLDINGS'),
])
def test_explore_complex_cases(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
       query=criteria,
       expected_list=[seed]
    )

# @integration_solr
# def test_returns_all_fields_that_we_need(client, jwt, app):
#     seed_database_with(client, jwt, 'Van Trucking Inc', 'any-id', 'any-source')
#     verify_synonym_match_results(client, jwt,
#        query='Van Trucking ltd',
#        expected=[
#            {'name': 'Van Trucking Inc', 'id':'any-id', 'source':'any-source'}
#        ]
#     )
#
#
# @pytest.mark.skip(reason="dont know how to make solr handle those scenarios")
# @integration_solr
# @pytest.mark.parametrize("criteria, seed", [
#     ('{JM} HOLDINGS', 'J. & M. HOLDINGS'),
#     ('[JM] HOLDINGS', 'J. & M. HOLDINGS'),
#     ('(JM) HOLDINGS', 'J.M HOLDINGS'),
#     ('J^M HOLDINGS', 'J. & M. HOLDINGS'),
#     ('J~M HOLDINGS', 'J. & M. HOLDINGS'),
#     ('J*M HOLDINGS', 'J. & M. HOLDINGS'),
#     ('J:M HOLDINGS', 'J. & M. HOLDINGS'),
#     ('J?M HOLDINGS', 'J. & M. HOLDINGS')
# ])
# def test_special_characters(client, jwt, app, criteria, seed):
#     seed_database_with(client, jwt, seed)
#     verify_synonym_match(client, jwt,
#        query=criteria,
#        expected=seed
#     )

