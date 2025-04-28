from urllib.parse import quote_plus

import jsonpickle
import pytest

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ...common import claims, token_header
from ..common import (
    assert_has_designations_upper,
    assert_has_no_issue_type,
    assert_issues_count_is_gt,
    save_words_list_classification,
)
from ..configuration import ENDPOINT_PATH


@pytest.mark.xfail(raises=ValueError)
def test_end_designation_more_than_once_request_response(client, jwt, app):
    words_list_classification = [
        {'word': 'ARMSTRONG', 'classification': 'DIST'},
        {'word': 'ARMSTRONG', 'classification': 'DESC'},
        {'word': 'PLUMBING', 'classification': 'DIST'},
        {'word': 'PLUMBING', 'classification': 'DESC'},
    ]
    save_words_list_classification(words_list_classification)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {'name': 'ARMSTRONG LTD. PLUMBING INC.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {
            'name': 'LTD. ARMSTRONG CORPORATION PLUMBING INC.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
        {
            'name': 'ARMSTRONG LTD. CORPORATION PLUMBING INC.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
        {
            'name': 'ARMSTRONG LTD. CORPORATION INC. PLUMBING',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
        {
            'name': 'LTD. COOP ARMSTRONG L.L.C. CORPORATION PLUMBING CCC INC.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
        {
            'name': 'ARMSTRONG LTD. COOP L.L.C. CORPORATION LLP INC. PLUMBING  ',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
        {
            'name': 'ARMSTRONG LTD. COOP L.L.C. CORPORATION LLP PLUMBING INC.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
        {'name': 'ARMSTRONG PLUMBING LTD. INC.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {
            'name': 'ARMSTRONG PLUMBING LTD. INC. CORPORATION',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
        {
            'name': 'ARMSTRONG LIMITED LIABILITY COMPANY PLUMBING COOP LIMITED INC. CORPORATION',
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
            assert_has_designations_upper(AnalysisIssueCodes.END_DESIGNATION_MORE_THAN_ONCE, payload.get('issues'))
            assert_has_no_issue_type(AnalysisIssueCodes.DESIGNATION_MISPLACED, payload.get('issues'))
