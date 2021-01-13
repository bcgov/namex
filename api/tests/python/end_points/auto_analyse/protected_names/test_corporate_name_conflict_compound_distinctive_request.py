import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..common import assert_issues_count_is_gt, assert_correct_conflict, save_words_list_name, \
    save_words_list_classification, assert_additional_conflict_parameters
from ..configuration import ENDPOINT_PATH
from ...common import token_header, claims


@pytest.mark.parametrize("name, expected",
                         [
                             ("SOUTH LAND BERRY FARMS LTD.", "SOUTHLAND BERRY FARMS LTD."),
                             ("SOUTH LAND FREIGHTWAYS LTD.", "SOUTHLAND FREIGHTWAYS LTD."),
                             ("SOUTH LAND FREIGHT WAYS LTD.", "SOUTHLAND FREIGHTWAYS LTD."),
                             ("SOUTH LAND RESTAURANT LTD.", "SOUTHLANDS CAFE LTD."),
                             ("SOUTHLANDS PLUMBING LTD.", "AMERICA SOUTH LAND MECHANICAL LTD."),
                             ("SOUTH NORTH BERRY PUB LTD.", "SOUTHNORTH PUB LTD."),
                             ("SOUTHNORTH VANCOUVER CAFE LTD.", "SOUTH NORTH CAFE LTD.")
                         ]
                         )
@pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_compound_distinctive_request_response(client, jwt, app, name, expected):
    words_list_classification = [{'word': 'SOUTH', 'classification': 'DIST'},
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
                                 {'word': 'RESTAURANT', 'classification': 'DIST'},
                                 {'word': 'RESTAURANT', 'classification': 'DESC'},
                                 {'word': 'CAFE', 'classification': 'DIST'},
                                 {'word': 'CAFE', 'classification': 'DESC'},
                                 {'word': 'PUB', 'classification': 'DIST'},
                                 {'word': 'PUB', 'classification': 'DESC'},
                                 {'word': 'CLUB', 'classification': 'DIST'},
                                 {'word': 'CLUB', 'classification': 'DESC'},
                                 {'word': 'VANCOUVER', 'classification': 'DIST'},
                                 {'word': 'VANCOUVER', 'classification': 'DESC'},
                                 {'word': 'PLUMBING', 'classification': 'DIST'},
                                 {'word': 'PLUMBING', 'classification': 'DESC'},
                                 {'word': 'HEATING', 'classification': 'DIST'},
                                 {'word': 'HEATING', 'classification': 'DESC'},
                                 ]
    save_words_list_classification(words_list_classification)

    conflict_list_db = ['SOUTHLAND BERRY FARMS LTD.', 'SOUTHLAND FREIGHTWAYS LTD.', 'SOUTHLANDS RATEPAYERS LTD.',
                        'SOUTHLANDS CAFE LTD.', "SOUTHNORTH PUB LTD.", "SOUTH NORTH CAFE LTD.",
                        "AMERICA SOUTH LAND MECHANICAL LTD."]

    save_words_list_name(conflict_list_db)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': name,
            'location': 'BC',
            'entity_type_cd': 'CR',
            'request_action_cd': 'NEW'
        }
    ]

    for entry in test_params:
        query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
        path = ENDPOINT_PATH + '?' + query
        print('\n' + 'request: ' + path + '\n')
        response = client.get(path, headers=headers)
        payload = jsonpickle.decode(response.data)
        print("Assert that the payload contains issues")
        if isinstance(payload.get('issues'), list):
            payload_lst = payload.get('issues')
            assert_issues_count_is_gt(0, payload_lst)
            assert_correct_conflict(AnalysisIssueCodes.CORPORATE_CONFLICT, payload_lst, expected)
            assert_additional_conflict_parameters(AnalysisIssueCodes.CORPORATE_CONFLICT, payload_lst)
