"""Tests for AbstractNameRequestMixin."""
import datetime

import pytest
from dateutil.tz import gettz

from namex.services.name_request import NameRequestService
from namex.models import Request as RequestDAO

nr_svc = NameRequestService()
pacific_tz = gettz('US/Pacific')
utc_tz = gettz('UTC')


@pytest.mark.parametrize('input_datetime_utc,expected_date_utc', [
    (datetime.datetime(2021, 1, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 3, 26, 6, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 1, 28, 11, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 3, 25, 6, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 2, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 4, 25, 6, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 3, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 5, 23, 6, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 4, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 6, 23, 6, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 5, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 7, 23, 6, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 6, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 8, 23, 6, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 7, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 9, 22, 6, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 8, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 10, 23, 6, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 9, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 11, 23, 7, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 10, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2021, 12, 23, 7, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 11, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2022, 1, 23, 7, 59, 0, tzinfo=utc_tz)),
    (datetime.datetime(2021, 12, 28, 14, 11, 00, tzinfo=utc_tz), datetime.datetime(2022, 2, 22, 7, 59, 0, tzinfo=utc_tz))
])
def test_create_expiry_date(input_datetime_utc, expected_date_utc):
    """
    Test that create_expiry_date method returns a datetime at added X days and at 11:59pm.

    It should not change the time (hour and minute in PST) because of TimeZone offset changes through the year.

    Dates in 2021 between 2:00 a.m. on Sunday, March 14 to 2:00 a.m. on Sunday, November 7 should have their time
    at 6:59am next day in UTC. Other dates should have their time at 7:59am next day in UTC.
    """
    expiry_date = nr_svc.create_expiry_date(input_datetime_utc, 56)
    assert expiry_date
    # Time in PST should always be 11:59pm
    assert expiry_date.astimezone(pacific_tz).time().hour == 23
    assert expiry_date.astimezone(pacific_tz).time().minute == 59

    assert expiry_date.strftime('%z') in ['-0800', '-0700'] # should not be +0000 or any other
    assert expiry_date.astimezone(utc_tz).hour == expected_date_utc.hour
    assert expiry_date.astimezone(utc_tz).minute == expected_date_utc.minute
