import importlib.util
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytz
import pytest

_path = Path(__file__).parents[1] / "src" / "bad_designation_notifier" / "services" / "utils.py"
_spec = importlib.util.spec_from_file_location("designation_utils", _path)
utils = importlib.util.module_from_spec(_spec)
sys.modules["designation_utils"] = utils
_spec.loader.exec_module(utils)


@pytest.mark.parametrize(
    ("instant", "expected"),
    [
        (datetime(2026, 11, 2, 7, 30, tzinfo=pytz.utc), "2026-11-01"),
        (datetime(2026, 1, 16, 7, 30, tzinfo=pytz.utc), "2026-01-14"),
    ],
)
def test_get_yesterday_str(instant, expected):
    with patch("designation_utils.datetime") as clock:
        clock.now.return_value = instant
        assert utils.get_yesterday_str() == expected
