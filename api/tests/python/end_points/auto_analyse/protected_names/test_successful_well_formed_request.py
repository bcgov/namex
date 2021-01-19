import pytest
import jsonpickle

from urllib.parse import quote_plus

from ..common import save_words_list_classification
from ..configuration import ENDPOINT_PATH
from ...common import token_header, claims


# 5.- Successful well formed name:
@pytest.mark.xfail(raises=ValueError)
def test_successful_well_formed_request_response(client, jwt, app):
    words_list_classification = [{'word': 'ADEA', 'classification': 'DIST'},
                                 {'word': 'HEATING', 'classification': 'DESC'},
                                 {'word': 'ABC', 'classification': 'DIST'},
                                 {'word': 'PLUMBING', 'classification': 'DIST'},
                                 {'word': 'PLUMBING', 'classification': 'DESC'}
                                 ]
    save_words_list_classification(words_list_classification)

    # create JWT & setup header with a Bearer Token using the JWT
    # token = jwt.create_jwt(claims, token_header)
    # headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': 'ADEA HEATING INC.',
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW'
        },
        {
            'name': 'ABC PLUMBING INC.',
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
        print("Assert that the payload status is Available")
        assert ('Available', payload.get('status'))
