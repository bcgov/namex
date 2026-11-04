import importlib.util
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest
import pytz

_path = Path(__file__).parents[1] / "src" / "services" / "utils.py"
_spec = importlib.util.spec_from_file_location("bad_name_utils", _path)
utils = importlib.util.module_from_spec(_spec)
sys.modules["bad_name_utils"] = utils
_spec.loader.exec_module(utils)


@pytest.mark.parametrize("parts, title, start, end", [
    ((2026, 11, 2, 15), "2026-11-01",
     "2026-11-01 07:00:00", "2026-11-02 07:00:00"),
    ((2026, 1, 16, 16), "2026-01-15",
     "2026-01-15 08:00:00", "2026-01-16 08:00:00"),
    ((2026, 11, 2, 4), "2026-10-31",
     "2026-10-31 07:00:00", "2026-11-01 07:00:00"),
])
def test_yesterday(parts, title, start, end):
    instant = datetime(*parts, tzinfo=pytz.utc)
    with patch("bad_name_utils.datetime") as clock:
        clock.now.return_value = instant
        assert utils.get_yesterday_str() == title
        assert utils.get_yesterday_utc_range() == (start, end)
