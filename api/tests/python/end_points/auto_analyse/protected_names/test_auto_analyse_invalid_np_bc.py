from datetime import date

from flask import jsonify
from flask import json

import pytest

from urllib.parse import quote_plus
import jsonpickle

from namex.models import User
from namex.services.name_request.auto_analyse import AnalysisRequestActions, AnalysisIssueCodes

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
        print('- ' + issue.get('issue_type') + '\n')
    assert issues.__len__() > count


@pytest.mark.skip
def assert_issue_type_is_one_of(types, issue):
    assert issue.get('issue_type') in types


@pytest.mark.skip
def assert_has_issue_type(issue_type, issues):
    has_issue = False
    for issue in issues:
        has_issue = True if issue.get('issue_type') == issue_type.value else False

    assert has_issue is True


# IN THIS SECTION TEST VARIOUS ERROR RESPONSES


# USE MOUNTAIN VIEW FOOD GROWERS INC.

@pytest.mark.xfail(raises=ValueError)
def test_add_distinctive_word_request_response(client, jwt, app):
    from namex.models import WordClassification as WordClassificationDAO

    words_list = [{'word': 'GROWERS', 'classification': 'DESC'},
                  {'word': 'AEROENTERPRISES', 'classification': 'DESC'}]

    for record in words_list:
        wc = WordClassificationDAO()
        wc.classification = record['classification']
        wc.word = record['word']
        wc.start_dt = date.today()
        wc.approved_dt = date.today()
        wc.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {'name': 'GROWERS INC.',
         'location': 'BC',
         'entity_type': 'CR',
         'request_action': 'NEW'
         },
        {'name': 'AEROENTERPRISES INC.',
         'location': 'BC',
         'entity_type': 'CR',
         'request_action': 'NEW'
         }
    ]

    for entry in test_params:
        query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())

        path = ENDPOINT_PATH + '?' + query
        print('\n' + 'request: ' + path + '\n')
        response = client.get(path, headers=headers)
        payload = jsonpickle.decode(response.data)
        print("Assert that the payload contains issues")
        if isinstance(payload.get('issues'), list):
            assert_issues_count_is_gt(0, payload.get('issues'))

            for issue in payload.get('issues'):
                # Make sure only Well Formed name issues are being returned
                assert_issue_type_is_one_of([
                    AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
                    AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
                    AnalysisIssueCodes.TOO_MANY_WORDS
                ], issue)

            assert_has_issue_type(AnalysisIssueCodes.ADD_DISTINCTIVE_WORD, payload.get('issues'))


# @pytest.mark.xfail(raises=ValueError)
def test_add_descriptive_word_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW INC.',
        'location': 'BC',
        'entity_type': 'BC',
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
                AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
                AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
                AnalysisIssueCodes.TOO_MANY_WORDS
            ], issue)

        assert_has_issue_type(AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD, payload.issues)


# @pytest.mark.xfail(raises=ValueError)
def test_too_many_words_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS INTERNATIONAL INC.',
        # TODO: We need another test to make sure that designations are not being included in too many words (test: clean name)
        'location': 'BC',
        'entity_type': 'BC',
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
                AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
                AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
                AnalysisIssueCodes.TOO_MANY_WORDS
            ], issue)

        assert_has_issue_type(AnalysisIssueCodes.TOO_MANY_WORDS, payload.issues)


# @pytest.mark.xfail(raises=ValueError)
def test_contains_words_to_avoid_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW VSC INC.',  # VSC = VANCOUVER STOCK EXCHANGE
        'location': 'BC',
        'entity_type': 'BC',
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
        assert_has_issue_type(AnalysisIssueCodes.WORD_TO_AVOID, payload.issues)


# @pytest.mark.xfail(raises=ValueError)
def test_designation_mismatch_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS COOP',  # TODO: Test for all designation mismatches
        'location': 'BC',
        'entity_type': 'BC',
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
        assert_has_issue_type(AnalysisIssueCodes.DESIGNATION_MISMATCH, payload.issues)


# @pytest.mark.xfail(raises=ValueError)
def test_name_requires_consent_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = {
        'name': 'MOUNTAIN VIEW FOOD ENGINEERING INC.',
        'location': 'BC',
        'entity_type': 'BC',
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
        assert_has_issue_type(AnalysisIssueCodes.NAME_REQUIRES_CONSENT, payload.issues)


# @pytest.mark.xfail(raises=ValueError)
def test_contains_unclassifiable_word_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    # TODO: Insert BLOGGINS into word classification, should fail, because it's unclassified
    #  This ideally involves separate tests
    test_params = {
        'name': 'MOUNTAIN VIEW FOOD BLOGGINS INC.',
        'location': 'BC',
        'entity_type': 'BC',
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
        assert_has_issue_type(AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD, payload.issues)


# TODO: Pytest uses an empty DB so create a CONFLICTING NAME first before / as part of running this test!!!
# @pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_request_response(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    # TODO: Insert 'name': 'MOUNTAIN VIEW FOOD INC.' as the 1st test!
    # TODO: Insert 'name': 'MOUNTAIN VIEW GROWERS INC.' as the 2nd test!
    test_params = {
        'name': 'MOUNTAIN VIEW FOOD GROWERS INC.',
        'location': 'BC',
        'entity_type': 'BC',
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
        assert_has_issue_type(AnalysisIssueCodes.CORPORATE_CONFLICT, payload.issues)
