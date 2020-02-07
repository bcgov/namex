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
        'entity_type': 'FR',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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
        'name': 'BOB\'S CARPENTRY INC.',
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


# @pytest.mark.xfail(raises=ValueError)
def test_add_distinctive_word_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'BOB\'S CARPENTRY INC.',
        'location': 'BC',
        'entity_type': 'FR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload contains issues")
    if isinstance(payload.issues, list):
        assert_issues_count_is_gt(0, payload.issues)

        for issue in payload.issues:
            # Make sure only Well Formed name issues are being returned
            assert_issue_type_is_one_of([
                AnalysisResultCodes.ADD_DISTINCTIVE_WORD,
                AnalysisResultCodes.ADD_DESCRIPTIVE_WORD,
                AnalysisResultCodes.TOO_MANY_WORDS
            ], issue)

        assert_has_issue_type(AnalysisResultCodes.ADD_DISTINCTIVE_WORD, payload.issues)


# @pytest.mark.xfail(raises=ValueError)
def test_add_descriptive_word_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'BOB\'S CARPENTRY INC.',
        'location': 'BC',
        'entity_type': 'FR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload contains issues")
    if isinstance(payload.issues, list):
        assert_issues_count_is_gt(0, payload.issues)

        for issue in payload.issues:
            # Make sure only Well Formed name issues are being returned
            assert_issue_type_is_one_of([
                AnalysisResultCodes.ADD_DISTINCTIVE_WORD,
                AnalysisResultCodes.ADD_DESCRIPTIVE_WORD,
                AnalysisResultCodes.TOO_MANY_WORDS
            ], issue)

        assert_has_issue_type(AnalysisResultCodes.ADD_DESCRIPTIVE_WORD, payload.issues)


# @pytest.mark.xfail(raises=ValueError)
def test_too_many_words_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'BOB\'S CARPENTRY AND HOME RENOVATIONS INC.',
        'location': 'BC',
        'entity_type': 'FR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload contains issues")
    if isinstance(payload.issues, list):
        assert_issues_count_is_gt(0, payload.issues)

        for issue in payload.issues:
            # Make sure only Well Formed name issues are being returned
            assert_issue_type_is_one_of([
                AnalysisResultCodes.ADD_DISTINCTIVE_WORD,
                AnalysisResultCodes.ADD_DESCRIPTIVE_WORD,
                AnalysisResultCodes.TOO_MANY_WORDS
            ], issue)

        assert_has_issue_type(AnalysisResultCodes.TOO_MANY_WORDS, payload.issues)


# @pytest.mark.xfail(raises=ValueError)
def test_contains_words_to_avoid_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'BOB\'S BULLSHIT CARPENTRY INC.',
        'location': 'BC',
        'entity_type': 'CR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload contains issues")
    if isinstance(payload.issues, list):
        assert_issues_count_is_gt(0, payload.issues)
        assert_has_issue_type(AnalysisResultCodes.WORD_TO_AVOID, payload.issues)


# @pytest.mark.xfail(raises=ValueError)
def test_designation_mismatch_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'BOB\'S CARPENTRY INC.',
        'location': 'BC',
        'entity_type': 'CR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload contains issues")
    if isinstance(payload.issues, list):
        assert_issues_count_is_gt(0, payload.issues)
        assert_has_issue_type(AnalysisResultCodes.DESIGNATION_MISMATCH, payload.issues)

    test_params = {
        'name': 'MOUNTAIN NEW FOOD GROWERS INC.',
        'location': 'CA',
        'entity_type': 'XLC',
        'request_type': 'NEW'
    }

# @pytest.mark.xfail(raises=ValueError)
def test_name_requires_consent_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'BOB\'S CARPENTRY INC.',
        'location': 'BC',
        'entity_type': 'CR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload contains issues")
    if isinstance(payload.issues, list):
        assert_issues_count_is_gt(0, payload.issues)
        assert_has_issue_type(AnalysisResultCodes.NAME_REQUIRES_CONSENT, payload.issues)

# IN THIS SECTION TEST VARIOUS ERROR RESPONSES

# @pytest.mark.xfail(raises=ValueError)
def test_contains_unclassifiable_word_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'BOB\'S CARPENTRY INC.',
        'location': 'BC',
        'entity_type': 'FR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload contains issues")
    if isinstance(payload.issues, list):
        assert_issues_count_is_gt(0, payload.issues)
        assert_has_issue_type(AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD, payload.issues)


# @pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'BOB\'S CARPENTRY INC.',
        'location': 'BC',
        'entity_type': 'FR',
        'request_type': 'NEW'
    }

    query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
    path = ENDPOINT_PATH + '?' + query
    print('\n' + 'request: ' + path + '\n')
    response = client.get(path, headers=headers)
    payload = jsonpickle.decode(response.data)
    print("Assert that the payload contains issues")
    if isinstance(payload.issues, list):
        assert_issues_count_is_gt(0, payload.issues)
        assert_has_issue_type(AnalysisResultCodes.CORPORATE_CONFLICT, payload.issues)
