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
                             ("WESTWOOD FABRICARE DRY CLEANER LTD.", "WESTWOOD FABRICARE LAUNDRY LTD."),
                             ("WESTWOOD FABRICARE DRYCLEANER LTD.", "WESTWOOD FABRICARE LAUNDRY LTD."),
                             ("WESTWOOD FABRICARE DRY CLEANING LTD.", "WESTWOOD FABRICARE LAUNDRY LTD."),
                             ("WESTWOOD FABRICARE DRYCLEAN LTD.", "WESTWOOD FABRICARE LAUNDRY LTD."),
                             ("GARY DRY CLEANING LTD.", "GARY'S LAUNDRY INC."),
                             ("GARY DRYCLEANING LTD.", "GARY'S LAUNDRY INC."),
                             ('VANCOUVER ISLAND AUTOSPA LTD.','VANCOUVER ISLAND CAR WASH LTD.'),
                             ('VANCOUVER ISLAND AUTO SPA LTD.','VANCOUVER ISLAND CAR WASH LTD.'),
                             ('WESTWOOD PRE-SCHOOL DEVELOPMENT LTD.', 'WESTWOOD EARLY CHILDHOOD DEVELOPMENT LTD.'),
                             ('WESTWOOD BIOFUEL LTD.','WESTWOOD LIQUIFIED NATURAL GAS LTD.'),
                             ('WESTWOOD BIO FUEL LTD.','WESTWOOD LIQUIFIED NATURAL GAS LTD.'),
                             ('WESTWOOD BIO FUELING LTD.', 'WESTWOOD LIQUIFIED NATURAL GAS LTD.')
                         ]
                         )
@pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_compound_descriptive_response(client, jwt, app, name, expected):
    words_list_classification = [{'word': 'WESTWOOD', 'classification': 'DIST'},
                                 {'word': 'WESTWOOD', 'classification': 'DESC'},
                                 {'word': 'GARY', 'classification': 'DIST'},
                                 {'word': 'FABRICARE', 'classification': 'DESC'},
                                 {'word': 'DRY', 'classification': 'DIST'},
                                 {'word': 'DRY', 'classification': 'DESC'},
                                 {'word': 'CLEANER', 'classification': 'DIST'},
                                 {'word': 'CLEANER', 'classification': 'DESC'},
                                 {'word': 'CLEANING', 'classification': 'DIST'},
                                 {'word': 'CLEANING', 'classification': 'DESC'},
                                 {'word': 'LAUNDRY', 'classification': 'DIST'},
                                 {'word': 'LAUNDRY', 'classification': 'DESC'},
                                 {'word': 'VANCOUVER', 'classification': 'DIST'},
                                 {'word': 'VANCOUVER', 'classification': 'DESC'},
                                 {'word': 'ISLAND', 'classification': 'DIST'},
                                 {'word': 'ISLAND', 'classification': 'DESC'},
                                 {'word': 'AUTO', 'classification': 'DIST'},
                                 {'word': 'AUTO', 'classification': 'DESC'},
                                 {'word': 'SPA', 'classification': 'DIST'},
                                 {'word': 'SPA', 'classification': 'DESC'},
                                 {'word': 'CAR', 'classification': 'DIST'},
                                 {'word': 'CAR', 'classification': 'DESC'},
                                 {'word': 'WASH', 'classification': 'DIST'},
                                 {'word': 'WASH', 'classification': 'DESC'},
                                 {'word': 'SCHOOL', 'classification': 'DIST'},
                                 {'word': 'SCHOOL', 'classification': 'DESC'},
                                 {'word': 'EARLY', 'classification': 'DIST'},
                                 {'word': 'EARLY', 'classification': 'DESC'},
                                 {'word': 'CHILDHOOD', 'classification': 'DIST'},
                                 {'word': 'KIDS', 'classification': 'DIST'},
                                 {'word': 'KIDS', 'classification': 'DESC'},
                                 {'word': 'DEVELOPMENT', 'classification': 'DIST'},
                                 {'word': 'DEVELOPMENT', 'classification': 'DESC'},
                                 {'word': 'BIOFUEL', 'classification': 'DESC'},
                                 {'word': 'BIO', 'classification': 'DIST'},
                                 {'word': 'BIO', 'classification': 'DESC'},
                                 {'word': 'FUEL', 'classification': 'DIST'},
                                 {'word': 'FUEL', 'classification': 'DESC'},
                                 {'word': 'FUEL', 'classification': 'DIST'},
                                 {'word': 'FUEL', 'classification': 'DESC'},
                                 {'word': 'NATURAL', 'classification': 'DIST'},
                                 {'word': 'NATURAL', 'classification': 'DESC'},
                                 {'word': 'GAS', 'classification': 'DIST'},
                                 {'word': 'GAS', 'classification': 'DESC'},
                                 {'word': 'FUELING', 'classification': 'DIST'},
                                 ]
    save_words_list_classification(words_list_classification)

    conflict_list_db = ['WESTWOOD FABRICARE LAUNDRY LTD.', 'WESTWOOD FABRICS & WAREHOUSE LTD.',
                        'VANCOUVER ISLAND CAR WASH LTD.', 'VANCOUVER ISLAND CAR SERVICES LTD.',
                        'WESTWOOD EARLY CHILDHOOD DEVELOPMENT LTD.', 'WESTWOOD KIDS DEVELOPMENT LTD.',
                        'WESTWOOD LIQUIFIED NATURAL GAS LTD.', 'WESTWOOD NATURAL GAS PRODUCTS LTD.',
                        "GARY'S LAUNDRY INC.", "GARY'S CLEAN SOLUTION INC."]
    save_words_list_name(conflict_list_db)

    # create JWT & setup header with a Bearer Token using the JWT
    # token = jwt.create_jwt(claims, token_header)
    # headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

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
        response = client.get(path, headers={})  # response = client.get(path, headers=headers)
        payload = jsonpickle.decode(response.data)
        print("Assert that the payload contains issues")
        if isinstance(payload.get('issues'), list):
            payload_lst = payload.get('issues')
            assert_issues_count_is_gt(0, payload_lst)
            assert_correct_conflict(AnalysisIssueCodes.CORPORATE_CONFLICT, payload_lst, expected)
            assert_additional_conflict_parameters(AnalysisIssueCodes.CORPORATE_CONFLICT, payload_lst)
