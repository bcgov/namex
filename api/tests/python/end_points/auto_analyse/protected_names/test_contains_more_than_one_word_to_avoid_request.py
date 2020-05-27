import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.models import User
from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..common import assert_issues_count_is_gt, assert_has_word_upper, save_words_list_classification, save_words_list_virtual_word_condition

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

@pytest.mark.xfail(raises=ValueError)
def test_contains_more_than_one_word_to_avoid_request_response(client, jwt, app):
    words_list_classification = [{'word': 'CANADIAN', 'classification': 'DIST'},
                                 {'word': 'CANADIAN', 'classification': 'DESC'},
                                 {'word': 'NATIONAL', 'classification': 'DIST'},
                                 {'word': 'NATIONAL', 'classification': 'DESC'},
                                 {'word': 'INVESTIGATORS', 'classification': 'DESC'}
                                 ]
    save_words_list_classification(words_list_classification)

    words_list_virtual_word_condition = [{'words': 'ICPO, INTERPOL', 'consent_required': False, 'allow_use': False},
                                         {'words': 'CANADIAN NATIONAL, CN', 'consent_required': False,
                                          'allow_use': False}]
    save_words_list_virtual_word_condition(words_list_virtual_word_condition)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': 'CANADIAN NATIONAL INTERPOL INVESTIGATORS INC.',
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
            assert_has_word_upper(AnalysisIssueCodes.WORDS_TO_AVOID, payload.get('issues'))
