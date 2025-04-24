from urllib.parse import quote_plus

import jsonpickle
import pytest

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ...common import claims, token_header
from ..common import (
    assert_has_issue_type,
    assert_issues_count_is_gt,
    save_words_list_classification,
    save_words_list_virtual_word_condition,
)
from ..configuration import ENDPOINT_PATH


@pytest.mark.xfail(raises=ValueError)
def test_designation_mismatch_one_word_with_hyphen_request_response(client, jwt, app):
    words_list_classification = [
        {'word': 'ARMSTRONG', 'classification': 'DIST'},
        {'word': 'ARMSTRONG', 'classification': 'DESC'},
        {'word': 'PLUMBING', 'classification': 'DIST'},
        {'word': 'PLUMBING', 'classification': 'DESC'},
    ]
    save_words_list_classification(words_list_classification)

    words_list_virtual_word_condition = [
        {'words': 'CO OP, CO OPERATIVES, COOP, COOPERATIVES', 'consent_required': False, 'allow_use': True}
    ]
    save_words_list_virtual_word_condition(words_list_virtual_word_condition)
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {'name': 'ARMSTRONG CO-OP PLUMBING', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {
            'name': 'ARMSTRONG CO-OPERATIVE PLUMBING',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
        {'name': 'ARMSTRONG PLUMBING L.L.C.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {'name': 'ARMSTRONG L.L.C. PLUMBING', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {
            'name': 'ARMSTRONG PLUMBING LIMITED LIABILITY CO.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
        {
            'name': 'ARMSTRONG PLUMBING L.L.C. INC.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
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
            assert_has_issue_type(AnalysisIssueCodes.DESIGNATION_MISMATCH, payload.get('issues'))
