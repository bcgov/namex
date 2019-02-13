from namex.models import User
import os
import requests
import json
import pytest
from tests.python import integration_solr
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
    #r = requests.post(url, headers=headers, data=data)

   #assert r.status_code == 200

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
    data = search_synonyms(client, jwt, query)
    verify(data, expected)

def verify_exact_match(client, jwt, query, expected):
    data = search_synonyms(client, jwt, query)
    expect = [
        { 'name':expected, 'id':'1', 'source':'2' }
    ]
    if expected == None:
        expect = []
    verify(data, expect)

def search_synonyms(client, jwt, query):
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    url = '/api/v1/requests/synonymbucket/' + query
    print(url)
    rv = client.get(url, headers=headers)

    assert rv.status_code == 200
    return json.loads(rv.data)

@integration_solr
def test_find_same_name(client, jwt, app):
    seed_database_with(client, jwt, 'TRUCK')
    verify_exact_match(client, jwt,
        query='TRUCK',
        expected='TRUCK'
    )
