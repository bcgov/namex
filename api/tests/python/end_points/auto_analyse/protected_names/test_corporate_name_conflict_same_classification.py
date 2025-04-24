import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..common import (
    assert_issues_count_is_gt,
    assert_issue_type_is_one_of,
    assert_has_word_upper,
    save_words_list_classification,
    save_words_list_name,
    assert_correct_conflict,
    assert_additional_conflict_parameters,
)
from ..configuration import ENDPOINT_PATH
from ...common import token_header, claims


@pytest.mark.parametrize(
    'name, expected',
    [
        ('BABY DOG CAFE LTD.', 'BABY DOG CAFE LTD.'),
        ('VALLEY VIEW HOME LTD.', 'VALLEY VIEW REALTY LTD.'),
    ],
)
@pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_same_classification_request_response(client, jwt, app, name, expected):
    words_list_classification = [
        {'word': 'BABY', 'classification': 'DIST'},
        {'word': 'BABY', 'classification': 'DESC'},
        {'word': 'DOG', 'classification': 'DIST'},
        {'word': 'DOG', 'classification': 'DESC'},
        {'word': 'CAFE', 'classification': 'DIST'},
        {'word': 'CAFE', 'classification': 'DESC'},
        {'word': 'RESTAURANT', 'classification': 'DIST'},
        {'word': 'RESTAURANT', 'classification': 'DESC'},
        {'word': 'VALLEY', 'classification': 'DIST'},
        {'word': 'VALLEY', 'classification': 'DESC'},
        {'word': 'VIEW', 'classification': 'DIST'},
        {'word': 'VIEW', 'classification': 'DESC'},
        {'word': 'HOME', 'classification': 'DIST'},
        {'word': 'HOME', 'classification': 'DESC'},
        {'word': 'REALTY', 'classification': 'DIST'},
        {'word': 'REALTY', 'classification': 'DESC'},
    ]

    save_words_list_classification(words_list_classification)

    conflict_list_db = [
        'BABY DOG CAFE LTD.',
        'BABY DOG CAFE RESTAURANT LTD.',
        'VALLEY VIEW REALTY LTD.',
        'VALLEY DOUGLAS REALTY LTD.',
    ]
    save_words_list_name(conflict_list_db)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    """
    Name is longer than two words we can adjust the classification when all words are in the same classification:
    - If they are all classified as DIST and the last word is classified as both DIST, DESC than we can change the last word to DESC.
    - If they are all DESC an dthe first word is classified as both DIST and DESC we will classify the first word as DIST.
    """
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
