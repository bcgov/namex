from urllib.parse import quote_plus

import jsonpickle
import pytest

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from .... import integration_synonym_api
from ...common import claims, token_header
from ..common import (
    assert_has_word_upper,
    assert_issues_count_is_gt,
    save_words_list_classification,
    save_words_list_virtual_word_condition,
)
from ..configuration import ENDPOINT_PATH


@integration_synonym_api
@pytest.mark.xfail(raises=ValueError)
def test_name_use_special_words_request_response(client, jwt, app):
    words_list_classification = [
        {'word': 'BC', 'classification': 'DIST'},
        {'word': 'BC', 'classification': 'DESC'},
        # {'word': '468040', 'classification': 'DIST'},
        {'word': 'COAST', 'classification': 'DIST'},
        {'word': 'COAST', 'classification': 'DESC'},
        {'word': 'TREASURY', 'classification': 'DISC'},
        {'word': 'TREASURY', 'classification': 'DESC'},
    ]
    save_words_list_classification(words_list_classification)

    words_list_virtual_word_condition = [
        {
            'words': 'B C, B C S, BC, BC S, BCPROVINCE, BRITISH COLUMBIA, BRITISHCOLUMBIA, PROVINCIAL',
            'consent_required': False,
            'allow_use': True,
        },
        {'words': 'TREASURY', 'consent_required': False, 'allow_use': True},
    ]
    save_words_list_virtual_word_condition(words_list_virtual_word_condition)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {'name': '468040 BC LTD.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'},
        {
            'name': 'COAST ANGULARS TREASURY INCORPORATED',
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
            assert_has_word_upper(AnalysisIssueCodes.WORD_SPECIAL_USE, payload.get('issues'))
