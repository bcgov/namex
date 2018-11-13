import pytest
import pytest_mock
from datetime import datetime
from nro.nro_datapump import nro_data_pump_update
from namex.models import Request, Name, State, User


# TODO Add more tests for the various use-cases.
def test_datapump(app, mocker):

    # create minimal NR to send to NRO
    nr = Request()
    nr.nrNum = 'NR 0000001'
    nr.stateCd = State.REJECTED
    nr.consentFlag = 'N'
    nr.lastUpdate = datetime.utcfromtimestamp(0)

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
    nro_data_pump_update(nr, ora_cursor=oc, expires_days=60)

    oc.callproc.assert_called_with('NRO_DATAPUMP_PKG.name_examination', #package.proc_name
                                   ['NR 0000001',                  # p_nr_number
                                    'R',                           # p_status
                                    '19700302',                    # p_expiry_date (length=8)
                                    'N',                           # p_consent_flag
                                    'bob',                         # p_examiner_id (anything length <=7)
                                    'R****No Distinctive Term 1',  # p_choice1
                                    'R****No Distinctive Term 2',  # p_choice2
                                    'R****No Distinctive Term 3',  # p_choice3
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
    nr.lastUpdate = datetime.utcfromtimestamp(0)

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
    nro_data_pump_update(nr, ora_cursor=oc, expires_days=60)

    oc.callproc.assert_called_with('NRO_DATAPUMP_PKG.name_examination', #package.proc_name
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
