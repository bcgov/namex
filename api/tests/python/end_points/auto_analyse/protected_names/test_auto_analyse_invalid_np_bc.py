from datetime import date
from operator import itemgetter

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

# # Showstoppers
# # 1.- Unique word classified as descriptive
# @pytest.mark.xfail(raises=ValueError)
# def test_add_distinctive_word_base_request_response(client, jwt, app):
#     words_list_classification = [{'word': 'GROWERS', 'classification': 'DESC'},
#                   {'word': 'AEROENTERPRISES', 'classification': 'DESC'}]
#
#     save_words_list_classification(words_list_classification)
#
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = [
#         {'name': 'GROWERS INC.',
#          'location': 'BC',
#          'entity_type': 'CR',
#          'request_action': 'NEW'
#          },
#         {'name': 'AEROENTERPRISES INC.',
#          'location': 'BC',
#          'entity_type': 'CR',
#          'request_action': 'NEW'
#          }
#     ]
#
#     for entry in test_params:
#         query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
#
#         path = ENDPOINT_PATH + '?' + query
#         print('\n' + 'request: ' + path + '\n')
#         response = client.get(path, headers=headers)
#         payload = jsonpickle.decode(response.data)
#         print("Assert that the payload contains issues")
#         if isinstance(payload.get('issues'), list):
#             assert_issues_count_is_gt(0, payload.get('issues'))
#
#             for issue in payload.get('issues'):
#                 # Make sure only Well Formed name issues are being returned
#                 assert_issue_type_is_one_of([
#                     AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
#                     AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
#                     AnalysisIssueCodes.TOO_MANY_WORDS
#                 ], issue)
#
#             assert_has_issue_type(AnalysisIssueCodes.ADD_DISTINCTIVE_WORD, payload.get('issues'))
#
#
# # 2.- Unique word classified as distinctive
# @pytest.mark.xfail(raises=ValueError)
# def test_add_descriptive_word_base_request_response(client, jwt, app):
#     words_list_classification = [{'word': 'ACTIVATIVE', 'classification': 'DIST'}]
#     save_words_list_classification(words_list_classification)
#
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = [
#         {
#             'name': 'ACTIVATIVE INC.',
#             'location': 'BC',
#             'entity_type': 'CR',
#             'request_action': 'NEW'
#         }
#     ]
#
#     for entry in test_params:
#         query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
#
#         path = ENDPOINT_PATH + '?' + query
#         print('\n' + 'request: ' + path + '\n')
#         response = client.get(path, headers=headers)
#         payload = jsonpickle.decode(response.data)
#         print("Assert that the payload contains issues")
#         if isinstance(payload.get('issues'), list):
#             assert_issues_count_is_gt(0, payload.get('issues'))
#
#             for issue in payload.get('issues'):
#                 # Make sure only Well Formed name issues are being returned
#                 assert_issue_type_is_one_of([
#                     AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
#                     AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
#                     AnalysisIssueCodes.TOO_MANY_WORDS
#                 ], issue)
#
#             assert_has_issue_type(AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD, payload.get('issues'))
#
#
# # 3.- Unique word not classified in word_classification
# @pytest.mark.xfail(raises=ValueError)
# def test_add_descriptive_word_not_classified_request_response(client, jwt, app):
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = [
#         {
#             'name': 'INVINITY INC.',
#             'location': 'BC',
#             'entity_type': 'CR',
#             'request_action': 'NEW'
#         }
#     ]
#
#     for entry in test_params:
#         query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
#
#         path = ENDPOINT_PATH + '?' + query
#         print('\n' + 'request: ' + path + '\n')
#         response = client.get(path, headers=headers)
#         payload = jsonpickle.decode(response.data)
#         print("Assert that the payload contains issues")
#         if isinstance(payload.get('issues'), list):
#             assert_issues_count_is_gt(0, payload.get('issues'))
#
#             for issue in payload.get('issues'):
#                 # Make sure only Well Formed name issues are being returned
#                 assert_issue_type_is_one_of([
#                     AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
#                     AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
#                     AnalysisIssueCodes.TOO_MANY_WORDS
#                 ], issue)
#
#             assert_has_issue_type(AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD, payload.get('issues'))
#
#
# # 4.- Unique word classified as distinctive and descriptive
# @pytest.mark.xfail(raises=ValueError)
# def test_add_descriptive_word_both_classifications_request_response(client, jwt, app):
#     words_list_classification = [{'word': 'ABBOTSFORD’ ', 'classification': 'DIST'},
#                   {'word': 'ABBOTSFORD’ ', 'classification': 'DESC'}]
#     save_words_list_classification(words_list_classification)
#
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = [
#         {
#             'name': 'ABBOTSFORD INC.',
#             'location': 'BC',
#             'entity_type': 'CR',
#             'request_action': 'NEW'
#         }
#     ]
#
#     for entry in test_params:
#         query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
#
#         path = ENDPOINT_PATH + '?' + query
#         print('\n' + 'request: ' + path + '\n')
#         response = client.get(path, headers=headers)
#         payload = jsonpickle.decode(response.data)
#         print("Assert that the payload contains issues")
#         if isinstance(payload.get('issues'), list):
#             assert_issues_count_is_gt(0, payload.get('issues'))
#
#             for issue in payload.get('issues'):
#                 # Make sure only Well Formed name issues are being returned
#                 assert_issue_type_is_one_of([
#                     AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
#                     AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
#                     AnalysisIssueCodes.TOO_MANY_WORDS
#                 ], issue)
#
#             assert_has_issue_type(AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD, payload.get('issues'))
#
#
# # 5.- Successful well formed name:
# @pytest.mark.xfail(raises=ValueError)
# def test_successful_well_formed_request_response(client, jwt, app):
#     words_list_classification = [{'word': 'ADEPTIO', 'classification': 'DIST'},
#                   {'word': 'AGRONOMICS', 'classification': 'DESC'}]
#     save_words_list_classification(words_list_classification)
#
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = [
#         {
#             'name': 'ADEPTIO AGRONOMICS INC.',
#             'location': 'BC',
#             'entity_type': 'CR',
#             'request_action': 'NEW'
#         }
#     ]
#
#     for entry in test_params:
#         query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
#
#         path = ENDPOINT_PATH + '?' + query
#         print('\n' + 'request: ' + path + '\n')
#         response = client.get(path, headers=headers)
#         payload = jsonpickle.decode(response.data)
#         print("Assert that the payload status is Available")
#         assert ('Available', payload.get('status'))
#
#
# @pytest.mark.xfail(raises=ValueError)
# def test_contains_one_word_to_avoid_request_response(client, jwt, app):
#     words_list_classification = [{'word': 'ABC', 'classification': 'DIST'},
#                                  {'word': 'INVESTIGATORS', 'classification': 'DESC'}]
#     save_words_list_classification(words_list_classification)
#
#     words_list_virtual_word_condition = [{'words': 'ICPO, INTERPOL', 'consent_required': False, 'allow_use': False}]
#     save_words_list_virtual_word_condition(words_list_virtual_word_condition)
#
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = [
#         {
#             'name': 'ABC INTERPOL INVESTIGATORS INC.',
#             'location': 'BC',
#             'entity_type': 'CR',
#             'request_action': 'NEW'
#         }
#     ]
#
#     for entry in test_params:
#         query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
#         path = ENDPOINT_PATH + '?' + query
#         print('\n' + 'request: ' + path + '\n')
#         response = client.get(path, headers=headers)
#         payload = jsonpickle.decode(response.data)
#         print("Assert that the payload contains issues")
#         if isinstance(payload.get('issues'), list):
#             assert_issues_count_is_gt(0, payload.get('issues'))
#             assert_has_issue_type(AnalysisIssueCodes.WORDS_TO_AVOID, payload.get('issues'))
#
#
# @pytest.mark.xfail(raises=ValueError)
# def test_contains_more_than_one_word_to_avoid_request_response(client, jwt, app):
#     words_list_classification = [{'word': 'CANADIAN', 'classification': 'DIST'},
#                                  {'word': 'CANADIAN', 'classification': 'DESC'},
#                                  {'word': 'NATIONAL', 'classification': 'DIST'},
#                                  {'word': 'NATIONAL', 'classification': 'DESC'},
#                                  {'word': 'INVESTIGATORS', 'classification': 'DESC'}
#                                  ]
#     save_words_list_classification(words_list_classification)
#
#     words_list_virtual_word_condition = [{'words': 'ICPO, INTERPOL', 'consent_required': False, 'allow_use': False},
#                                          {'words': 'CANADIAN NATIONAL, CN', 'consent_required': False, 'allow_use': False}]
#     save_words_list_virtual_word_condition(words_list_virtual_word_condition)
#
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = [
#         {
#             'name': 'CANADIAN NATIONAL INTERPOL INVESTIGATORS INC.',
#             'location': 'BC',
#             'entity_type': 'CR',
#             'request_action': 'NEW'
#         }
#     ]
#
#     for entry in test_params:
#         query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
#         path = ENDPOINT_PATH + '?' + query
#         print('\n' + 'request: ' + path + '\n')
#         response = client.get(path, headers=headers)
#         payload = jsonpickle.decode(response.data)
#         print("Assert that the payload contains issues")
#         if isinstance(payload.get('issues'), list):
#             assert_issues_count_is_gt(0, payload.get('issues'))
#             assert_has_issue_type(AnalysisIssueCodes.WORDS_TO_AVOID, payload.get('issues'))
#
#
# @pytest.mark.xfail(raises=ValueError)
# def test_too_many_words_request_response(client, jwt, app):
#     words_list_classification = [{'word': 'MOUNTAIN', 'classification': 'DIST'},
#                                  {'word': 'MOUNTAIN', 'classification': 'DESC'},
#                                  {'word': 'VIEW', 'classification': 'DIST'},
#                                  {'word': 'VIEW', 'classification': 'DESC'},
#                                  {'word': 'FOOD', 'classification': 'DIST'},
#                                  {'word': 'FOOD', 'classification': 'DESC'},
#                                  {'word': 'GROWERS', 'classification': 'DIST'},
#                                  {'word': 'GROWERS', 'classification': 'DESC'},
#                                  {'word': 'CAFE', 'classification': 'DIST'},
#                                  {'word': 'CAFE', 'classification': 'DESC'}
#                                  ]
#     save_words_list_classification(words_list_classification)
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = [
#         {
#             'name': 'MOUNTAIN VIEW FOOD GROWERS & CAFE LTD.',
#             'location': 'BC',
#             'entity_type': 'CR',
#             'request_action': 'NEW'
#         }
#     ]
#
#     for entry in test_params:
#         query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
#         path = ENDPOINT_PATH + '?' + query
#         print('\n' + 'request: ' + path + '\n')
#         response = client.get(path, headers=headers)
#         payload = jsonpickle.decode(response.data)
#         print("Assert that the payload contains issues")
#         if isinstance(payload.get('issues'), list):
#             assert_issues_count_is_gt(0, payload.get('issues'))
#
#             for issue in payload.get('issues'):
#                 # Make sure only Well Formed name issues are being returned
#                 assert_issue_type_is_one_of([
#                     AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
#                     AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
#                     AnalysisIssueCodes.TOO_MANY_WORDS
#                 ], issue)
#
#         assert_has_issue_type(AnalysisIssueCodes.TOO_MANY_WORDS, payload.get('issues'))
#
#
# @pytest.mark.xfail(raises=ValueError)
# def test_contains_unclassifiable_word_request_response(client, jwt, app):
#     words_list_classification = [{'word': 'FINANCIAL', 'classification': 'DIST'},
#                                  {'word': 'FINANCIAL', 'classification': 'DESC'},
#                                  {'word': 'SOLUTIONS', 'classification': 'DIST'},
#                                  {'word': 'SOLUTIONS', 'classification': 'DESC'}
#                                  ]
#     save_words_list_classification(words_list_classification)
#
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = [
#         {
#             'name': 'INVINITY FINANCIAL SOLUTIONS INCORPORATED',
#             'location': 'BC',
#             'entity_type': 'CR',
#             'request_action': 'NEW'
#         }
#     ]
#
#     for entry in test_params:
#         query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
#
#         path = ENDPOINT_PATH + '?' + query
#         print('\n' + 'request: ' + path + '\n')
#         response = client.get(path, headers=headers)
#         payload = jsonpickle.decode(response.data)
#         print("Assert that the payload contains issues")
#         if isinstance(payload.get('issues'), list):
#             assert_issues_count_is_gt(0, payload.get('issues'))
#             assert_has_issue_type(AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD, payload.get('issues'))
#
#
# @pytest.mark.xfail(raises=ValueError)
# def test_contains_unclassifiable_words_request_response(client, jwt, app):
#     words_list_classification = [{'word': 'CONSULTING', 'classification': 'DIST'},
#                                  {'word': 'CONSULTING', 'classification': 'DESC'}
#                                  ]
#     save_words_list_classification(words_list_classification)
#
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = [
#         {
#             'name': 'FLERKIN BLUBBLUB CONSULTING INC.',
#             'location': 'BC',
#             'entity_type': 'CR',
#             'request_action': 'NEW'
#         }
#     ]
#
#     for entry in test_params:
#         query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
#
#         path = ENDPOINT_PATH + '?' + query
#         print('\n' + 'request: ' + path + '\n')
#         response = client.get(path, headers=headers)
#         payload = jsonpickle.decode(response.data)
#         print("Assert that the payload contains issues")
#         if isinstance(payload.get('issues'), list):
#             assert_issues_count_is_gt(0, payload.get('issues'))
#             assert_has_issue_type(AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD, payload.get('issues'))
#

@pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_request_response(client, jwt, app):
    words_list_classification = [{'word': 'ARMSTRONG', 'classification': 'DIST'},
                                 {'word': 'ARMSTRONG', 'classification': 'DESC'},
                                 {'word': 'PLUMBING', 'classification': 'DIST'},
                                 {'word': 'PLUMBING', 'classification': 'DESC'}
                                 ]
    save_words_list_classification(words_list_classification)

    name_list_db = ['ARMSTRONG PLUMBING & HEATING LTD.']
    save_words_list_name(name_list_db)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': 'ARMSTRONG PLUMBING LTD.',
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
            assert_has_issue_type(AnalysisIssueCodes.CORPORATE_CONFLICT, payload.get('issues'))


# # @pytest.mark.xfail(raises=ValueError)
# def test_designation_mismatch_request_response(client, jwt, app):
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = {
#         'name': 'MOUNTAIN VIEW FOOD GROWERS COOP',  # TODO: Test for all designation mismatches
#         'location': 'BC',
#         'entity_type': 'BC',
#         'request_type': 'NEW'
#     }
#
#     query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
#     path = ENDPOINT_PATH + '?' + query
#     print('\n' + 'request: ' + path + '\n')
#     response = client.get(path, headers=headers)
#     payload = jsonpickle.decode(response.data)
#     print("Assert that the payload contains issues")
#     if isinstance(payload.issues, list):
#         assert_issues_count_is_gt(0, payload.issues)
#         assert_has_issue_type(AnalysisIssueCodes.DESIGNATION_MISMATCH, payload.issues)
#
#
# # @pytest.mark.xfail(raises=ValueError)
# def test_name_requires_consent_request_response(client, jwt, app):
#     # create JWT & setup header with a Bearer Token using the JWT
#     token = jwt.create_jwt(claims, token_header)
#     headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
#
#     test_params = {
#         'name': 'MOUNTAIN VIEW FOOD ENGINEERING INC.',
#         'location': 'BC',
#         'entity_type': 'BC',
#         'request_type': 'NEW'
#     }
#
#     query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in test_params.items())
#     path = ENDPOINT_PATH + '?' + query
#     print('\n' + 'request: ' + path + '\n')
#     response = client.get(path, headers=headers)
#     payload = jsonpickle.decode(response.data)
#     print("Assert that the payload contains issues")
#     if isinstance(payload.issues, list):
#         assert_issues_count_is_gt(0, payload.issues)
#         assert_has_issue_type(AnalysisIssueCodes.NAME_REQUIRES_CONSENT, payload.issues)
#
#

#
#


def save_words_list_classification(words_list):
    from namex.models import WordClassification as WordClassificationDAO
    for record in words_list:
        wc = WordClassificationDAO()
        wc.classification = record['classification']
        wc.word = record['word']
        wc.start_dt = date.today()
        wc.approved_dt = date.today()
        wc.save_to_db()


def save_words_list_virtual_word_condition(words_list):
    from namex.models import VirtualWordCondition as VirtualWordConditionDAO
    for record in words_list:
        vwc = VirtualWordConditionDAO()
        vwc.rc_words = record['words']
        vwc.rc_consent_required = record['consent_required']
        vwc.rc_allow_use = record['allow_use']
        vwc.save_to_db()


def save_words_list_name(words_list):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User
    num = 0
    req = 1460775
    for record in words_list:
        nr_num_label = 'NR 000000'
        # add a user for the comment
        user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                    'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
        user.save_to_db()
        user_id = user.id

        nr = RequestDAO()
        num += 1
        nr_num = nr_num_label + str(num)
        nr.nrNum = nr_num
        nr.stateCd = State.INPROGRESS
        req += 1
        nr.requestId = req

        n = NameDAO()
        n.nr_id = nr.id
        n.choice = 1
        n.name = record
        n.state = State.APPROVED
        nr.names = [n]
        nr.save_to_db()
