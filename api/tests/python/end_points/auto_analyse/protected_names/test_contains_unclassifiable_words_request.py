import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ...common import assert_issues_count_is_gt, assert_has_word_upper, save_words_list_classification
from ..common import ENDPOINT_PATH
from ...common import token_header, claims


@pytest.mark.xfail(raises=ValueError)
def test_contains_unclassifiable_words_request_response(client, jwt, app):
    words_list_classification = [{'word': 'CONSULTING', 'classification': 'DIST'},
                                 {'word': 'CONSULTING', 'classification': 'DESC'}
                                 ]
    save_words_list_classification(words_list_classification)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': 'FLERKIN BLUBBLUB CONSULTING INC.',
            'location': 'BC',
            'entity_type': 'CR',
            'request_action': 'NEW'
        },
        {
            'name': 'FLERKIN BLUBBLUB BAKERY INC.',
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
            assert_has_word_upper(AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD, payload.get('issues'))
