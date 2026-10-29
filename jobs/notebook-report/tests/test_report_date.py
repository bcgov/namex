import importlib.util
import sys
import types
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytz

def _stub(name, **attrs):
    if name in sys.modules:
        return
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module


_stub("papermill")
_stub("requests")
_stub("flask", Flask=object, current_app=None)
_stub("structured_logging", StructuredLogging=object)
_stub("config", Config=object)

_path = Path(__file__).parents[1] / "src" / "notebookreport.py"
_spec = importlib.util.spec_from_file_location("notebookreport", _path)
report = importlib.util.module_from_spec(_spec)
sys.modules["notebookreport"] = report
_spec.loader.exec_module(report)


def test_vancouver_yesterday():
    cases = [
        (datetime(2026, 11, 2, 15, tzinfo=pytz.utc), "2026-11-01", 0),
        (datetime(2026, 1, 16, 16, tzinfo=pytz.utc), "2026-01-15", 4),
        (datetime(2026, 11, 2, 4, tzinfo=pytz.utc), "2026-10-31", 6),
    ]
    for instant, yesterday, weekday in cases:
        with patch("notebookreport.datetime") as clock:
            clock.now.return_value = instant
            local_now = report.vancouver_now()
            assert (local_now - report.timedelta(days=1)).strftime("%Y-%m-%d") == yesterday
            assert local_now.weekday() == weekday
