from datetime import datetime, timezone

import pytest

from namex.resources.name_requests.report_resource import to_vancouver_datetime


@pytest.mark.parametrize(
    ("utc_timestamp", "expected_local"),
    [
        # Before the November 1, 2026 change
        (
            "2026-10-31T12:00:00Z",
            "2026-10-31T05:00:00-07:00",
        ),
        # On November 1, 2026
        (
            "2026-11-01T12:00:00Z",
            "2026-11-01T05:00:00-07:00",
        ),
        # After November 1, 2026: expect permanent UTC-7
        (
            "2026-11-02T12:00:00Z",
            "2026-11-02T05:00:00-07:00",
        ),
    ],
)
def test_vancouver_datetime_uses_utc_minus_7(utc_timestamp, expected_local):
    result = to_vancouver_datetime(utc_timestamp)

    assert result.isoformat() == expected_local
    assert result.utcoffset().total_seconds() == -7 * 60 * 60


def test_naive_datetime_is_assumed_to_be_utc():
    result = to_vancouver_datetime(datetime(2026, 11, 2, 12, 0, 0))

    assert result.isoformat() == "2026-11-02T05:00:00-07:00"


def test_utc_aware_datetime_converts_to_vancouver_time():
    utc_datetime = datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc)

    result = to_vancouver_datetime(utc_datetime)

    assert result.isoformat() == "2026-11-02T05:00:00-07:00"


def test_invalid_input_raises_type_error():
    with pytest.raises(TypeError):
        to_vancouver_datetime(123)