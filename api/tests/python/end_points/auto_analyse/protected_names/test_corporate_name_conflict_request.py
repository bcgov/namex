import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..common import (
    assert_issues_count_is_gt,
    assert_correct_conflict,
    save_words_list_name,
    save_words_list_classification,
    assert_additional_conflict_parameters,
)
from ..configuration import ENDPOINT_PATH
from ...common import token_header, claims


@pytest.mark.parametrize(
    'name, expected',
    [
        ('ARMSTRONG PLUMBING LTD.', 'ARMSTRONG PLUMBING & HEATING LTD.'),
        # # ("ABC CONSULTING LTD.", "ABC INTERNATIONAL CONSULTING LTD."), #Under evaluation
        ('NO. 001 CATHEDRAL MINING LTD.', 'CATHEDRAL MINING LTD.'),
        ('ARMSTRONG PLUMBING & CAFE INC.', 'ARMSTRONG PLUMBING & HEATING LTD.'),
        # Stand-alone names are approved as long as they have an additional distinctive or descriptive.
        # The only way to be rejected is to have an exact match. We need to implement an exact match for
        # Stand-alone names to avoid comparing with many names, just exact matches should be returned.
        # ("PACIFIC BLUE ENGINEERING & ENTERPRISES LTD.", "PACIFIC BLUE ENTERPRISES LTD."),
        ('LE BLUE CAFE LTD.', 'LE BLUE FOX CAFE INC.'),
        ('SWIFT EDUCATION SERVICES LTD', 'CANADA SWIFT INTERNATIONAL EDUCATION CORP.'),
        ('CANDID CONSULTING SERVICES LTD.', 'CANDID COMMUNITY CONSULTING CORP.'),
        ('SMART SUPPLY LTD.', 'COASTAL SMART SUPPLIES LTD.'),
        ('AAA POWER WASHING LTD.', 'AAA STREAMLINE POWER WASHING TRUCKING LTD.'),
        ('AAA POWER WASHING LTD.', 'AAA STREAMLINE POWER WASHING TRUCKING LTD.'),
        ('PIONEERS OF FLOORING LTD.', 'PIONEER FLOOR COVERING LTD.'),
        ('CHAMPIONS OF FLOORING LTD.', 'CHAMPION HARDWOOD FLOORS LTD.'),
    ],
)
@pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_request_response(client, jwt, app, name, expected):
    words_list_classification = [
        {'word': 'ARMSTRONG', 'classification': 'DIST'},
        {'word': 'ARMSTRONG', 'classification': 'DESC'},
        {'word': 'PLUMBING', 'classification': 'DIST'},
        {'word': 'PLUMBING', 'classification': 'DESC'},
        {'word': 'ABC', 'classification': 'DIST'},
        {'word': 'CONSULTING', 'classification': 'DIST'},
        {'word': 'CONSULTING', 'classification': 'DESC'},
        {'word': 'CATHEDRAL', 'classification': 'DIST'},
        {'word': 'MINING', 'classification': 'DIST'},
        {'word': 'MINING', 'classification': 'DESC'},
        {'word': 'INVESTMENTS', 'classification': 'DIST'},
        {'word': 'INVESTMENTS', 'classification': 'DESC'},
        {'word': 'CAFE', 'classification': 'DIST'},
        {'word': 'CAFE', 'classification': 'DESC'},
        {'word': 'PACIFIC', 'classification': 'DIST'},
        {'word': 'PACIFIC', 'classification': 'DESC'},
        {'word': 'BLUE', 'classification': 'DIST'},
        {'word': 'ENGINEERING', 'classification': 'DIST'},
        {'word': 'ENGINEERING', 'classification': 'DESC'},
        {'word': 'ENTERPRISES', 'classification': 'DIST'},
        {'word': 'ENTERPRISES', 'classification': 'DESC'},
        {'word': 'HOLDINGS', 'classification': 'DIST'},
        {'word': 'HOLDINGS', 'classification': 'DESC'},
        {'word': 'WATER', 'classification': 'DIST'},
        {'word': 'WATER', 'classification': 'DESC'},
        {'word': 'VENTURES', 'classification': 'DIST'},
        {'word': 'VENTURES', 'classification': 'DESC'},
        {'word': 'PETER', 'classification': 'DIST'},
        {'word': 'LE', 'classification': 'DIST'},
        {'word': 'LE', 'classification': 'DESC'},
        {'word': 'SWIFT', 'classification': 'DIST'},
        {'word': 'SWIFT', 'classification': 'DESC'},
        {'word': 'EDUCATION', 'classification': 'DIST'},
        {'word': 'EDUCATION', 'classification': 'DESC'},
        {'word': 'SERVICES', 'classification': 'DIST'},
        {'word': 'SERVICES', 'classification': 'DESC'},
        {'word': 'CANADA', 'classification': 'DIST'},
        {'word': 'CANADA', 'classification': 'DESC'},
        {'word': 'INTERNATIONAL', 'classification': 'DIST'},
        {'word': 'INTERNATIONAL', 'classification': 'DESC'},
        {'word': 'SMART', 'classification': 'DIST'},
        {'word': 'SMART', 'classification': 'DESC'},
        {'word': 'SUPPLY', 'classification': 'DIST'},
        {'word': 'SUPPLY', 'classification': 'DESC'},
        {'word': 'COASTAL', 'classification': 'DIST'},
        {'word': 'COASTAL', 'classification': 'DESC'},
        {'word': 'SUPPLIES', 'classification': 'DIST'},
        {'word': 'SUPPLIES', 'classification': 'DESC'},
        {'word': 'CANDID', 'classification': 'DIST'},
        {'word': 'CONSULTING', 'classification': 'DIST'},
        {'word': 'CONSULTING', 'classification': 'DESC'},
        {'word': 'SERVICES', 'classification': 'DIST'},
        {'word': 'SERVICES', 'classification': 'DESC'},
        {'word': 'COMMUNITY', 'classification': 'DIST'},
        {'word': 'COMMUNITY', 'classification': 'DESC'},
        {'word': 'AAA', 'classification': 'DIST'},
        {'word': 'POWER', 'classification': 'DIST'},
        {'word': 'POWER', 'classification': 'DESC'},
        {'word': 'WASHING', 'classification': 'DESC'},
        {'word': 'STREAMLINE', 'classification': 'DIST'},
        {'word': 'TRUCKING', 'classification': 'DIST'},
        {'word': 'TRUCKING', 'classification': 'DESC'},
        {'word': 'PIONEERS', 'classification': 'DIST'},
        {'word': 'FLOORING', 'classification': 'DIST'},
        {'word': 'FLOORING', 'classification': 'DESC'},
        {'word': 'FLOOR', 'classification': 'DIST'},
        {'word': 'FLOOR', 'classification': 'DESC'},
        {'word': 'FLOORS', 'classification': 'DIST'},
        {'word': 'FLOORS', 'classification': 'DESC'},
        {'word': 'COVERING', 'classification': 'DESC'},
        {'word': 'CHAMPIONS', 'classification': 'DIST'},
        {'word': 'CHAMPIONS', 'classification': 'DESC'},
        {'word': 'CHAMPION', 'classification': 'DIST'},
        {'word': 'CHAMPION', 'classification': 'DESC'},
        {'word': 'HARDWOOD', 'classification': 'DIST'},
        {'word': 'HARDWOOD', 'classification': 'DESC'},
    ]
    save_words_list_classification(words_list_classification)

    conflict_list_db = [
        'ARMSTRONG PLUMBING & HEATING LTD.',
        'ARMSTRONG COOLING & WAREHOUSE LTD.',
        'ABC PEST MANAGEMENT CONSULTING INC.',
        'ABC ALWAYS BETTER CONSULTING INC.',
        'ABC - AUTISM BEHAVIOUR CONSULTING INCORPORATED',
        'ABC INTERNATIONAL CONSULTING LTD.',
        'NO. 003 CATHEDRAL MINING LTD.',
        'CATHEDRAL MINING LTD.',
        'ABC CREDIT BUREAU COLLECTIONS LIMITED',
        'ABC JEWELLERY & LOAN PAWNBROKERS LTD.',
        'PACIFIC BLUE ENTERPRISES LTD.',
        'PACIFIC ENGINEERING LTD.',
        'PACIFIC HOLDINGS LTD.',
        'BLUE PETER HOLDINGS INC.',
        'BLUE WATER VENTURES LTD.',
        'LE BLUE FOX CAFE INC.',
        'LE BLUE RESTAURANT LTD.',
        'CANADA SWIFT INTERNATIONAL EDUCATION CORP.',
        'COASTAL SMART SUPPLIES LTD.',
        'CANDID COMMUNITY CONSULTING CORP.',
        'AAA STREAMLINE POWER WASHING TRUCKING LTD.',
        'PIONEER FLOOR COVERING LTD.',
        'CHAMPION HARDWOOD FLOORS LTD.',
    ]
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
