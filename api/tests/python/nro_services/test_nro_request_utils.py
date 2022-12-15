import datetime

import pytest

from namex.models import Request, User, State
from namex import db

from tests.python import FROZEN_DATETIME, EPOCH_DATETIME


# utility routine
def dict_to_json_keys(pydict: dict) -> dict:
    """this converts a dict using the python coding style to a dict
    where the keys are in JSON format style
    :pydict dict keys are strings in python style format
    :returns dict
    """
    d = {}
    for key in pydict.keys():
        new_key = key.title().replace('_', '')
        new_key = new_key[:1].lower() + new_key[1:]
        d[new_key] = pydict[key]
    return d


nr_format_testdata = [
    ('', False),
    ('NR', False),
    ('NR ', False),
    ('NR 1', False),
    ('NR 1234567', True),
    ('NR-1234567', False),
    ('1', False),
    ('1234567', False),
    ('12345678', False),
    (' 1234567', False),
]


@pytest.mark.parametrize("nr, valid", nr_format_testdata)
def test_valid_nr_format(nr, valid):
    from namex.services.nro.utils import validNRFormat
    assert valid == validNRFormat(nr)


nr_applicants_test_data = [
    ({'lastName': 'last_name',
      'firstName': 'first_name',
      'middleName': 'middle_name',
      'phoneNumber': '111.111.1111',
      'faxNumber': '111.111.1111',
      'emailAddress': 'email_address',
      'contact' : 'contact',
      'clientFirstName': 'first_name',
      'clientLastName': 'last_name',
      'declineNotificationInd': 'Y',
      'addrLine1': 'addr_line_1',
      'addrLine2': 'addr_line_2',
      'addrLine3' : 'addr_line_3',
      'city': 'city',
      'postalCd': 'postal_cd',
      'stateProvinceCd': 'BC',
      'countryTypeCd': 'CA'
      },
     {'last_name': 'new_last_name',
      'first_name': 'new_first_name',
      'middle_name': 'new_middle_name',
      'phone_number': '222.222.2222',
      'fax_number': '222.222.2222',
      'email_address': 'tom@example.com',
      'contact' : None,
      'client_first_name': 'cl_first_name',
      'client_last_name': 'cl_last_name',
      'decline_notification_ind': 'N',
      'addr_line_1': '1234 Alder',
      'addr_line_2': 'Suite 100',
      'addr_line_3' : None,
      'city': 'Victoria',
      'postal_cd': 'X0X0X0',
      'state_province_cd': 'AB',
      'country_type_cd': 'AG'
      }
    )
]


@pytest.mark.parametrize("applicant1 ,applicant2", nr_applicants_test_data)
def test_request_add_applicant_existing(app, request, session, applicant1, applicant2):

    # imports for just this test
    from namex.models import Applicant
    from namex.services.nro.request_utils import add_applicant

    # SETUP
    # create an NR and add an applicant
    nr = Request()
    nr.activeUser = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')
    nr.applicants.append(Applicant(**applicant1))

    session.add(nr)
    session.commit()

    # Test
    # Call add_applicant and then assert the new NR applicant matches our data

    add_applicant(nr, applicant2)

    session.add(nr)
    session.commit()

    appl = nr.applicants.one_or_none()

    nra = dict_to_json_keys(applicant2)
    a = appl.as_dict()
    if a.get('partyId'): a.pop('partyId')

    # check entire dict
    assert nra == a


@pytest.mark.parametrize("applicant1 ,applicant2", nr_applicants_test_data)
def test_request_add_applicant_not_existing(app, request, session, applicant1, applicant2):

    # imports for just this test
    from namex.services.nro.request_utils import add_applicant

    # SETUP
    # create an NR
    nr = Request()
    nr.activeUser = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')

    session.add(nr)
    session.commit()

    # Test
    # Call add_applicant and then assert the new NR applicant matches our data

    add_applicant(nr, applicant2)

    session.add(nr)
    session.commit()

    appl = nr.applicants.one_or_none()

    nra = dict_to_json_keys(applicant2)
    a = appl.as_dict()
    if a.get('partyId'): a.pop('partyId')

    # check entire dict
    assert nra == a


comments_test_data = [
    ([{'examiner_idir': 'idir/bob', 'examiner_comment': 'examiner comment', 'state_comment': 'state comment', 'event_timestamp': EPOCH_DATETIME},
      ], 1, False
    ),
    ([
        {'examiner_idir': 'idir/bob', 'examiner_comment': 'examiner comment', 'state_comment': 'state comment', 'event_timestamp': EPOCH_DATETIME},
        {'examiner_idir': 'idir/bob', 'examiner_comment': 'examiner comment', 'state_comment': 'state comment', 'event_timestamp': EPOCH_DATETIME},
        {'examiner_idir': 'idir/bob', 'examiner_comment': 'examiner comment', 'state_comment': 'state comment', 'event_timestamp': EPOCH_DATETIME},
      ], 3, False
    ),
    ([{'examiner_idir': 'idir/bob', 'examiner_comment': 'examiner comment', 'state_comment': 'state comment', 'event_timestamp': EPOCH_DATETIME},
      ], 1, True
     ),
    ([
         {'examiner_idir': 'idir/bob', 'examiner_comment': 'examiner comment', 'state_comment': 'state comment', 'event_timestamp': EPOCH_DATETIME},
         {'examiner_idir': 'idir/bob', 'examiner_comment': 'examiner comment', 'state_comment': 'state comment', 'event_timestamp': EPOCH_DATETIME},
         {'examiner_idir': 'idir/bob', 'examiner_comment': 'examiner comment', 'state_comment': 'state comment', 'event_timestamp': EPOCH_DATETIME},
     ], 3, True
    ),
]
@pytest.mark.parametrize("test_comments, test_size, should_have_existing_comments", comments_test_data)
def test_add_comments(app, request, session, test_comments, test_size, should_have_existing_comments):

    # imports for just this test
    from namex.services.nro.request_utils  import add_comments

    # SETUP
    # create an NR
    nr = Request()
    nr.activeUser = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')

    if should_have_existing_comments:
        add_comments(nr, test_comments)

    session.add(nr)
    session.commit()

    # Test
    add_comments(nr, test_comments)

    session.add(nr)
    session.commit()

    comments = nr.comments.all()

    assert test_size == len(comments)

    for com in comments:
        comment_found = False
        for tc in test_comments:
            if tc['examiner_comment'] == com.comment:
                comment_found = True
                continue

        assert comment_found
        assert EPOCH_DATETIME == com.timestamp.replace(tzinfo=None)


pns_test_data=[([{'partner_name_type_cd': 'type_cd'
                    ,'partner_name_number': 'pn_number'
                    ,'partner_jurisdiction_type_cd': 'AB'
                    ,'partner_name_date': EPOCH_DATETIME
                    ,'partner_name': 'partner_name'
                    ,'last_update_id': 'id'},]
                ),
               ([
                   {'partner_name_type_cd': 'type_cd'
                     ,'partner_name_number': 'pn_1'
                     ,'partner_jurisdiction_type_cd': 'AB'
                     ,'partner_name_date': EPOCH_DATETIME
                     ,'partner_name': 'partner_name_1'
                     ,'last_update_id': 'id'},
                   {'partner_name_type_cd': 'type_cd'
                       ,'partner_name_number': 'pn_2'
                       ,'partner_jurisdiction_type_cd': 'AB'
                       ,'partner_name_date': EPOCH_DATETIME
                       ,'partner_name': 'partner_name_2'
                       ,'last_update_id': 'id'},
                 ]
               ),
               ]


@pytest.mark.parametrize("pns", pns_test_data)
def test_add_nwpta(app, request, session, pns):

    # imports for just this test
    from namex.services.nro.request_utils import add_nwpta

    # SETUP
    # create an NR
    nr = Request()
    nr.activeUser = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')

    session.add(nr)
    session.commit()

    # Test
    add_nwpta(nr, pns)

    session.add(nr)
    session.commit()

    partners = nr.partnerNS.all()

    assert len(pns) == len(partners)

    for partner in partners:
        partner_found = False
        for p in pns:
            if p['partner_jurisdiction_type_cd'] == partner.partnerJurisdictionTypeCd:
                partner_found = True
                continue

        assert partner_found


names_test_data = [
    ([
        {'choice_number': 1, 'name': 'name corp', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ], False),
    ([
        {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ], False),
    ([
        {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 3, 'name': 'name corp3', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ], False),
    ([
         {'choice_number': 1, 'name': 'name corp', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
     ], True),
    ([
         {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
         {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
     ], True),
    ([
         {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
         {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
         {'choice_number': 3, 'name': 'name corp3', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
     ], True),
    ([
         {'choice_number': 1, 'name': 'name corp', 'designation': 'ltd', 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
     ], ['APPROVED', ]),
    ([
         {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
         {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
     ], ['APPROVED', ]),
    ([
         {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
         {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
         {'choice_number': 3, 'name': 'name corp3', 'designation': 'ltd', 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
     ], ['APPROVED', ]),
]


@pytest.mark.parametrize("test_names, previous_names", names_test_data)
def test_add_names(app, request, session, test_names, previous_names):

    # imports for just this test
    from namex.services.nro.request_utils import add_names

    # SETUP
    # create an NR
    nr = Request()
    nr.activeUser = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')

    if previous_names:
        add_names(nr, test_names)

    session.add(nr)
    session.commit()

    # Test
    add_names(nr, test_names)
    session.add(nr)
    session.commit()

    names = nr.names.all()

    assert len(test_names) == len(names)

    for name in names:
        name_found = False
        for tn in test_names:
            if tn['name'] == name.name:
                name_found = True
                continue

        assert name_found

names_test_after_reset_data = [
    ([
        {'choice_number': 1, 'name': 'name corp', 'designation': 'ltd', 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
    ], [
        {'choice_number': 1, 'name': 'name corp', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ], ['APPROVED',]),
    ([
        {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
        {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ], [
        {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ], ['APPROVED', 'NE']),
    ([
        {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'R', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'R', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 3, 'name': 'name corp3', 'designation': 'ltd', 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
    ], [
        {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 3, 'name': 'name corp3', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ], ['REJECTED', 'REJECTED', 'APPROVED']),
]


@pytest.mark.parametrize("previous_names, test_names, expected_states", names_test_after_reset_data)
def test_add_names_after_reset(app, request, session, previous_names, test_names, expected_states):

    # imports for just this test
    from namex.services.nro.request_utils import add_names

    # SETUP
    # create an NR
    nr = Request()
    nr.activeUser = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')

    if previous_names:
        add_names(nr, previous_names)

    nr.hasBeenReset = True

    session.add(nr)
    session.commit()

    # Test
    add_names(nr, test_names)
    session.add(nr)
    session.commit()

    names = nr.names.all()

    assert len(test_names) == len(names)

    for name in names:
        name_found = False
        decision_data_intact = False
        for tn in test_names:
            if tn['name'] == name.name:
                name_found = True
                if name.state == expected_states[tn['choice_number']-1]:
                    decision_data_intact = True
                continue

        assert name_found
        assert decision_data_intact

names_test_with_changes_data = [
    ([
        {'choice_number': 1, 'name': 'name corp', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ], [
        {'choice_number': 1, 'name': 'name corp new', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ]),
    ([
        {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ], [
        {'choice_number': 1, 'name': 'name corp1 new', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2 new', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ]),
    ([
        {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 3, 'name': 'name corp3', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ], [
        {'choice_number': 1, 'name': 'name corp1 new', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2 new', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 3, 'name': 'name corp3 new', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
    ]),
    ([
        {'choice_number': 1, 'name': 'name corp1', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 3, 'name': 'name corp3', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
     ], [
        {'choice_number': 1, 'name': 'name corp1 new', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
        {'choice_number': 2, 'name': 'name corp2 new', 'designation': 'ltd', 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
     ]),
]

@pytest.mark.parametrize("previous_names, test_names", names_test_with_changes_data)
def test_add_names_with_changes(app, request, session, previous_names, test_names):

    # imports for just this test
    from namex.services.nro.request_utils import add_names

    # SETUP
    # create an NR
    nr = Request()
    nr.activeUser = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')

    if previous_names:
        add_names(nr, previous_names)

    session.add(nr)
    session.commit()

    # Test
    add_names(nr, test_names)
    session.add(nr)
    session.commit()

    names = nr.names.all()

    assert len(test_names) == len(names)

    for name in names:
        name_found = False
        decision_data_intact = False
        for tn in test_names:
            if tn['name'] == name.name:
                name_found = True
                continue

        assert name_found


priority_flag_testdata = [
    ('PQ', 'Y'),
    ('PJ', 'Y'),
    ('RQ', 'N'),
    ('RJ', 'Y'),
    ('P', 'N'),
    ('R', 'N')
]


@pytest.mark.parametrize("priority_cd,expected", priority_flag_testdata)
def test_add_nr_header_with_priority(priority_cd, expected):

    from namex.services.nro.request_utils import add_nr_header

    nr = Request()
    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')
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
        'submitted_date': EPOCH_DATETIME,
        'last_update': EPOCH_DATETIME
    }

    add_nr_header(nr, nr_header, nr_submitter, user)

    assert nr.priorityCd == expected
    # assert nr.priorityDate == datetime.utcfromtimestamp(0)


# test for changing priority codes
mutating_priority_flag_testdata = [
    ('priority_not_changed', 'PQ', 'PQ', 'Y', EPOCH_DATETIME),
    ('priority_changed', 'PJ', 'PQ', 'Y', EPOCH_DATETIME),
    ('priority_changed', 'RJ', 'PQ', 'Y', EPOCH_DATETIME),
    ('priority_changed', 'P', 'PQ', 'Y', FROZEN_DATETIME),
    ('priority_changed', 'R', 'PQ', 'Y', FROZEN_DATETIME),
    ('priority_changed', 'RQ', 'PQ', 'Y', FROZEN_DATETIME),
    ('priority_changed', 'RQ', 'PJ', 'Y', FROZEN_DATETIME),
    ('priority_changed', 'RQ', 'RJ', 'Y', FROZEN_DATETIME),
]


@pytest.mark.parametrize("test_name, initial_priority_cd, second_priority_code, expected_cd, expected_dt", mutating_priority_flag_testdata)
def test_update_nr_header_with_mutating_priority(freeze_datetime_utcnow, test_name, initial_priority_cd, second_priority_code, expected_cd, expected_dt):

    from namex.services.nro.request_utils import add_nr_header

    nr = Request()
    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')
    nr_submitter = {'submitted_date': EPOCH_DATETIME, 'submitter': 'doesnt matter'}

    nr_header = {
        'priority_cd': initial_priority_cd,
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
        'submitted_date': EPOCH_DATETIME,
        'last_update': EPOCH_DATETIME
    }

    print (nr.json())

    add_nr_header(nr, nr_header, nr_submitter, user)

    nr_header['priority_cd'] = second_priority_code
    add_nr_header(nr, nr_header, nr_submitter, user)

    assert  expected_cd == nr.priorityCd
    assert  expected_dt == nr.priorityDate


nr_state_testdata = [
    ('HISTORICAL',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'}],
     'HISTORICAL'
     ),
    ('H',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'}],
     'HOLD'
     ),
    ('D',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'}],
     'DRAFT'
     ),
    ('C',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'}],
     'CANCELLED'
     ),
    ('E',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'}],
     'EXPIRED'
     ),
    ('COMPLETED',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'}],
     State.APPROVED
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
     ],
     State.APPROVED
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R', 'consumption_date': None, 'corp_num': None},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
     ],
     State.APPROVED
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R', 'consumption_date': None, 'corp_num': None},
     ],
     State.APPROVED
     ),
    ('COMPLETED',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R', 'consumption_date': None, 'corp_num': None}],
     State.REJECTED
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R', 'consumption_date': None, 'corp_num': None},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R', 'consumption_date': None, 'corp_num': None},
     ],
     State.REJECTED
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R', 'consumption_date': None, 'corp_num': None},
     ],
     State.REJECTED
     ),
    ('COMPLETED',
     [{'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'C', 'consumption_date': None, 'corp_num': None}],
     State.CONDITIONAL
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'NE', 'consumption_date': None, 'corp_num': None},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'C', 'consumption_date': None, 'corp_num': None},
     ],
     State.CONDITIONAL
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'C', 'consumption_date': None, 'corp_num': None},
     ],
     State.CONDITIONAL
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'R', 'consumption_date': None, 'corp_num': None},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'C', 'consumption_date': None, 'corp_num': None},
     ],
     State.CONDITIONAL
     ),
    ('COMPLETED',
     [
         {'choice_number': 1, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'C', 'consumption_date': None, 'corp_num': None},
         {'choice_number': 2, 'name': 'PROCINE ENTERPRISES LTD', 'designation': None, 'name_state_type_cd': 'A', 'consumption_date': '01-SEP-08 11:11:11', 'corp_num': 'S1234567'},
     ],
     State.CONDITIONAL
     ),
]


@pytest.mark.parametrize("state_type_cd,nr_names,expected", nr_state_testdata)
def test_add_nr_header_set_state(state_type_cd, nr_names, expected):
    from namex.services.nro.request_utils import add_names, add_nr_header

    # the correct state for a Request that is completed in NRO is determined by the Name states

    nr = Request()
    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')
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
        'submitted_date': EPOCH_DATETIME,
        'last_update': EPOCH_DATETIME
    }

    add_nr_header(nr, nr_header, nr_submitter, user)
    add_names(nr, nr_names)

    assert nr.stateCd == expected
