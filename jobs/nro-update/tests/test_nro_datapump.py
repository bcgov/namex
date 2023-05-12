from datetime import datetime

import pytest
from pytz import timezone

from nro.nro_datapump import nro_data_pump_update
from namex.models import Request, Name, State, User
from namex.services.name_request import NameRequestService


expiry_date_test_data = [
    ('using epoch utc',            # test descriptive name
     datetime(1970, 1, 1, 00, 00, tzinfo=timezone('US/Pacific', )), # start date - time
     20,                           # days to add
     'US/Pacific',                 # timezone that should be used
     datetime(1970, 1, 21, 23, 59)), # expected outcome
    ('using a time after 4pm',
     datetime(2001, 8, 5, 19, 00, tzinfo=timezone('US/Pacific',)), 20, 'US/Pacific', datetime(2001, 8, 25, 23, 59)),
    ('using a time before 4pm',
     datetime(2001, 8, 5, 9, 00, tzinfo=timezone('US/Pacific',)), 20, 'US/Pacific', datetime(2001, 8, 25, 23, 59)),
]

@pytest.mark.parametrize("test_name, start_date, days, tz, expected_date", expiry_date_test_data)
def test_create_expiry_date(test_name, start_date, days, tz, expected_date):
    nr_service = NameRequestService()
    ced = nr_service.create_expiry_date(start_date, expires_in_days=days)

    assert ced.replace(tzinfo=None) == expected_date
    assert ced.tzinfo.zone == tz


datapump_test_data = [
    (datetime(1970, 1, 1, 00, 00, tzinfo=timezone('US/Pacific', )), datetime(1970, 2, 26, 23, 59)),
    (datetime(2001, 8, 5,  9, 00, tzinfo=timezone('US/Pacific',)), datetime(2001, 9, 30, 23, 59)),
    (datetime(2001, 8, 5, 19, 00, tzinfo=timezone('US/Pacific',)), datetime(2001, 9, 30, 23, 59)),
]

# TODO Add more tests for the various use-cases.
@pytest.mark.parametrize("start_date, expected_date", datapump_test_data)
def test_datapump(app, mocker, start_date, expected_date):

    # create minimal NR to send to NRO
    nr = Request()
    nr.nrNum = 'NR 0000001'
    nr.stateCd = State.REJECTED
    nr.consentFlag = 'N'
    nr.lastUpdate = start_date

    # requires the username
    user = User('idir/bob','bob','last','idir','localhost')
    nr.activeUser = user

    # add name(s) to the NR - max 3
    for i in range(1,4):
        name = Name()
        name.state=Name.REJECTED
        name.name = 'sample name {}'.format(i)
        name.choice = i
        name.decision_text = 'No Distinctive Term {}'.format(i)
        nr.names.append(name)

    # mock the oracle cursor
    oc = mocker.MagicMock()

    # make the real call
    nro_data_pump_update(nr, ora_cursor=oc, expiry_date=datetime(2023, 6, 30, 23, 59))
    oc.callfunc.assert_called_with('NRO_DATAPUMP_PKG.name_examination_func',  # package.func_name
                                   str,
                                   ['NR 0000001',  # p_nr_number
                                    'R',  # p_status
                                    expected_date.strftime('%Y%m%d'),  # p_expiry_date (length=8)
                                    'N',  # p_consent_flag
                                    'bob',  # p_examiner_id (anything length <=7)
                                    'R****No Distinctive Term 1',  # p_choice1
                                    'R****No Distinctive Term 2',  # p_choice2
                                    'R****No Distinctive Term 3',  # p_choice3
                                    None,  # p_exam_comment
                                    '',  # p_add_info - not used in proc anymore
                                    None,  # p_confname1A
                                    None,  # p_confname1B
                                    None,  # p_confname1C
                                    None,  # p_confname2A
                                    None,  # p_confname2B
                                    None,  # p_confname2C
                                    None,  # p_confname3A
                                    None,  # p_confname3B
                                    None])  # p_confname3C

# testdata pattern is ({consent_flag}, {state_cd})
consent_testdata = [
    ('Y', State.APPROVED),
    ('N', State.CONDITIONAL),
    ('Y', State.CONDITIONAL)
]


@pytest.mark.parametrize("consent_flag,state_cd", consent_testdata)
def test_datapump_nr_requires_consent_flag(app, mocker,consent_flag,state_cd):

    # create minimal NR to send to NRO
    nr = Request()
    nr.nrNum = 'NR 0000001'
    nr.stateCd = state_cd
    nr.consentFlag = consent_flag
    nr.lastUpdate = datetime(1970, 1, 1, 00, 00, tzinfo=timezone('US/Pacific', ))

    # requires the username
    user = User('idir/bob','bob','last','idir','localhost')
    nr.activeUser = user

    # add name(s) to the NR - max 3
    for i in range(1,4):
        name = Name()
        name.state=Name.APPROVED if i == 1 else Name.NOT_EXAMINED
        name.name = 'sample name {}'.format(i)
        name.choice = i
        name.decision_text = 'All good to go {}'.format(i)
        nr.names.append(name)

    # mock the oracle cursor
    oc = mocker.MagicMock()
    # make the real call

    nro_data_pump_update(nr, ora_cursor=oc, expiry_date=datetime(2023, 6, 30, 23, 59))

    oc.callfunc.assert_called_with('NRO_DATAPUMP_PKG.name_examination_func',  # package.func_name
                                   str,
                                   ['NR 0000001',                  # p_nr_number
                                    'A',                           # p_status
                                    '19700302',                    # p_expiry_date (length=8)
                                    'Y',                           # p_consent_flag
                                    'bob',                         # p_examiner_id (anything length <=7)
                                    'A****All good to go 1',       # p_choice1
                                    None,                          # p_choice2
                                    None,                          # p_choice3
                                    None,                          # p_exam_comment
                                    '',                            # p_add_info - not used in proc anymore
                                    None,                          # p_confname1A
                                    None,                          # p_confname1B
                                    None,                          # p_confname1C
                                    None,                          # p_confname2A
                                    None,                          # p_confname2B
                                    None,                          # p_confname2C
                                    None,                          # p_confname3A
                                    None,                          # p_confname3B
                                    None])                         # p_confname3C
