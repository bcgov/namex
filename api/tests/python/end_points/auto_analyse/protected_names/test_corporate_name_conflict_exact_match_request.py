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
        ('J-J BULK TRANSPORT INC.', 'J & J BULK TRANSPORT LTD.'),
        ('MAPLE BAY PRESCHOOL LTD.', 'MAPLE BAY PRE-SCHOOL LTD.'),
        ('THUNDERROAD INVESTMENTS LTD.', 'THUNDERROAD.ORG INVESTMENTS INC.'),
        # No longer valid: FLOWERS AND DECORATING are in different categories,
        # then the name is approved
        # ('J & J HARDWOOD FLOORS AND FLOWERS LTD.', "J.J.'S HARDWOOD FLOORS AND DECORATING LTD."),
        ('TRADEPRO PHOENIX ENTERPRISES LTD.', 'TRADEPRO/PHOENIX ENTERPRISES INC.'),
        ('TEANOOK JOHNSON HOLDINGS INC.', 'TEANOOK / JOHNSON HOLDINGS INC.'),
        ('BIG MIKE FUN FARM INC.', "BIG MIKE'S FUN FARM INC."),
        ('PJI PIZZA POCO LTD.', 'PJI PIZZA(POCO) LTD.'),
        ('BEEDIE CH PROPERTY INC.', 'BEEDIE CH PROPERTY (LOT 3-22) INC.'),
        ('DISCOVERY RESIDENTIAL HOLDINGS INC.', 'DISCOVERY RESIDENTIAL HOLDINGS (LOT 4) INC.'),
        ('RR SOLUTIONS LTD.', 'R R SOLUTIONS LTD.'),
        # ("ISLAND H SERVICES INC.",'ISLAND H20 SERVICES INC.'),
        ('MR RENT A CAR LTD.', 'MR RENT-A-CAR LTD.'),
        ('ARMSTRONG PLUMBING & HEATING LTD.', 'ARMSTRONG PLUMBING & HEATING LTD.'),
        ('CATHEDRAL MINING LTD.', 'CATHEDRAL MINING LTD.'),
        ('MARKET CAFE LTD.', 'MARKET CAFE LTD.'),
    ],
)
@pytest.mark.xfail(raises=ValueError)
def test_corporate_name_conflict_exact_match_request_response(client, jwt, app, name, expected):
    words_list_classification = [
        {'word': 'ARMSTRONG', 'classification': 'DIST'},
        {'word': 'ARMSTRONG', 'classification': 'DESC'},
        {'word': 'PLUMBING', 'classification': 'DIST'},
        {'word': 'PLUMBING', 'classification': 'DESC'},
        {'word': 'HEATING', 'classification': 'DESC'},
        {'word': 'CATHEDRAL', 'classification': 'DIST'},
        {'word': 'MINING', 'classification': 'DIST'},
        {'word': 'MINING', 'classification': 'DESC'},
        {'word': 'JJ', 'classification': 'DIST'},
        {'word': 'JJ', 'classification': 'DESC'},
        {'word': 'BULK', 'classification': 'DIST'},
        {'word': 'BULK', 'classification': 'DESC'},
        {'word': 'TRANSPORT', 'classification': 'DIST'},
        {'word': 'TRANSPORT', 'classification': 'DESC'},
        {'word': 'MAPLE', 'classification': 'DIST'},
        {'word': 'MAPLE', 'classification': 'DESC'},
        {'word': 'BAY', 'classification': 'DIST'},
        {'word': 'BAY', 'classification': 'DESC'},
        {'word': 'PRESCHOOL', 'classification': 'DESC'},
        {'word': 'HARDWOOD', 'classification': 'DIST'},
        {'word': 'HARDWOOD', 'classification': 'DESC'},
        {'word': 'FLOORS', 'classification': 'DIST'},
        {'word': 'FLOORS', 'classification': 'DESC'},
        {'word': 'FLOWERS', 'classification': 'DIST'},
        {'word': 'FLOWERS', 'classification': 'DESC'},
        {'word': 'DECORATING', 'classification': 'DESC'},
        {'word': 'THUNDERROAD', 'classification': 'DIST'},
        {'word': 'INVESTMENTS', 'classification': 'DIST'},
        {'word': 'INVESTMENTS', 'classification': 'DESC'},
        {'word': 'TRADEPRO', 'classification': 'DIST'},
        {'word': 'PHOENIX', 'classification': 'DIST'},
        {'word': 'ENTERPRISES', 'classification': 'DIST'},
        {'word': 'ENTERPRISES', 'classification': 'DESC'},
        {'word': 'TEANOOK', 'classification': 'DIST'},
        {'word': 'JOHNSON', 'classification': 'DIST'},
        {'word': 'JOHNSON', 'classification': 'DESC'},
        {'word': 'HOLDINGS', 'classification': 'DIST'},
        {'word': 'HOLDINGS', 'classification': 'DESC'},
        {'word': 'BIG', 'classification': 'DIST'},
        {'word': 'MIKE', 'classification': 'DIST'},
        {'word': 'FUN', 'classification': 'DIST'},
        {'word': 'FUN', 'classification': 'DESC'},
        {'word': 'FARM', 'classification': 'DIST'},
        {'word': 'FARM', 'classification': 'DESC'},
        {'word': 'PJI', 'classification': 'DIST'},
        {'word': 'PIZZA', 'classification': 'DIST'},
        {'word': 'PIZZA', 'classification': 'DESC'},
        {'word': 'POCO', 'classification': 'DIST'},
        {'word': 'POCO', 'classification': 'DESC'},
        {'word': 'BEEDIE', 'classification': 'DIST'},
        {'word': 'CH', 'classification': 'DIST'},
        {'word': 'CH', 'classification': 'DESC'},
        {'word': 'PROPERTY', 'classification': 'DIST'},
        {'word': 'PROPERTY', 'classification': 'DESC'},
        {'word': 'DISCOVERY', 'classification': 'DIST'},
        {'word': 'DISCOVERY', 'classification': 'DESC'},
        {'word': 'RESIDENTIAL', 'classification': 'DIST'},
        {'word': 'RESIDENTIAL', 'classification': 'DESC'},
        {'word': 'RR', 'classification': 'DIST'},
        {'word': 'RR', 'classification': 'DESC'},
        {'word': 'SOLUTIONS', 'classification': 'DIST'},
        {'word': 'SOLUTIONS', 'classification': 'DESC'},
        {'word': 'ISLAND', 'classification': 'DIST'},
        {'word': 'ISLAND', 'classification': 'DESC'},
        {'word': 'H', 'classification': 'DIST'},
        {'word': 'H', 'classification': 'DESC'},
        {'word': 'SERVICES', 'classification': 'DIST'},
        {'word': 'SERVICES', 'classification': 'DESC'},
        {'word': 'MR', 'classification': 'DIST'},
        {'word': 'MR', 'classification': 'DESC'},
        {'word': 'RENT', 'classification': 'DIST'},
        {'word': 'RENT', 'classification': 'DESC'},
        {'word': 'A', 'classification': 'DIST'},
        {'word': 'A', 'classification': 'DESC'},
        {'word': 'CAR', 'classification': 'DIST'},
        {'word': 'CAR', 'classification': 'DESC'},
        {'word': 'MARKET', 'classification': 'DIST'},
        {'word': 'MARKET', 'classification': 'DESC'},
        {'word': 'CAFE', 'classification': 'DIST'},
        {'word': 'CAFE', 'classification': 'DESC'},
    ]
    save_words_list_classification(words_list_classification)

    conflict_list_db = [
        'ARMSTRONG PLUMBING & HEATING LTD.',
        'ARMSTRONG COOLING & WAREHOUSE LTD.',
        'NO. 003 CATHEDRAL MINING LTD.',
        'CATHEDRAL MINING LTD.',
        'MAPLE BAY PRE-SCHOOL LTD.',
        'MAPLE LEAF MONTESSORI PRESCHOOL INC.',
        'J & J BULK TRANSPORT LTD.',
        'J & J TRANSPORT (PARTNERSHIP)',
        'JJ KK TRANSPORT SERVICES INC.',
        'J&J TRANSPORTATION SERVICES',
        'JJ TRANSPORT',
        'J & J TRANSPORT',
        "J.J.'S HARDWOOD FLOORS AND DECORATING LTD.",
        'THUNDERROAD.ORG INVESTMENTS INC.',
        'TRADEPRO/PHOENIX ENTERPRISES INC.',
        'TEANOOK / JOHNSON HOLDINGS INC.',
        'COAST WIDE HOMECARE/PAINTING NEEDS LTD.',
        "BIG MIKE'S FUN FARM INC.",
        'PJI PIZZA(POCO) LTD.',
        'BEEDIE CH PROPERTY (LOT 3-22) INC.',
        'DISCOVERY RESIDENTIAL HOLDINGS (LOT 4) INC.',
        'R R SOLUTIONS LTD.',
        'ISLAND H20 SERVICES INC.',
        'MR RENT-A-CAR LTD.',
        'MARKET CAFE LTD.',
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
