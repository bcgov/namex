import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..common import (
    assert_issues_count_is_gt,
    assert_issue_type_is_one_of,
    assert_has_word_upper,
    save_words_list_classification,
)
from ..configuration import ENDPOINT_PATH
from ...common import token_header, claims


# 1.- Unique word classified as descriptive
@pytest.mark.xfail(raises=ValueError)
def test_add_distinctive_word_base_request_response(client, jwt, app):
    words_list_classification = [
        {'word': 'CARPENTRY', 'classification': 'DESC'},
        {'word': 'HEATING', 'classification': 'DESC'},
        {'word': 'ADJUSTERS', 'classification': 'DESC'},
        {'word': 'COFFEE', 'classification': 'DIST'},
        {'word': 'COFFEE', 'classification': 'DESC'},
        {'word': 'SHOP', 'classification': 'DIST'},
        {'word': 'SHOP', 'classification': 'DESC'},
        {'word': 'AUTO', 'classification': 'DIST'},
        {'word': 'AUTO', 'classification': 'DESC'},
        {'word': 'BODY', 'classification': 'DIST'},
        {'word': 'BODY', 'classification': 'DESC'},
        {'word': 'GARAGE', 'classification': 'DIST'},
        {'word': 'GARAGE', 'classification': 'DESC'},
        {'word': 'KITCHEN', 'classification': 'DIST'},
        {'word': 'KITCHEN', 'classification': 'DESC'},
        {'word': 'FOOD', 'classification': 'DIST'},
        {'word': 'FOOD', 'classification': 'DESC'},
        {'word': 'CAR', 'classification': 'DIST'},
        {'word': 'CAR', 'classification': 'DESC'},
        {'word': 'WASH', 'classification': 'DIST'},
        {'word': 'WASH', 'classification': 'DESC'},
        {'word': 'CENTRAL', 'classification': 'DIST'},
        {'word': 'CENTRAL', 'classification': 'DESC'},
        {'word': 'PACIFIC', 'classification': 'DIST'},
        {'word': 'PACIFIC', 'classification': 'DESC'},
        {'word': 'CAPITAL', 'classification': 'DIST'},
        {'word': 'CAPITAL', 'classification': 'DESC'},
        {'word': 'IDEAS', 'classification': 'DIST'},
        {'word': 'IDEAS', 'classification': 'DESC'},
    ]

    save_words_list_classification(words_list_classification)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {'name': 'CARPENTRY INC.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {'name': 'HEATING LIMITED', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {'name': 'ADJUSTERS LTD.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        # When checking synonyms dist=['victoria'], desc=['properties']. Because if there are descriptive items before distinctive, these become distinctive as well:
        # dist=['victoria','properties']. There are no conflicts, then a descriptive is missing, not a distinctive. This test case is moved to test_add_descriptive_word_both_classification_request.py
        # {'name': 'PROPERTIES OF VICTORIA LTD.',
        #  'location': 'BC',
        #  'entity_type_cd': 'CR',
        #  'request_action_cd': 'NEW'
        #  },
        {'name': 'COFFEE SHOP INC', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {'name': 'AUTO BODY GARAGE LTD.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        # When checking synonyms dist=['service'], desc=['sewing']. Because if there are descriptive items before distinctive, these become distinctive as well:
        # dist=['sewing','service']. There are no conflicts, then a descriptive is missing, not a distinctive. This test case is moved to test_add_descriptive_word_both_classification_request.py
        # {'name': 'SEWING SERVICE LTD.',
        #  'location': 'BC',
        #  'entity_type_cd': 'CR',
        #  'request_action_cd': 'NEW'
        #  },
        {'name': 'KITCHEN FOOD LTD.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {'name': 'CAR WASH CENTRAL LTD.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {'name': 'AUTO BODY PACIFIC LTD.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {'name': 'CAPITAL IDEAS LTD.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
    ]

    for entry in test_params:
        query = '&'.join('{!s}={}'.format(k, quote_plus(v)) for (k, v) in entry.items())

        path = ENDPOINT_PATH + '?' + query
        print('\n' + 'request: ' + path + '\n')
        response = client.get(path, headers=headers)
        payload = jsonpickle.decode(response.data)
        print('Assert that the payload contains issues')
        if isinstance(payload.get('issues'), list):
            assert_issues_count_is_gt(0, payload.get('issues'))

            for issue in payload.get('issues'):
                # Make sure only Well Formed name issues are being returned
                assert_issue_type_is_one_of(
                    [
                        AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
                        AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
                        AnalysisIssueCodes.TOO_MANY_WORDS,
                    ],
                    issue,
                )

            assert_has_word_upper(AnalysisIssueCodes.ADD_DISTINCTIVE_WORD, payload.get('issues'))
