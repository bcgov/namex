from urllib.parse import quote_plus

import jsonpickle
import pytest

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from .... import integration_synonym_api
from ...common import claims, token_header
from ..common import assert_has_designations_upper, assert_issues_count_is_gt, save_words_list_classification
from ..configuration import ENDPOINT_PATH


@integration_synonym_api
@pytest.mark.xfail(raises=ValueError)
def test_designation_existence_request_response(client, jwt, app):
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

    test_params = [{'name': 'ARMSTRONG PLUMBING', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'}]

    for entry in test_params:
        query = '&'.join('{!s}={}'.format(k, quote_plus(v)) for (k, v) in entry.items())
        path = ENDPOINT_PATH + '?' + query
        print('\n' + 'request: ' + path + '\n')
        response = client.get(path, headers=headers)
        payload = jsonpickle.decode(response.data)
        print('Assert that the payload contains issues')
        if isinstance(payload.get('issues'), list):
            assert_issues_count_is_gt(0, payload.get('issues'))
            assert_has_designations_upper(AnalysisIssueCodes.DESIGNATION_NON_EXISTENT, payload.get('issues'))
