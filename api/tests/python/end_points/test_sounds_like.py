from namex.models import User
import requests
import json
import pytest
from tests.python import integration_solr
import urllib
from hamcrest import *


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


@pytest.fixture(scope="session", autouse=True)
def reload_schema(solr):
    url = solr + '/solr/admin/cores?action=RELOAD&core=possible.conflicts&wt=json'
    r = requests.get(url)

    assert r.status_code == 200


@integration_solr
def test_solr_available(solr, app, client, jwt):
    url = solr + '/solr/possible.conflicts/admin/ping'
    r = requests.get(url)

    assert r.status_code == 200


def clean_database(solr):
    url = solr + '/solr/possible.conflicts/update?commit=true'
    headers = {'content-type': 'text/xml'}
    data = '<delete><query>id:*</query></delete>'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200


def seed_database_with(solr, name, id='1', source='CORP'):
    url = solr + '/solr/possible.conflicts/update?commit=true'
    headers = {'content-type': 'application/json'}
    data = '[{"source":"' + source + '", "name":"' + name + '", "id":"'+ id +'"}]'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200


def verify(data, expected):
    actual = [{ 'name':doc['name'] } for doc in data['names']]
    print(actual)
    print(expected)

    assert_that(len(actual), equal_to(len(expected)))
    for item in expected:
        assert_that(actual, has_item(item))


def verify_results(client, jwt, query, expected):
    data = search(client, jwt, query)
    verify(data, expected)


def search(client, jwt, query):
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    url = '/api/v1/sounds-like?query=' + urllib.parse.quote(query)
    print(url)
    rv = client.get(url, headers=headers)

    assert rv.status_code == 200
    return json.loads(rv.data)


@integration_solr
def test_all_good(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'GOLDSTREAM ELECTRICAL LTD')
    verify_results(client, jwt,
       query='GOLDSMITHS',
       expected=[
           {'name': 'GOLDSTREAM ELECTRICAL LTD'}
       ]
    )


@integration_solr
def test_sounds_like(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'GAYLEDESIGNS INC.', id='1')
    seed_database_with(solr, 'GOLDSTREAM ELECTRICAL LTD', id='2')
    seed_database_with(solr, 'GLADSTONE JEWELLERY LTD', id='3')
    seed_database_with(solr, 'GOLDSTEIN HOLDINGS INC.', id='4')
    seed_database_with(solr, 'CLOUDSIDE INN INCORPORATED', id='5')
    seed_database_with(solr, 'GOLDSPRING PROPERTIES LTD', id='6')
    seed_database_with(solr, 'GOLDSTRIPES AVIATION INC', id='7')
    seed_database_with(solr, 'GLADSTONE CAPITAL CORP', id='8')
    seed_database_with(solr, 'KLETAS LAW CORPORATION', id='9')
    seed_database_with(solr, 'COLDSTREAM VENTURES INC.', id='10')
    seed_database_with(solr, 'BLABLA ANYTHING', id='11')
    verify_results(client, jwt,
       query='GOLDSMITHS',
       expected=[
           {'name': 'COLDSTREAM VENTURES INC.'},
           {'name': 'GOLDSTEIN HOLDINGS INC.'},
           {'name': 'GOLDSPRING PROPERTIES LTD'},
           {'name': 'GOLDSTREAM ELECTRICAL LTD'},
           {'name': 'GOLDSTRIPES AVIATION INC'},
       ]
    )

@integration_solr
def test_liberti(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'LIBERTI', id='1')
    verify_results(client, jwt,
       query='LIBERTY',
       expected=[
           {'name': 'LIBERTI'},
       ]
    )

@integration_solr
def test_deeper(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'LABORATORY', id='1')
    seed_database_with(solr, 'LAPORTE', id='2')
    seed_database_with(solr, 'LIBERTI', id='3')
    verify_results(client, jwt,
       query='LIBERTY',
       expected=[
           {'name': 'LIBERTI'},
       ]
    )

@integration_solr
def test_jasmine(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'JASMINE', id='1')
    verify_results(client, jwt,
       query='OSMOND',
       expected=[
       ]
    )


@integration_solr
def test_nikke(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'NEEKA', id='1')
    verify_results(client, jwt,
       query='NIKKA',
       expected=[
           {'name': 'NEEKA'},
       ]
    )


@integration_solr
def test_neeka(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'NIKKA', id='1')
    verify_results(client, jwt,
       query='NEEKA',
       expected=[
           {'name': 'NIKKA'},
       ]
    )


@integration_solr
def test_neeka_like(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'NIPPA', id='1')
    verify_results(client, jwt,
       query='NEEPA',
       expected=[
           {'name': 'NIPPA'},
       ]
    )


@integration_solr
def test_crazy(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'NIPPLA', id='1')
    verify_results(client, jwt,
       query='NEEPLA',
       expected=[
           {'name': 'NIPPLA'},
       ]
    )


@integration_solr
def test_more_crazy(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'NIPPLA', id='1')
    seed_database_with(solr, 'NIPPLAA', id='2')
    verify_results(client, jwt,
       query='NEEPLA',
       expected=[
           {'name': 'NIPPLA'},
           {'name': 'NIPPLAA'},
       ]
    )

@integration_solr
def test_neighbour(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'NEIGHBOUR', id='1')
    verify_results(client, jwt,
       query='NAYBOR',
       expected=[
           {'name': 'NEIGHBOUR'}
       ]
    )

@integration_solr
def test_fey(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'FEY', id='1')
    verify_results(client, jwt,
       query='FAY',
       expected=[
           {'name': 'FEY'}
       ]
    )

