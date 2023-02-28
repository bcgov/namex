from __future__ import annotations

import json
import pytest
from contextlib import suppress
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import List

from namex.models import Applicant, Name, Request, State, User
from tests.python.end_points.util import create_header
from tests.python.end_points.common.utils import (
    get_utc_server_now_with_delta,
    get_server_now_str,
    get_server_now_with_delta_str,
    get_utc_server_now
)

# TODO: import these helper functions from somewhere shared by the tests


def create_applicant(first_name: str, last_name: str, email_address: str = None, phone_number: str = None) -> Applicant:
    """Create new applicant."""
    applicant = Applicant(
        firstName=first_name,
        lastName=last_name,
        emailAddress=email_address,
        phoneNumber=phone_number
    )
    applicant.save_to_db()
    return applicant


def create_name(name: str, state: str, choice: int) -> Name:
    """Create new name."""
    name = Name(
        name=name,
        state=state,
        choice=choice
    )
    name.save_to_db()
    return name


def create_nr(nr_num: str, state_cd: str, submitted: datetime, names: list) -> Request:
    """Create new NR."""
    nr = Request()
    nr.nrNum = nr_num
    nr.stateCd = state_cd
    nr.submittedDate = submitted
    nr._source = 'NRO'
    for name in names:
        nr.names.append(create_name(name['name'], name['state'], name['choice']))
    nr.save_to_db()
    return nr


def generate_nrs(num: int, nr_nums: List[str], names: list, submitted: List[datetime]) -> List[Request]:
    """Generate a set of NRs and applicants for testing."""
    states = [
        State.APPROVED,
        State.CONDITIONAL,
        State.DRAFT,
        State.CANCELLED,
        State.REJECTED,
        State.HOLD,
        State.PENDING_PAYMENT
    ]
    nrs = []
    for i in range(num):
        nr_num = nr_num = nr_nums[i] if i < len(nr_nums) else f'NR {i}'
        submitted_date = submitted[i] if i < len(submitted) else datetime.utcnow() - timedelta(days=i)
        state_index = i % len(states)
        new_names = names[i] if i < len(names) else []
        nr = create_nr(nr_num, states[state_index], submitted_date, new_names)
        applicant = create_applicant(i, i, email_address=i, phone_number=i)
        nr.applicants.append(applicant)
        nrs.append(nr)
    return nrs

# TODO: add tests for searching by last modified by, etc. and combined searches


def test_namex_search_default(client, jwt, app):
    """Test default search brings back nrs as expected."""
    generate_nrs(14, [], [], [])

    # get the resource (this is what we are testing)
    rv = client.get(f'api/v1/requests', headers=create_header(jwt, [User.EDITOR]))
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')
    # default should return up to 10 and order by submitted date desc
    assert len(resp['nameRequests'][0]) == 10

    date = resp['nameRequests'][0][0]['submittedDate']
    for nr in resp['nameRequests'][0]:
        assert nr['submittedDate'] <= date
        date = nr['submittedDate']


@pytest.mark.parametrize('state_cd', [
    State.APPROVED,
    State.CANCELLED,
    State.CONDITIONAL,
    State.DRAFT,
    State.HOLD,
    State.REJECTED
])
def test_namex_search_state(client, jwt, app, state_cd):
    """Test searching by state."""
    generate_nrs(14, [], [], [])

    # get the resource (this is what we are testing)
    rv = client.get(f'api/v1/requests?queue={state_cd}', headers=create_header(jwt, [User.EDITOR]))
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')
    assert len(resp['nameRequests'][0]) > 0

    # should only contain nrs with the given state
    for nr in resp['nameRequests'][0]:
        assert nr['stateCd'] == state_cd


@pytest.mark.parametrize('search_nr, nrs', [
    ('NR', ['NR 0000001', 'NR 0000011', 'NR 1000011', 'NR 0100011', 'NR 0101010', 'NR 01', 'NR 1234']),
    ('NR 00', ['NR 0000001', 'NR 0000011', 'NR 1000011', 'NR 0100011', 'NR 0101010', 'NR 01', 'NR 1234']),
    ('00', ['NR 0000001', 'NR 0000011', 'NR 1000011', 'NR 0100011', 'NR 0101010', 'NR 01', 'NR 1234']),
    ('001', ['NR 0000001', 'NR 0000011', 'NR 1000011', 'NR 0100011', 'NR 0101010', 'NR 01', 'NR 1234']),
    ('NR 01', ['NR 0000001', 'NR 0000011', 'NR 1000011', 'NR 0100011', 'NR 0101010', 'NR 01', 'NR 1234']),
    ('NR 23', ['NR 0000001', 'NR 0000011', 'NR 1000011', 'NR 0100011', 'NR 0101010', 'NR 01', 'NR 1234']),
    ('23', ['NR 0000001', 'NR 0000011', 'NR 1000011', 'NR 0100011', 'NR 0101010', 'NR 01', 'NR 1234']),
    ('NR 123', ['NR 0000001', 'NR 0000011', 'NR 1000011', 'NR 0100011', 'NR 0101010', 'NR 01', 'NR 1234']),
    ('NR 123', ['NR 0000001', 'NR 0000011', 'NR 1000011', 'NR 0100011', 'NR 0101010', 'NR 01', 'NR 1234'])
])
def test_namex_search_nr_num(client, jwt, app, search_nr, nrs):
    """Test searching by NR number."""
    generate_nrs(len(nrs), nrs, [], [])

    # get the resource (this is what we are testing)
    rv = client.get(f'api/v1/requests?nrNum={search_nr}', headers=create_header(jwt, [User.EDITOR]))
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')
    assert len(resp['nameRequests'][0]) == len([nr for nr in nrs if search_nr in nr])

    # should only contain nrs that contain the search_nr
    for nr in resp['nameRequests'][0]:
        assert search_nr in nr['nrNum']


@pytest.mark.parametrize('order, submitted_interval, last_date', [
    ('desc', 'All', None),
    ('asc', 'All', None),
    ('desc', 'Today', datetime.utcnow() - timedelta(days=1)),
    ('asc', 'Today', datetime.utcnow() - timedelta(days=1)),
    ('desc', '7 days', datetime.utcnow() - timedelta(days=7)),
    ('asc', '7 days', datetime.utcnow() - timedelta(days=7)),
    ('desc', '30 days', datetime.utcnow() - timedelta(days=30)),
    ('asc', '30 days', datetime.utcnow() - timedelta(days=30)),
    ('desc', '90 days', datetime.utcnow() - timedelta(days=90)),
    ('asc', '90 days', datetime.utcnow() - timedelta(days=90)),
    ('desc', '1 year', datetime.utcnow() - timedelta(days=1 * (365))),
    ('asc', '1 year', datetime.utcnow() - timedelta(days=1 * (365))),
    ('desc', '3 years', datetime.utcnow() - timedelta(days=3 * (365))),
    ('asc', '3 years', datetime.utcnow() - timedelta(days=3 * (365))),
    ('desc', '5 years', datetime.utcnow() - timedelta(days=5 * (365))),
    ('asc', '5 years', datetime.utcnow() - timedelta(days=5 * (365))),
])
def test_namex_search_submitted(client, jwt, app, order, submitted_interval, last_date):
    """Test searching by submitted date."""
    submitted = [
        datetime.utcnow(),
        datetime.utcnow() - timedelta(days=6),
        datetime.utcnow() - timedelta(days=8),
        datetime.utcnow() - timedelta(days=29),
        datetime.utcnow() - timedelta(days=31),
        datetime.utcnow() - timedelta(days=89),
        datetime.utcnow() - timedelta(days=91),
        datetime.utcnow() - timedelta(days=1 * (365)),
        datetime.utcnow() - timedelta(days=2 * (365)),
        datetime.utcnow() - timedelta(days=3 * (365)),
        datetime.utcnow() - timedelta(days=5 * (365)),
    ]
    generate_nrs(len(submitted), [], [], submitted)

    # get the resource (this is what we are testing)
    rv = client.get(
        f'api/v1/requests?order=submittedDate:{order}&submittedInterval={submitted_interval}',
        headers=create_header(jwt, [User.EDITOR])
    )
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')
    assert len(resp['nameRequests'][0]) > 0

    # check order and that submitted dates are within search interval
    date = resp['nameRequests'][0][0]['submittedDate']
    for nr in resp['nameRequests'][0]:
        if last_date:
            assert nr['submittedDate'] >= last_date.isoformat()
        if order == 'asc':
            assert date <= nr['submittedDate']
        else:
            assert date >= nr['submittedDate']
        date = nr['submittedDate']


@pytest.mark.parametrize('search_name', [
    't',
    'test 1',
    '0 matches',
    'tester',
    'testing',
    'testing tester'
])
def test_namex_search_compname(client, jwt, app, search_name):
    """Test searching by NR names."""
    names = [
        [{'name': 'test1', 'state': 'NE', 'choice': 1}],
        [{'name': 'test 1', 'state': 'NE', 'choice': 1}],
        [{'name': 'test tester 1', 'state': 'NE', 'choice': 1}],
        [{'name': 'testing tester 1', 'state': 'NE', 'choice': 1}],
        [{'name': 'test tester 1', 'state': 'NE', 'choice': 1}],
        [{'name': 'tes', 'state': 'NE', 'choice': 1}, {'name': 'ting', 'state': 'NE', 'choice': 2}]
    ]
    generate_nrs(len(names), [], names, [])

    # get the resource (this is what we are testing)
    rv = client.get(f'api/v1/requests?compName={search_name}', headers=create_header(jwt, [User.EDITOR]))
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')

    # should only contain nrs that contain the search_nr
    for nr in resp['nameRequests'][0]:
        matching_name = False
        for name in nr['names']:
            all_words_match = False
            for word in search_name.upper().split(' '):
                if word not in name['name']:
                    all_words_match = False
                    break
                else:
                    all_words_match = True
            if all_words_match:
                matching_name = True
                break
        # assert at least one name in the NR contained all the search words
        assert matching_name


@pytest.mark.parametrize('consent_option', [
    'All',
    'Received',
    'Yes',
    'No'
])
def test_namex_search_consent(client, jwt, app, consent_option):
    """Test searching by consent."""
    base_nrs = generate_nrs(4, [], [], [])
    base_nrs[0].consentFlag = 'N'
    base_nrs[1].consentFlag = 'Y'
    base_nrs[2].consentFlag = 'R'
    base_nrs[2].consent_dt = datetime.utcnow()
    for nr in base_nrs:
        nr.save_to_db()

    # get the resource (this is what we are testing)
    rv = client.get(f'api/v1/requests?consentOption={consent_option}', headers=create_header(jwt, [User.EDITOR]))
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')
    assert len(resp['nameRequests'][0]) > 0

    if consent_option == 'All':
        # should have returned all nrs
        assert len(resp['nameRequests'][0]) == len(base_nrs)
    else:
        # check it returned NRs based on filter
        for nr in resp['nameRequests'][0]:
            if consent_option == 'Received':
                assert nr['consent_dt'] is not None
            elif consent_option == 'Yes':
                assert nr['consentFlag'] == 'Y'
            else:
                assert nr['consentFlag'] in ['N', None]


@pytest.mark.parametrize('search_name', [
    '1',
    '2',
    '3',
    'no matches'
])
def test_namex_search_first_name(client, jwt, app, search_name):
    """Test search by applicant first name."""
    generate_nrs(5, [], [], [])

    # get the resource (this is what we are testing)
    rv = client.get(f'api/v1/requests?firstName={search_name}', headers=create_header(jwt, [User.EDITOR]))
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')
    if search_name == 'no matches':
        assert len(resp['nameRequests'][0]) == 0
    else:
        assert len(resp['nameRequests'][0]) > 0

    # check it returned NRs based on filter
    for nr in resp['nameRequests'][0]:
        assert search_name in nr['applicants'][0]['firstName']


@pytest.mark.parametrize('search_name', [
    't',
    'test',
    'testing',
    'no matches'
])
def test_namex_search_last_name(client, jwt, app, search_name):
    """Test search by applicant last name."""
    generate_nrs(5, [], [], [])

    # get the resource (this is what we are testing)
    rv = client.get(f'api/v1/requests?lastName={search_name}', headers=create_header(jwt, [User.EDITOR]))
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')
    if search_name == 'no matches':
        assert len(resp['nameRequests'][0]) == 0
    else:
        assert len(resp['nameRequests'][0]) > 0

    # check it returned NRs based on filter
    for nr in resp['nameRequests'][0]:
        assert search_name in nr['applicants'][0]['lastName']


@pytest.mark.parametrize('submitted_start_date, expected_result_count', [
    (get_server_now_with_delta_str(timedelta(days=-1)), 9),
    (get_server_now_with_delta_str(timedelta(days=-2)), 9),
    (get_server_now_with_delta_str(timedelta(-5 * (365) + 1)), 11),
    (get_server_now_with_delta_str(timedelta(-5 * (365))), 12),
    (get_server_now_str(), 6),
    (get_server_now_with_delta_str(timedelta(days=1)), 4),
    (get_server_now_with_delta_str(timedelta(days=5 * (365))), 1),
    (get_server_now_with_delta_str(timedelta(days=5 * (365) + 1)), 0),
])
def test_namex_search_submitted_start_date(client, jwt, app, submitted_start_date, expected_result_count):
    """Test searching by submitted start date."""

    submitted = [
        get_utc_server_now_with_delta(timedelta(days=-5 * (365))),
        get_utc_server_now_with_delta(timedelta(days=-1 * (365))),
        get_utc_server_now_with_delta(timedelta(days=-100)),
        get_utc_server_now_with_delta(timedelta(days=-1)),
        get_utc_server_now_with_delta(timedelta(days=-1)),
        get_utc_server_now_with_delta(timedelta(days=-1)),
        get_utc_server_now(),
        get_utc_server_now(),
        get_utc_server_now_with_delta(timedelta(days=1)),
        get_utc_server_now_with_delta(timedelta(days=100)),
        get_utc_server_now_with_delta(timedelta(days=1 * (365))),
        get_utc_server_now_with_delta(timedelta(days=5 * (365))),
    ]
    generate_nrs(len(submitted), [], [], submitted)

    # get the resource (this is what we are testing)
    rv = client.get(
        f'api/v1/requests?submittedStartDate={submitted_start_date}&rows=1000',
        headers=create_header(jwt, [User.VIEWONLY])
    )
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')
    response_count = len(resp['nameRequests'][0])
    assert response_count >= 0
    assert response_count == expected_result_count


@pytest.mark.parametrize('submitted_end_date, expected_result_count', [
    (get_server_now_with_delta_str(timedelta(-5 * (365) - 1)), 0),
    (get_server_now_with_delta_str(timedelta(-5 * (365))), 1),
    (get_server_now_with_delta_str(timedelta(days=-105)), 2),
    (get_server_now_with_delta_str(timedelta(days=-1)), 6),
    (get_server_now_str(), 8),
    (get_server_now_with_delta_str(timedelta(days=1)), 9),
    (get_server_now_with_delta_str(timedelta(days=1 * (365))), 11),
    (get_server_now_with_delta_str(timedelta(days=5 * (365) - 1)), 11),
    (get_server_now_with_delta_str(timedelta(days=5 * (365))), 12),
    (get_server_now_with_delta_str(timedelta(days=6 * (365))), 12),
])
def test_namex_search_submitted_end_date(client, jwt, app, submitted_end_date, expected_result_count):
    """Test searching by submitted end date."""

    submitted = [
        get_utc_server_now_with_delta(timedelta(days=-5 * (365))),
        get_utc_server_now_with_delta(timedelta(days=-1 * (365))),
        get_utc_server_now_with_delta(timedelta(days=-100)),
        get_utc_server_now_with_delta(timedelta(days=-1)),
        get_utc_server_now_with_delta(timedelta(days=-1)),
        get_utc_server_now_with_delta(timedelta(days=-1)),
        get_utc_server_now(),
        get_utc_server_now(),
        get_utc_server_now_with_delta(timedelta(days=1)),
        get_utc_server_now_with_delta(timedelta(days=100)),
        get_utc_server_now_with_delta(timedelta(days=1 * (365))),
        get_utc_server_now_with_delta(timedelta(days=5 * (365))),
    ]
    generate_nrs(len(submitted), [], [], submitted)

    # get the resource (this is what we are testing)
    rv = client.get(
        f'api/v1/requests?submittedEndDate={submitted_end_date}&rows=1000',
        headers=create_header(jwt, [User.VIEWONLY])
    )
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')
    response_count = len(resp['nameRequests'][0])
    assert response_count >= 0
    assert response_count == expected_result_count


@pytest.mark.parametrize('submitted_start_date, submitted_end_date, expected_result_count', [
    (get_server_now_with_delta_str(timedelta(days=-5 * (365) - 2)), get_server_now_with_delta_str(timedelta(days=-5 * (365) - 1)), 0),
    (get_server_now_with_delta_str(timedelta(days=-5 * (365) - 2)), get_server_now_with_delta_str(timedelta(days=-5 * (365))), 1),
    (get_server_now_with_delta_str(timedelta(days=-5 * (365))), get_server_now_with_delta_str(timedelta(days=-100)), 3),
    (get_server_now_with_delta_str(timedelta(days=-5 * (365))), get_server_now_str(), 8),
    (get_server_now_with_delta_str(timedelta(days=-5 * (365))), get_server_now_with_delta_str(timedelta(days=1 * (365))), 11),
    (get_server_now_with_delta_str(timedelta(days=-5 * (365))), get_server_now_with_delta_str(timedelta(days=5 * (365))), 12),
    (get_server_now_with_delta_str(timedelta(days=-5 * (365))), get_server_now_with_delta_str(timedelta(days=6 * (365))), 12),
    (get_server_now_with_delta_str(timedelta(days=-1)), get_server_now_with_delta_str(timedelta(days=100)), 7),
    (get_server_now_str(), get_server_now_str(), 2),
])
def test_namex_search_submitted_start_and_end_date(client, jwt, app, submitted_start_date, submitted_end_date, expected_result_count):
    """Test searching by submitted start date and submitted end date."""

    submitted = [
        get_utc_server_now_with_delta(timedelta(days=-5 * (365))),
        get_utc_server_now_with_delta(timedelta(days=-1 * (365))),
        get_utc_server_now_with_delta(timedelta(days=-100)),
        get_utc_server_now_with_delta(timedelta(days=-1)),
        get_utc_server_now_with_delta(timedelta(days=-1)),
        get_utc_server_now_with_delta(timedelta(days=-1)),
        get_utc_server_now(),
        get_utc_server_now(),
        get_utc_server_now_with_delta(timedelta(days=1)),
        get_utc_server_now_with_delta(timedelta(days=100)),
        get_utc_server_now_with_delta(timedelta(days=1 * (365))),
        get_utc_server_now_with_delta(timedelta(days=5 * (365))),
    ]
    generate_nrs(len(submitted), [], [], submitted)

    # get the resource (this is what we are testing)
    rv = client.get(
        f'api/v1/requests?submittedStartDate={submitted_start_date}&submittedEndDate={submitted_end_date}&rows=1000',
        headers=create_header(jwt, [User.VIEWONLY])
    )
    data = rv.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('nameRequests') and resp.get('response')
    response_count = len(resp['nameRequests'][0])
    assert response_count >= 0
    assert response_count == expected_result_count


@pytest.mark.parametrize('submitted_start_date, submitted_end_date', [
    ('2021-03-11', '2021-03-01'),
    ('2021-03-11', '2021-03-10'),
    ('2020-03-11', '2000-01-25'),
])
def test_namex_search_submitted_end_date_before_submitted_start_date(client,
                                                                     jwt,
                                                                     app,
                                                                     submitted_start_date,
                                                                     submitted_end_date):
    """Test searching by submitted end date before submitted start date."""

    # get the resource (this is what we are testing)
    rv = client.get(
        f'api/v1/requests?submittedStartDate={submitted_start_date}&submittedEndDate={submitted_end_date}&submittedEndDate={submitted_end_date}&rows=100000',
        headers=create_header(jwt, [User.VIEWONLY])
    )

    assert rv
    assert rv.status_code
    assert rv.status_code == 400
    assert rv.data
    resp = json.loads(rv.data.decode('utf-8'))
    assert resp.get('message')
    assert resp.get('message') == 'submittedEndDate must be after submittedStartDate'


@pytest.mark.parametrize('submitted_interval, submitted_start_date, submitted_end_date', [
    ('Today', '2021-05-01', '2021-05-13'),
    ('7 days', '2021-05-01', '2021-05-13'),
    ('90 days', '2021-05-01', ''),
    ('1 year', '', '2021-05-01'),
])
def test_namex_search_submitted_interval_with_submitted_start_and_end_date(client,
                                                                           jwt,
                                                                           app,
                                                                           submitted_interval,
                                                                           submitted_start_date,
                                                                           submitted_end_date):
    """Test searching by submitted interval with submitted start and end date."""

    # get the resource (this is what we are testing)
    rv = client.get(
        f'api/v1/requests?submittedInterval={submitted_interval}&submittedStartDate={submitted_start_date}&submittedEndDate={submitted_end_date}',
        headers=create_header(jwt, [User.VIEWONLY])
    )

    assert rv
    assert rv.status_code
    assert rv.status_code == 400
    assert rv.data
    resp = json.loads(rv.data.decode('utf-8'))
    assert resp.get('message')
    assert 'submittedInterval cannot be used in conjuction with submittedStartDate and submittedEndDate' in resp.get('message')


@pytest.mark.parametrize('submitted_start_date, submitted_end_date, valid_start_date, valid_end_date', [
    ('11-05-2021', '2021-02-03', False, True),
    ('2021-12-01a', '2001-08-22', False, True),
    ('asdfdsf0sadfsf', '2001-07-11', False, True),
    ('2005-01-12', '05-01-2021', True, False),
    ('2005-01-12', 'asdfsdf', True, False),
    ('2005-01-12', '2005-01-15asd', True, False),
    ('asdfsdf', 'badfasdfsdf', False, False),
    ('02-23-2005', '07-11-2006', False, False),
    ('2005-02-232', '2006-07-113', False, False),
])
def test_namex_search_submitted_start_and_end_date_invalid_date_format(client,
                                                                       jwt,
                                                                       app,
                                                                       submitted_start_date,
                                                                       submitted_end_date,
                                                                       valid_start_date,
                                                                       valid_end_date):
    """Test searching by submitted start and end date with incorrect date formats."""

    # get the resource (this is what we are testing)
    rv = client.get(
        f'api/v1/requests?submittedStartDate={submitted_start_date}&submittedEndDate={submitted_end_date}',
        headers=create_header(jwt, [User.VIEWONLY])
    )

    assert rv
    assert rv.status_code
    assert rv.status_code == 400
    assert rv.data
    resp = json.loads(rv.data.decode('utf-8'))
    msg = resp.get('message')
    assert msg

    if not valid_start_date:
        assert 'Invalid submittedStartDate: ' in msg
        assert 'Must be of date format %Y-%m-%d' in msg
    elif (valid_start_date and not valid_end_date):
        assert 'Invalid submittedEndDate: ' in msg
        assert 'Must be of date format %Y-%m-%d' in msg


@pytest.mark.parametrize('test_name, identifiers, total_results', [
    ('Search for NRs by identifier', ['NR 0', 'NR 1', 'NR 2', 'NR 3'], 4),
    ('Empty Search', [], 0),
])
def test_namex_search_direct_nrs(
    client, jwt, app, test_name, identifiers, total_results
):  # pylint: disable=unused-argument
    """Test searching directly using name requests."""
    base_names = [
        [{'name': 'test1', 'state': 'NE', 'choice': 1}],
        [{'name': 'test 1', 'state': 'NE', 'choice': 1}],
        [{'name': 'test tester 1', 'state': 'NE', 'choice': 1}],
        [{'name': 'testing tester 1', 'state': 'NE', 'choice': 1}],
        [{'name': 'test tester 1', 'state': 'NE', 'choice': 1}]
    ]
    generate_nrs(5, [], base_names, [])
    rv = client.post(
        'api/v1/requests/search',
        headers={**create_header(jwt, [User.SYSTEM]), **{'content-type': 'application/json'}},
        data=json.dumps({
            'identifiers': identifiers
        })
    )

    assert rv.status_code == HTTPStatus.OK

    nrs = [x['nrNum'] for x in rv.json]
    applicants = [x['applicants'][0] for x in rv.json]
    names = [x['names'][0] for x in rv.json]

    for nr in nrs:
        assert nr in identifiers
    assert len(applicants) == total_results
    for name, base_name in zip(names, base_names):
        assert name['name'] == base_name[0]['name'].upper()


def test_request_search_system_only(client, jwt, app):
    """Test request search end point requires system role."""

    # flask-restx / flask-jwt-oidc AttributeError on auth error response (this is a low impact bug in prod)
    with suppress(AttributeError):
        rv = client.post('api/v1/requests/search',
                         headers=create_header(jwt, [User.APPROVER, User.EDITOR, User.VIEWONLY, User.STAFF]),
                         json={'identifiers': []})

        # commented out because unauthorized status code not getting passed by auth error
        # assert rv.status_code == HTTPStatus.UNAUTHORIZED
        assert rv.status_code not in [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.CREATED]
        # assert rv.json['code'] == 'missing_a_valid_role'
        # assert rv.json['description'] == 'Missing a role required to access this endpoint'
