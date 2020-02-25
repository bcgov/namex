# TODO: FIX TESTS!!!

from flask import jsonify
from flask import json

import pytest

from urllib.parse import quote_plus
import jsonpickle

from namex.models import User
from namex.services.name_request.auto_analyse import AnalysisRequestActions, AnalysisResultCodes

# from tests.python import integration_oracle_namesdb

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

@pytest.mark.skip
def assert_issue_type_is_one_of(types, issue):
    assert issue.issueType in types


@pytest.mark.skip
def assert_has_issue_type(issue_type, issues):
    has_issue = False
    for issue in issues:
        has_issue = True if issue.issueType == issue_type and issue.issueType.value == issue_type.value else False

    assert has_issue is True

# IN THIS SECTION TEST VARIOUS ERROR RESPONSES


# USE MOUNTAIN VIEW FOOD GROWERS ULC.

# @pytest.mark.xfail(raises=ValueError)
def test_contains_unclassifiable_word_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD BLOGGINS ULC.',
        'location': 'CA',
        'entity_type': 'XUL',
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
def test_contains_words_to_avoid_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW VSC ULC.',
        'location': 'CA',
        'entity_type': 'XUL',
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
def test_name_requires_consent_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD ENGINEERING ULC.',
        'location': 'CA',
        'entity_type': 'XUL',
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


# @pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_request_response(client, jwt, app):
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
    print("Assert that the payload contains issues")
    if isinstance(payload.issues, list):
        assert_issues_count_is_gt(0, payload.issues)
        assert_has_issue_type(AnalysisResultCodes.CORPORATE_CONFLICT, payload.issues)
