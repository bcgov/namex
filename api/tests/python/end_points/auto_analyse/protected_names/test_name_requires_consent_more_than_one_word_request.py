from urllib.parse import quote_plus

import jsonpickle
import pytest

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ...common import claims, token_header
from ..common import (
    assert_has_word_upper,
    assert_issues_count_is_gt,
    save_words_list_classification,
    save_words_list_virtual_word_condition,
)
from ..configuration import ENDPOINT_PATH


@pytest.mark.xfail(raises=ValueError)
def test_name_requires_consent_more_than_one_word_request_response(client, jwt, app):
    words_list_classification = [
        {'word': 'BLAKE', 'classification': 'DIST'},
        {'word': 'BLAKE', 'classification': 'DESC'},
        {'word': 'ENGINEERING', 'classification': 'DIST'},
        {'word': 'ENGINEERING', 'classification': 'DESC'},
        {'word': 'EQTEC', 'classification': 'DIST'},
        {'word': 'ECOMMERCE', 'classification': 'DIST'},
        {'word': 'ECOMMERCE', 'classification': 'DESC'},
        {'word': 'SOLUTIONS', 'classification': 'DIST'},
        {'word': 'SOLUTIONS', 'classification': 'DESC'},
    ]
    save_words_list_classification(words_list_classification)

    words_list_virtual_word_condition = [
        {'words': '4H', 'consent_required': True, 'allow_use': True},
        {
            'words': 'CONSULTING ENGINEER, ENGINEER, ENGINEERING, INGENIERE, INGENIEUR, INGENIEUR CONSIEL, P ENG, PROFESSIONAL ENGINEER',
            'consent_required': True,
            'allow_use': True,
        },
        {'words': 'HONEYWELL', 'consent_required': True, 'allow_use': True},
    ]
    save_words_list_virtual_word_condition(words_list_virtual_word_condition)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': 'BLAKE 4H ENGINEERING ECOMMERCE LTD.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW',
        },
        {
            'name': 'EQTEC HONEYWELL ENGINEERING SOLUTIONS LTD.',
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
            assert_has_word_upper(AnalysisIssueCodes.NAME_REQUIRES_CONSENT, payload.get('issues'))
