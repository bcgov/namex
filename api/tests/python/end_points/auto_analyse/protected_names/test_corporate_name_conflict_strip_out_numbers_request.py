import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ...common import assert_issues_count_is_gt, assert_correct_conflict, save_words_list_name, \
    save_words_list_classification, assert_additional_conflict_parameters
from ..common import ENDPOINT_PATH
from ...common import token_header, claims


@pytest.mark.parametrize("name, expected",
                         [
                             ("NO. 295 CATHEDRAL VENTURES LTD.", "CATHEDRAL HOLDINGS LTD."),
                             ("NO. 295 SCS NO. 003 VENTURES LTD.", "SCS SOLUTIONS INC."),
                             ("2000 ARMSTRONG -- PLUMBING 2020 LTD.", "ARMSTRONG PLUMBING & HEATING LTD."),
                             ("ABC TWO PLUMBING ONE INC.", "ABC PLUMBING & HEATING LTD."),
                             ("SCS HOLDINGS INC.", "SCS SOLUTIONS INC."),
                             # NO LONGER VALID TEST SCENARIO, LUMBY IS NOT SYNONYM, THEN IT IS DISTINCTIVE AND IT
                             # DOES NOT PASS WELL FORMED NAME DUE TO <DIST><DIST>
                             ("RE/MAX LUMBY INC.", "REMAX LUMBY"),
                             # NO LONGER VALID TEST SCENARIO, LUMBY IS NOT SYNONYM, THEN IT IS DISTINCTIVE AND IT
                             # DOES NOT PASS WELL FORMED NAME DUE TO <DIST><DIST>
                             ("RE MAX LUMBY INC.", "REMAX LUMBY"),
                             ("468040 B.C. LTD.", "468040 BC LTD."),
                             ("S, C & S HOLDINGS INC.", "SCS SOLUTIONS INC."),
                             # ENGINEERING not found in synonyms, then considered a distintive, the only match obtained is
                             # EQTEC SOLUTIONS LTD. which is not close enough with current similarity score (0.6 vs 0.67 -->threshold)
                             ("EQTEC ENGINEERING & SOLUTIONS LTD.", "EQTEC ENGINEERING LTD.")
                         ]
                         )
@pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_strip_out_numbers_request_response(client, jwt, app, name, expected):
    words_list_classification = [{'word': 'CATHEDRAL', 'classification': 'DIST'},
                                 {'word': 'VENTURES', 'classification': 'DIST'},
                                 {'word': 'VENTURES', 'classification': 'DESC'},
                                 {'word': 'SCS', 'classification': 'DIST'},
                                 {'word': 'ARMSTRONG', 'classification': 'DIST'},
                                 {'word': 'ARMSTRONG', 'classification': 'DESC'},
                                 {'word': 'PLUMBING', 'classification': 'DIST'},
                                 {'word': 'PLUMBING', 'classification': 'DESC'},
                                 {'word': 'ABC', 'classification': 'DIST'},
                                 {'word': 'HOLDINGS', 'classification': 'DIST'},
                                 {'word': 'HOLDINGS', 'classification': 'DESC'},
                                 {'word': 'BC', 'classification': 'DIST'},
                                 {'word': 'BC', 'classification': 'DESC'},
                                 #{'word': '468040', 'classification': 'DIST'},
                                 {'word': 'EQTEC', 'classification': 'DIST'},
                                 {'word': 'ENGINEERING', 'classification': 'DIST'},
                                 {'word': 'ENGINEERING', 'classification': 'DESC'},
                                 {'word': 'SOLUTIONS', 'classification': 'DIST'},
                                 {'word': 'SOLUTIONS', 'classification': 'DESC'}
                                 ]
    save_words_list_classification(words_list_classification)

    conflict_list_db = ['CATHEDRAL VENTURES TRADING LTD.', 'CATHEDRAL HOLDINGS LTD.',
                        'SCS ENTERPRISES INTERNATIONAL', 'SCS SOLUTIONS INC.',
                        'ARMSTRONG PLUMBING & HEATING LTD.', 'ARMSTRONG COOLING & WAREHOUSE LTD.',
                        'ABC PLUMBING & HEATING LTD.', 'REMAX LUMBY', '468040 BC LTD.',
                        'EQTEC ENGINEERING LTD.', 'EQTEC SOLUTIONS LTD.']
    save_words_list_name(conflict_list_db)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': name,
            'location': 'BC',
            'entity_type': 'CR',
            'request_action': 'NEW'
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
