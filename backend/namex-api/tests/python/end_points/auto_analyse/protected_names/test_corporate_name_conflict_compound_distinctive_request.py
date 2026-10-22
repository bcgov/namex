from urllib.parse import quote_plus

import jsonpickle
import pytest

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from .... import integration_solr
from ...common import claims, token_header
from ..common import (
    assert_additional_conflict_parameters,
    assert_correct_conflict,
    assert_issues_count_is_gt,
    save_words_list_classification,
    save_words_list_name,
)
from ..configuration import ENDPOINT_PATH


@pytest.mark.parametrize(
    'name, expected',
    [
        ('SOUTH LAND BERRY FARMS LTD.', 'SOUTHLAND BERRY FARMS LTD.'),
        ('SOUTH LAND FREIGHTWAYS LTD.', 'SOUTHLAND FREIGHTWAYS LTD.'),
        ('SOUTH LAND FREIGHT WAYS LTD.', 'SOUTHLAND FREIGHTWAYS LTD.'),
    ],
)
@integration_solr
@pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_compound_distinctive_request_response(client, jwt, app, name, expected):
    words_list_classification = [
        {'word': 'SOUTH', 'classification': 'DIST'},
        {'word': 'SOUTH', 'classification': 'DESC'},
        {'word': 'LAND', 'classification': 'DIST'},
        {'word': 'LAND', 'classification': 'DESC'},
        {'word': 'BERRY', 'classification': 'DIST'},
        {'word': 'BERRY', 'classification': 'DESC'},
        {'word': 'FARMS', 'classification': 'DIST'},
        {'word': 'FARMS', 'classification': 'DESC'},
        {'word': 'FREIGHT', 'classification': 'DIST'},
        {'word': 'FREIGHT', 'classification': 'DESC'},
        {'word': 'WAYS', 'classification': 'DIST'},
        {'word': 'WAYS', 'classification': 'DESC'},
        {'word': 'LANDS', 'classification': 'DIST'},
        {'word': 'LANDS', 'classification': 'DESC'},
    ]
    save_words_list_classification(words_list_classification)

    conflict_list_db = ['SOUTHLAND BERRY FARMS LTD.', 'SOUTHLAND FREIGHTWAYS LTD.', 'SOUTHLANDS RATEPAYERS LTD.']
    save_words_list_name(conflict_list_db)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [{'name': name, 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'}]

    for entry in test_params:
        query = '&'.join('{!s}={}'.format(k, quote_plus(v)) for (k, v) in entry.items())
        path = ENDPOINT_PATH + '?' + query
        print('\n' + 'request: ' + path + '\n')
        response = client.get(path, headers=headers)
        payload = jsonpickle.decode(response.data)
        print('Assert that the payload contains issues')
        if isinstance(payload.get('issues'), list):
            payload_lst = payload.get('issues')
            assert_issues_count_is_gt(0, payload_lst)
            assert_correct_conflict(AnalysisIssueCodes.CORPORATE_CONFLICT, payload_lst, expected)
            assert_additional_conflict_parameters(AnalysisIssueCodes.CORPORATE_CONFLICT, payload_lst)
