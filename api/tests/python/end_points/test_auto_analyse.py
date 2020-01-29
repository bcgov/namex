from flask import jsonify
from flask import json

from urllib.parse import quote_plus

from namex.models import User

from tests.python import integration_oracle_namesdb


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

API_BASE_URI = '/api/v1/'
ENDPOINT_PATH = API_BASE_URI + 'name-analysis'
# params = {
#   name,
#   location, one of: [‘bc’, ‘ca’, ‘us’, or ‘it’],
#   entity_type: abbreviation. convention not finalized yet.
#   request_type, one of: [‘new’, ‘existing’, ‘continuation’]
# }


def test_get_analysis_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS LTD.',
        'location': 'BC',
        'entity_type': 'SOLPROP',
        'request_type': 'new'
    }

    query = '&'.join("{!s}={!r}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    print(response)


# Test each of the response strategies
# API Returns
# Requires addition of distinctive word
# Requires addition of descriptive word
# Name Contains a Word To Avoid
# Designation Mismatch
# Too Many Words
# Name Requires Consent
# Contains Unclassifiable Word
# Conflicts with the Corporate Database


def test_valid_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN NEW FOOD GROWERS LTD.',
        'location': 'BC',
        'entity_type': 'SOLPROP',
        'request_type': 'new'
    }

    query = '&'.join("{!s}={!r}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    print(response)


def test_add_distinctive_word_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'FOOD GROWERS LTD.',
        'location': 'BC',
        'entity_type': 'SOLPROP',
        'request_type': 'new'
    }

    query = '&'.join("{!s}={!r}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    print(response)


def test_add_descriptive_word_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW LTD.',
        'location': 'BC',
        'entity_type': 'SOLPROP',
        'request_type': 'new'
    }

    query = '&'.join("{!s}={!r}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    print(response)


def test_contains_words_to_avoid_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD PROVINCIAL LTD.',
        'location': 'BC',
        'entity_type': 'SOLPROP',
        'request_type': 'new'
    }

    query = '&'.join("{!s}={!r}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    print(response)


def test_designation_mismatch_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'My Test String',
        'location': 'BC',
        'entity_type': 'whatev',
        'request_type': 'new'
    }

    query = '&'.join("{!s}={!r}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    print(response)


def test_too_many_words_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS INTERNATIONAL LTD.',
        'location': 'BC',
        'entity_type': 'whatev',
        'request_type': 'new'
    }

    query = '&'.join("{!s}={!r}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    print(response)


def test_name_requires_consent_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'VANCOUVER PORT FOOD GROWERS LTD.',
        'location': 'BC',
        'entity_type': 'whatev',
        'request_type': 'new'
    }

    query = '&'.join("{!s}={!r}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    print(response)


def test_contains_unclassifiable_word_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'UNCLASSIFIED MOUNTAIN FOOD GROWERS LTD.',
        'location': 'BC',
        'entity_type': 'whatev',
        'request_type': 'new'
    }

    query = '&'.join("{!s}={!r}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    print(response)


def test_corporate_name_conflict_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS LTD.',
        'location': 'BC',
        'entity_type': 'whatev',
        'request_type': 'new'
    }

    query = '&'.join("{!s}={!r}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    print(response)
