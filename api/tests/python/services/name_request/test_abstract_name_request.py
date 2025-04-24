"""Tests for AbstractNameRequestMixin."""

import datetime

import pytest
from dateutil.tz import gettz

from namex.constants import RequestAction
from namex.models import Request as RequestDAO
from namex.models import State
from namex.services.name_request import NameRequestService

nr_svc = NameRequestService()
pacific_tz = gettz('US/Pacific')
utc_tz = gettz('UTC')


@pytest.mark.parametrize(
    'input_datetime_utc,expected_date_utc,time_offset',
    [
        (
            datetime.datetime(2021, 1, 28, 8, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2021, 3, 26, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 1, 28, 7, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2021, 3, 25, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 2, 28, 8, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2021, 4, 26, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 2, 28, 7, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2021, 4, 25, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 3, 28, 7, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2021, 5, 24, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 3, 28, 6, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2021, 5, 23, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 4, 28, 7, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2021, 6, 24, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 4, 28, 6, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2021, 6, 23, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 5, 28, 7, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2021, 7, 24, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 5, 28, 6, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2021, 7, 23, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 6, 28, 7, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2021, 8, 24, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 6, 28, 6, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2021, 8, 23, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 7, 28, 7, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2021, 9, 23, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 7, 28, 6, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2021, 9, 22, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 8, 28, 7, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2021, 10, 24, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 8, 28, 6, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2021, 10, 23, 6, 59, 0, tzinfo=utc_tz),
            '-0700',
        ),
        (
            datetime.datetime(2021, 9, 28, 7, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2021, 11, 24, 7, 59, 0, tzinfo=utc_tz),
            '-0800',
        ),
        (
            datetime.datetime(2021, 9, 28, 6, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2021, 11, 23, 7, 59, 0, tzinfo=utc_tz),
            '-0800',
        ),
        (
            datetime.datetime(2021, 10, 28, 7, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2021, 12, 24, 7, 59, 0, tzinfo=utc_tz),
            '-0800',
        ),
        (
            datetime.datetime(2021, 10, 28, 6, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2021, 12, 23, 7, 59, 0, tzinfo=utc_tz),
            '-0800',
        ),
        (
            datetime.datetime(2021, 11, 28, 8, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2022, 1, 24, 7, 59, 0, tzinfo=utc_tz),
            '-0800',
        ),
        (
            datetime.datetime(2021, 11, 28, 7, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2022, 1, 23, 7, 59, 0, tzinfo=utc_tz),
            '-0800',
        ),
        (
            datetime.datetime(2021, 12, 28, 8, 0, 0, tzinfo=utc_tz),
            datetime.datetime(2022, 2, 23, 7, 59, 0, tzinfo=utc_tz),
            '-0800',
        ),
        (
            datetime.datetime(2021, 12, 28, 7, 59, 59, tzinfo=utc_tz),
            datetime.datetime(2022, 2, 22, 7, 59, 0, tzinfo=utc_tz),
            '-0800',
        ),
    ],
)
def test_create_expiry_date(input_datetime_utc, expected_date_utc, time_offset):
    """
    Test that create_expiry_date method returns a datetime at added X days and at 11:59pm Pacific time.

    It should not change the time (hour and minute in Pacific time) because of timezone offset changes through the year.

    Dates in 2021 between 2:00 a.m. on Sunday, March 14 to 2:00 a.m. on Sunday, November 7 should have their time
    at 6:59am next day in UTC. Other dates should have their time at 7:59am next day in UTC.
    """
    expiry_date = nr_svc.create_expiry_date(input_datetime_utc, 56)
    assert expiry_date
    # Time in PST should always be 11:59pm
    assert expiry_date.astimezone(pacific_tz).time().hour == 23
    assert expiry_date.astimezone(pacific_tz).time().minute == 59

    assert expiry_date.strftime('%z') == time_offset

    expiry_date_in_utc = expiry_date.astimezone(utc_tz)
    assert expiry_date_in_utc.year == expected_date_utc.year
    assert expiry_date_in_utc.month == expected_date_utc.month
    assert expiry_date_in_utc.day == expected_date_utc.day
    # Time in UTC will vary depending on the time offset (summer savings time)
    assert expiry_date_in_utc.hour == expected_date_utc.hour
    assert expiry_date_in_utc.minute == expected_date_utc.minute
    assert expiry_date_in_utc.second == expected_date_utc.second


@pytest.mark.parametrize(
    'test_name, action_cd, request_type, days',
    [
        ('Testing an NR restoration', RequestAction.REH.value, 'RCR', 421),
        ('Testing an NR reinstatement', RequestAction.REN.value, 'RCR', 421),
        ('Testing an NR NRO restoration', RequestAction.REST.value, 'RCR', 421),
        ('Testing an NR RequestAction is new, Benefit Restore_Reinstate', RequestAction.NEW.value, 'BERE', 421),
        ('Testing an NR RequestAction is null, BC Comp Restore_Reinstate', None, 'RCR', 421),
        ('Testing an NR RequestAction is null, BC Company', None, 'CR', 56),
        ('Testing an NR RequestAction is new, BC Company', RequestAction.NEW.value, 'CR', 56),
    ],
)
def test_get_expiry_days(client, test_name, days, action_cd, request_type):
    """
    Test that get_expiry_date method returns a either 56 or 421 days
    """
    mock_nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    mock_nr.stateCd = State.APPROVED
    mock_nr.request_action_cd = action_cd
    mock_nr.requestTypeCd = request_type
    mock_nr.expirationDate = None
    mock_expiry_days = int(nr_svc.get_expiry_days(mock_nr.request_action_cd, mock_nr.activeUser.requestTypeCd))

    assert mock_expiry_days == days
