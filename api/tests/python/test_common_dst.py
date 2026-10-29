
from datetime import datetime, timezone

import pytest

from namex.utils.common import (
    convert_to_utc_min_date_time,
    convert_to_utc_max_date_time,
)


@pytest.mark.parametrize(
    ("date_str", "expected_min_utc", "expected_max_utc"),
    [
        # The day before the DST transition: UTC-7 (PDT)
        (
            "2026-10-31",
            "2026-10-31T07:00:00+00:00",
            "2026-11-01T06:59:59.999999+00:00",
        ),
        # DST transition day: UTC-7 at midnight, then UTC-8 later that day
        (
            "2026-11-01",
            "2026-11-01T07:00:00+00:00",
            "2026-11-02T07:59:59.999999+00:00",
        ),
        # The day after the DST transition: UTC-8 (PST)
        (
            "2026-11-02",
            "2026-11-02T08:00:00+00:00",
            "2026-11-03T07:59:59.999999+00:00",
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
    assert min_utc.tzinfo == timezone.utc
    assert max_utc.tzinfo == timezone.utc
    assert min_utc <= max_utc

