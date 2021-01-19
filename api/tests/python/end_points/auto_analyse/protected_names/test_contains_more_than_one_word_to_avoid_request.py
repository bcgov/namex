import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..common import assert_issues_count_is_gt, assert_has_word_upper, save_words_list_classification, save_words_list_virtual_word_condition
from ..configuration import ENDPOINT_PATH
from ...common import token_header, claims


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
    # token = jwt.create_jwt(claims, token_header)
    # headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': 'CANADIAN NATIONAL INTERPOL INVESTIGATORS INC.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW'
        }
    ]

    for entry in test_params:
        query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
        path = ENDPOINT_PATH + '?' + query
        print('\n' + 'request: ' + path + '\n')
        response = client.get(path, headers={})  # response = client.get(path, headers=headers)
        payload = jsonpickle.decode(response.data)
        print("Assert that the payload contains issues")
        if isinstance(payload.get('issues'), list):
            assert_issues_count_is_gt(0, payload.get('issues'))
            assert_has_word_upper(AnalysisIssueCodes.WORDS_TO_AVOID, payload.get('issues'))
