from datetime import datetime
import pytest


priority_flag_testdata = [
    ('PQ', 'Y'),
    ('PJ', 'N'),
    ('P', 'N'),
    ('R', 'N')
]


@pytest.mark.parametrize("priority_cd,expected", priority_flag_testdata)
def test_add_nr_header_with_priority(priority_cd, expected):

    from api.endpoints.requests import add_nr_header
    from namex.models import Request, User

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
