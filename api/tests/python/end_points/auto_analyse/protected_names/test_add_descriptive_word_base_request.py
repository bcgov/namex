import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..common import assert_issues_count_is_gt, assert_issue_type_is_one_of, assert_has_word_upper, save_words_list_classification
from ..configuration import ENDPOINT_PATH
from ...common import token_header, claims


# 2.- Unique word classified as distinctive
@pytest.mark.xfail(raises=ValueError)
def test_add_descriptive_word_base_request_response(client, jwt, app):
    words_list_classification = [{'word': 'COSTAS', 'classification': 'DIST'},
                                 {'word': 'ABC', 'classification': 'DIST'}]
    save_words_list_classification(words_list_classification)

    # create JWT & setup header with a Bearer Token using the JWT
    # token = jwt.create_jwt(claims, token_header)
    # headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': 'COSTAS INC.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW'
        },
        {
            'name': 'ABC INC.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW'
        }
    ]

    for entry in test_params:
        query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())

        path = ENDPOINT_PATH + '?' + query
        print('\n' + 'request: ' + path + '\n')
        response = client.get(path, headers={})  # response = client.get(path, headers=headers)
        payload = jsonpickle.decode(response.data)
        print("Assert that the payload contains issues")
        if isinstance(payload.get('issues'), list):
            assert_issues_count_is_gt(0, payload.get('issues'))

            for issue in payload.get('issues'):
                # Make sure only Well Formed name issues are being returned
                assert_issue_type_is_one_of([
                    AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
                    AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
                    AnalysisIssueCodes.TOO_MANY_WORDS
                ], issue)

            assert_has_word_upper(AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD, payload.get('issues'))
