
from datetime import datetime, timedelta

import pytest

from namex.utils.common import (
    convert_to_utc_max_date_time,
    convert_to_utc_min_date_time,
)


@pytest.mark.parametrize(
    ('date_str', 'expected_min_utc', 'expected_max_utc'),
    [
        # The day before the traditional DST transition: UTC-7
        (
            '2026-10-31',
            '2026-10-31T07:00:00+00:00',
            '2026-11-01T06:59:59.999999+00:00',
        ),
        # The traditional DST transition date: UTC-7 throughout
        (
            '2026-11-01',
            '2026-11-01T07:00:00+00:00',
            '2026-11-02T06:59:59.999999+00:00',
        ),
        # The day after the traditional DST transition: UTC-7
        (
            '2026-11-02',
            '2026-11-02T07:00:00+00:00',
            '2026-11-03T06:59:59.999999+00:00',
        ),
    ],
)
def test_convert_to_utc_date_time_across_dst(
    date_str, expected_min_utc, expected_max_utc
):
    min_utc = convert_to_utc_min_date_time(date_str)
    max_utc = convert_to_utc_max_date_time(date_str)

    assert min_utc == datetime.fromisoformat(expected_min_utc)
    assert max_utc == datetime.fromisoformat(expected_max_utc)

    # Verify both datetimes are timezone-aware and have a zero UTC offset.
    assert min_utc.tzinfo is not None
    assert max_utc.tzinfo is not None
    assert min_utc.utcoffset() == timedelta(0)
    assert max_utc.utcoffset() == timedelta(0)

    assert min_utc <= max_utc
