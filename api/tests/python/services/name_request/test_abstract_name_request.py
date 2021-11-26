"""Tests for AbstractNameRequestMixin."""
import datetime

import pytest
from dateutil.tz import gettz

from namex.services.name_request import NameRequestService
from namex.models import Request as RequestDAO

nr_svc = NameRequestService()
pacific_tz = gettz("UTC")


@pytest.mark.parametrize("input_datetime,expected_date", [
    (datetime.datetime(2021, 1, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2021, 3, 25)),
    (datetime.datetime(2021, 2, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2021, 4, 25)),
    (datetime.datetime(2021, 3, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2021, 5, 23)),
    (datetime.datetime(2021, 4, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2021, 6, 23)),
    (datetime.datetime(2021, 5, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2021, 7, 23)),
    (datetime.datetime(2021, 6, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2021, 8, 23)),
    (datetime.datetime(2021, 7, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2021, 9, 22)),
    (datetime.datetime(2021, 8, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2021, 10, 23)),
    (datetime.datetime(2021, 9, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2021, 11, 23)),
    (datetime.datetime(2021, 10, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2021, 12, 23)),
    (datetime.datetime(2021, 11, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2022, 1, 23)),
    (datetime.datetime(2021, 12, 28, 14, 11, 00, tzinfo=pacific_tz), datetime.date(2022, 2, 22))
])
def test_create_expiry_date(input_datetime, expected_date):
    """Test that create_expiry_date method returns a datetime at added X days and at 11:59pm.

    It should not change the time (hour and minute) because of TimeZone offset changes through the year.
    """
    expiry_date = nr_svc.create_expiry_date(input_datetime, 56)
    assert expiry_date
    assert expiry_date.time().hour == 23
    assert expiry_date.time().minute == 59
    assert expiry_date.strftime('%z') in ['-0800', '-0700'] # should not be +0000 or any other
    assert expiry_date.date() == expected_date


def test_extend_expiry_date():
    nr_model = RequestDAO()
    nr_svc.extend_expiry_date(nr_model, days=56)
    assert nr_model.expirationDate.hour == 23