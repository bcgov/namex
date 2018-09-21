from datetime import datetime

import pytest

from namex.models import Request, Name, State, User


priority_flag_testdata = [
    ('PQ', 'Y'),
    ('PJ', 'N'),
    ('P', 'N'),
    ('R', 'N')
]


@pytest.mark.parametrize("priority_cd,expected", priority_flag_testdata)
def test_add_nr_header_with_priority(priority_cd, expected):

    from api.endpoints.requests import add_nr_header

    nr = Request()
    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')
    nr_submitter = None

    nr_header = {
        'priority_cd': priority_cd,
        'state_type_cd': 'H',
        'nr_num': 'NR 0000001',
        'request_id': 1,
        'previous_request_id': None,
        'submit_count': 0,
        'request_type_cd': 'REQ',
        'expiration_date': None,
        'additional_info': None,
        'nature_business_info': 'N/A',
        'xpro_jurisdiction': None,
        'submitted_date': datetime.utcfromtimestamp(0),
        'last_update': datetime.utcfromtimestamp(0)
    }

    add_nr_header(nr, nr_header, nr_submitter, user, update=False)

    assert nr.priorityCd == expected


nr_state_testdata = [
    ('HISTORICAL',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'}],
     'HISTORICAL'
     ),
    ('H',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'}],
     'HOLD'
     ),
    ('D',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'}],
     'DRAFT'
     ),
    ('C',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'}],
     'CANCELLED'
     ),
    ('E',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'}],
     'EXPIRED'
     ),
    ('COMPLETED',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'}],
     State.APPROVED
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'},
     ],
     State.APPROVED
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'},
     ],
     State.APPROVED
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R'},
     ],
     State.APPROVED
     ),
    ('COMPLETED',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R'}],
     State.REJECTED
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R'},
     ],
     State.REJECTED
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'NE'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R'},
     ],
     State.REJECTED
     ),
    ('COMPLETED',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'C'}],
     State.CONDITIONAL
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'NE'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'C'},
     ],
     State.CONDITIONAL
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'C'},
     ],
     State.CONDITIONAL
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'C'},
     ],
     State.CONDITIONAL
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'C'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A'},
     ],
     State.CONDITIONAL
     ),
]


@pytest.mark.parametrize("state_type_cd,nr_names,expected", nr_state_testdata)
def test_add_nr_header_set_state(state_type_cd, nr_names, expected):
    from api.endpoints.requests import add_nr_header, add_names

    # the correct state for a Request that is completed in NRO is determined by the Name states

    nr = Request()
    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')
    nr_submitter = None

    nr_header = {
        'priority_cd': 'N',
        'state_type_cd': state_type_cd,
        'nr_num': 'NR 0000001',
        'request_id': 1,
        'previous_request_id': None,
        'submit_count': 0,
        'request_type_cd': 'REQ',
        'expiration_date': None,
        'additional_info': None,
        'nature_business_info': 'N/A',
        'xpro_jurisdiction': None,
        'submitted_date': datetime.utcfromtimestamp(0),
        'last_update': datetime.utcfromtimestamp(0)
    }

    add_nr_header(nr, nr_header, nr_submitter, user, update=False)
    add_names(nr, nr_names, update=False)

    assert nr.stateCd == expected
