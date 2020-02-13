from flask import jsonify
from flask import json

import pytest

from urllib.parse import quote_plus
import jsonpickle

from namex.models import User
from namex.services.name_request.auto_analyse import AnalysisRequestActions, AnalysisResultCodes

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


@pytest.mark.skip
def assert_issues_count_is(count, issues):
    if issues.__len__() > count:
        print('\n' + 'Issue types:' + '\n')
        for issue in issues:
            print('- ' + issue.issueType.value + '\n')
    assert issues.__len__() == count


@pytest.mark.skip
def assert_issues_count_is_gt(count, issues):

    print('\n' + 'Issue types:' + '\n')
    for issue in issues:
        print('- ' + issue.issueType.value + '\n')
    assert issues.__len__() > count


# @pytest.mark.xfail(raises=ValueError)
def test_get_analysis_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS LTD.',
        'location': 'BC',
        'entity_type': 'CR',
        'request_type': 'NEW'
    }

    # TODO: Obviously we can't be using strings with spaces but I don't know how to deal with this yet
    # query = '&'.join("{!s}={}".format(k, v) for (k, v) in test_params.items())
    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


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

# FIRST LET'S TEST AND MAKE SURE ALL VALID REQUESTS ARE WORKING

# @pytest.mark.xfail(raises=ValueError)
def test_new_bc_cr_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS INC.',  # OR [INCORPORATED, LTD]
        'location': 'BC',
        'entity_type': 'CR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_bc_ul_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS ULC.',  # OR [UNLIMITED LIABILITY COMPANY]
        'location': 'BC',
        'entity_type': 'UL',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        if payload.issues.__len__() > 0:
            print('\n' + 'Issue types:' + '\n')
            for issue in payload.issues:
                print('\n' + issue.issueType + '\n')
        assert payload.issues.__len__() == 0


def test_new_bc_cp_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS COOP',  # []
        'location': 'BC',
        'entity_type': 'CP',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_bc_bc_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS INC.',  # OR [INCORPORATED, LTD]
        'location': 'BC',
        'entity_type': 'BC',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_bc_cc_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS INC.',  # OR [INCORPORATED, LTD] ALSO REQ *CCC* INC OR COMMUNITY CONTRIBUTION COMPANY
        'location': 'BC',
        'entity_type': 'CC',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_bc_fr_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS',
        'location': 'BC',
        'entity_type': 'FR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_bc_dba_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS',
        'location': 'BC',
        'entity_type': 'DBA',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_bc_gp_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS',
        'location': 'BC',
        'entity_type': 'GP',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_bc_lp_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS LP.',
        'location': 'BC',
        'entity_type': 'LP',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_bc_ll_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS LLP.',
        'location': 'BC',
        'entity_type': 'LL',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_xpro_xcr_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS INC.',  # OR LTD.
        'location': 'CA',
        'entity_type': 'XCR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_xpro_xul_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS ULC.',
        'location': 'CA',
        'entity_type': 'XUL',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_xpro_xcp_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS COOP',
        'location': 'CA',
        'entity_type': 'XCP',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_xpro_xlc_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS LLC.',  # CHECK FOR DESIGNATION
        'location': 'CA',
        'entity_type': 'XLC',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_xpro_xlp_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS LP.',  # CHECK FOR DESIGNATION
        'location': 'CA',
        'entity_type': 'XLC',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)


def test_new_xpro_xll_valid_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS LLP.',
        'location': 'CA',
        'entity_type': 'XLL',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload does not contain any issues, and if it does that it is an empty list")
    if isinstance(payload.issues, list):
        assert_issues_count_is(0, payload.issues)

# IN THIS SECTION TEST VARIOUS ERROR RESPONSES
