import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..common import assert_issues_count_is_gt, assert_correct_conflict, save_words_list_name, \
    save_words_list_classification, assert_additional_conflict_parameters
from ..common import ENDPOINT_PATH
from ..common import token_header, claims


@pytest.mark.parametrize("name, expected",
                         [
                             ("ARMSTRONG PLUMBING LTD.", "ARMSTRONG PLUMBING & HEATING LTD."),
                             ("ABC CONSULTING LTD.", "ABC INTERNATIONAL CONSULTING LTD.")
                         ]
                         )
@pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_request_response(client, jwt, app, name, expected):
    words_list_classification = [{'word': 'ARMSTRONG', 'classification': 'DIST'},
                                 {'word': 'ARMSTRONG', 'classification': 'DESC'},
                                 {'word': 'PLUMBING', 'classification': 'DIST'},
                                 {'word': 'PLUMBING', 'classification': 'DESC'},
                                 {'word': 'ABC', 'classification': 'DIST'},
                                 {'word': 'CONSULTING', 'classification': 'DIST'},
                                 {'word': 'CONSULTING', 'classification': 'DESC'}
                                 ]
    save_words_list_classification(words_list_classification)

    conflict_list_db = ['ARMSTRONG PLUMBING & HEATING LTD.', 'ARMSTRONG COOLING & WAREHOUSE LTD.',
                        'ABC PEST MANAGEMENT CONSULTING INC.', 'ABC ALWAYS BETTER CONSULTING INC.',
                        'ABC - AUTISM BEHAVIOUR CONSULTING INCORPORATED', 'ABC INTERNATIONAL CONSULTING LTD.']
    save_words_list_name(conflict_list_db)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': name,
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
            payload_lst = payload.get('issues')
            assert_issues_count_is_gt(0, payload_lst)
            assert_correct_conflict(AnalysisIssueCodes.CORPORATE_CONFLICT, payload_lst, expected)
            assert_additional_conflict_parameters(AnalysisIssueCodes.CORPORATE_CONFLICT, payload_lst)
