from namex.models import User
import os
import requests
import json
import pytest

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

@pytest.fixture(scope="session", autouse=True)
def reload_schema(request):
    url = SOLR_URL + '/solr/admin/cores?action=RELOAD&core=possible.conflicts&wt=json'
    r = requests.get(url)

    assert r.status_code == 200

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
    print(data['names'])

    assert expected == data['names']

def verify_exact_match_results(client, jwt, query, expected):
    data = search_exact_match(client, jwt, query)
    verify(data, expected)

def verify_exact_match(client, jwt, query, expected):
    data = search_exact_match(client, jwt, query)
    expect = [
        { 'name':expected, 'id':'1', 'source':'2' }
    ]
    if expected == None:
        expect = []
    verify(data, expect)

def search_exact_match(client, jwt, query):
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    rv = client.get('/api/v1/exact-match?query='+query, headers=headers)

    assert rv.status_code == 200
    return json.loads(rv.data)

def test_find_same_name(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt,
        query='JM Van Damme inc',
        expected='JM Van Damme inc'
    )

def test_resists_different_type(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt,
        query='JM Van Damme ltd',
        expected='JM Van Damme inc'
    )

def test_case_insensitive(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt,
        query='JM VAN DAMME INC',
        expected='JM Van Damme inc'
    )

def test_no_match(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt,
        query='Hello BC inc',
        expected=None
    )

def test_ignores_and(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_exact_match(client, jwt,
       query='J and M Van Damme inc',
       expected='JM Van Damme inc'
    )

def test_ignores_dots(client, jwt, app):
    seed_database_with(client, jwt, 'J.M. Van Damme Inc')
    verify_exact_match(client, jwt,
       query='JM Van Damme Inc',
       expected='J.M. Van Damme Inc'
    )

def test_ignores_ampersand(client, jwt, app):
    seed_database_with(client, jwt, 'J&M & Van Damme Inc')
    verify_exact_match(client, jwt,
       query='JM Van Damme Inc',
       expected='J&M & Van Damme Inc'
    )

def test_ignores_comma(client, jwt, app):
    seed_database_with(client, jwt, 'JM, Van Damme Inc')
    verify_exact_match(client, jwt,
       query='JM Van Damme Inc',
       expected='JM, Van Damme Inc'
    )

def test_ignores_exclamation_mark(client, jwt, app):
    seed_database_with(client, jwt, 'JM! Van Damme Inc')
    verify_exact_match(client, jwt,
       query='JM Van Damme Inc',
       expected='JM! Van Damme Inc'
    )

def test_no_match_because_additional_initial(client, jwt, app):
    seed_database_with(client, jwt, 'J.M.J. Van Damme Trucking Inc')
    verify_exact_match(client, jwt,
       query='J.M. Van Damme Trucking Inc',
       expected=None
    )

def test_no_match_because_additional_word(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme Trucking Inc')
    verify_exact_match(client, jwt,
       query='JM Van Damme Trucking International Inc',
       expected=None
    )

def test_no_match_because_missing_one_word(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme Physio inc')
    verify_exact_match(client, jwt,
       query='JM Van Damme inc',
       expected=None
    )

def test_duplicated_letters(client, jwt, app):
    seed_database_with(client, jwt, 'Damme Trucking Inc')
    verify_exact_match(client, jwt,
       query='Dame Trucking Inc',
       expected='Damme Trucking Inc'
    )

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
        'soc.'
    ]
    for suffix in suffixes:
        seed_database_with(client, jwt, 'Van Trucking ' + suffix)
        verify_exact_match(client, jwt,
           query='Van Trucking',
           expected='Van Trucking ' + suffix
        )

def test_numbers_preserved(client, jwt, app):
    seed_database_with(client, jwt, 'Van 4 Trucking Inc')
    verify_exact_match(client, jwt,
       query='Van 4 Trucking ltd',
       expected='Van 4 Trucking Inc'

    )

def test_returns_all_fields_that_we_need(client, jwt, app):
    seed_database_with(client, jwt, 'Van Trucking Inc', 'any-id', 'any-source')
    verify_exact_match_results(client, jwt,
       query='Van Trucking ltd',
       expected=[
           {'name': 'Van Trucking Inc', 'id':'any-id', 'source':'any-source'}
       ]
    )




