import importlib.util
import sys
import types
import zoneinfo
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

import pytest


class _Logger:
    def info(self, *args, **kwargs):
        return None


class _App:
    def __init__(self):
        self.logger = _Logger()
        self.config = self

    def from_object(self, config):
        return None


class _StructuredLogging:
    def init_app(self, app):
        return None

    def get_logger(self):
        return _Logger()


class _Response:
    def __init__(self, status_code):
        self.status_code = status_code


def _stub(name, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module


_stub("papermill")
_stub("requests", request=lambda *args, **kwargs: _Response(200))
_stub("flask", Flask=lambda name: _App(), current_app=_App())
_stub("structured_logging", StructuredLogging=_StructuredLogging)
_stub("config", Config=type("Config", (), {}))

_path = Path(__file__).parents[1] / "src" / "notebookreport.py"
_spec = importlib.util.spec_from_file_location("notebookreport", _path)
report = importlib.util.module_from_spec(_spec)
sys.modules["notebookreport"] = report
_spec.loader.exec_module(report)


def _configure(environment):
    report.Config.ENVIRONMENT = environment
    report.Config.WEEK_REPORT_DATE = "[0, 1, 2, 3, 4, 5]"
    report.Config.DAILY_REPORT_RECIPIENTS = "daily@example.com"
    report.Config.WEEKLY_REPORT_NAMEX_RECIPIENTS = "weekly@example.com"
    report.Config.ERROR_EMAIL_RECIPIENTS = "errors@example.com"
    report.Config.NOTIFY_API_URL = "http://notify.example/notify"


def _notebook(tmp, kind, date, write_csv):
    folder = tmp / kind
    folder.mkdir()
    stem = "daily" if kind == "daily" else "weeklynamex"
    (folder / f"{stem}.ipynb").write_text("{}", encoding="utf-8")
    if write_csv:
        name = f"daily_totals_{date}.csv" if kind == "daily" else f"weekly_totals_till_{date}.csv"
        (folder / name).write_text("count\n1\n", encoding="utf-8")


def _execute(input_path, output_path, parameters=None, cwd=None):
    Path(output_path).write_text("{}", encoding="utf-8")


def _run(tmp, monkeypatch, instant, kind, environment, write_csv, execute):
    _configure(environment)
    yesterday = (instant.astimezone(ZoneInfo("America/Vancouver"))
                 - report.timedelta(days=1)).strftime("%Y-%m-%d")
    _notebook(tmp, kind, yesterday, write_csv)
    monkeypatch.chdir(tmp)
    monkeypatch.setattr(report.pm, "execute_notebook", execute, raising=False)
    sent = []

    def _request(method, url, json=None, headers=None):
        sent.append(json)
        return _Response(200)

    monkeypatch.setattr(report.requests, "request", _request)
    with patch("notebookreport.datetime") as clock:
        clock.now.return_value = instant
        report.processnotebooks(kind, "token")
    return sent


def test_vancouver_zone_file():
    assert zoneinfo.TZPATH == ()
    zone = ZoneInfo("America/Vancouver")
    nov = datetime(2026, 11, 1, 9, 1, tzinfo=timezone.utc).astimezone(zone)
    jan = datetime(2026, 1, 15, 20, tzinfo=timezone.utc).astimezone(zone)
    assert nov.strftime("%z") == "-0700"
    assert jan.strftime("%z") == "-0800"


def test_vancouver_yesterday():
    cases = [
        (datetime(2026, 11, 2, 7, 30, tzinfo=timezone.utc), "2026-11-01", 0),
        (datetime(2026, 11, 2, 15, tzinfo=timezone.utc), "2026-11-01", 0),
        (datetime(2026, 1, 16, 16, tzinfo=timezone.utc), "2026-01-15", 4),
        (datetime(2026, 11, 2, 4, tzinfo=timezone.utc), "2026-10-31", 6),
    ]
    for instant, yesterday, weekday in cases:
        with patch("notebookreport.datetime") as clock:
            clock.now.return_value = instant
            local_now = report.vancouver_now()
            assert (local_now - report.timedelta(days=1)).strftime("%Y-%m-%d") == yesterday
            assert local_now.weekday() == weekday


def test_create_app_and_findfiles(tmp_path):
    app = report.create_app()
    assert app.logger is not None
    (tmp_path / "daily.ipynb").write_text("{}", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("x", encoding="utf-8")
    found = list(report.findfiles(tmp_path, "*.ipynb"))
    assert found == [str(tmp_path / "daily.ipynb")]


def test_send_email_raises_when_notify_fails():
    _configure("dev")
    with patch.object(report.requests, "request", return_value=_Response(500)):
        with pytest.raises(Exception, match="Unsuccessful response when sending email."):
            report.send_email({"recipients": "daily@example.com"}, "token")


def test_daily_subject_uses_vancouver_yesterday(tmp_path, monkeypatch):
    instant = datetime(2026, 11, 2, 15, tzinfo=timezone.utc)
    sent = _run(tmp_path, monkeypatch, instant, "daily", "dev", True, _execute)
    assert sent[0]["content"]["subject"] == "Daily NameX Stats for 2026-11-01 on dev"
    assert sent[0]["content"]["attachments"][0]["fileBytes"]


def test_weekly_subject_and_prod_have_no_environment_suffix(tmp_path, monkeypatch):
    instant = datetime(2026, 1, 16, 16, tzinfo=timezone.utc)
    sent = _run(tmp_path, monkeypatch, instant, "weekly", "prod", True, _execute)
    assert sent[0]["content"]["subject"] == "Weekly NameX Stats till 2026-01-15"


def test_weekly_report_does_not_run_on_sunday(tmp_path, monkeypatch):
    instant = datetime(2026, 11, 2, 4, tzinfo=timezone.utc)
    sent = _run(tmp_path, monkeypatch, instant, "weekly", "dev", False, _execute)
    assert sent == []


def test_failed_notebook_sends_the_error_mail(tmp_path, monkeypatch):
    instant = datetime(2026, 11, 2, 15, tzinfo=timezone.utc)

    def _boom(input_path, output_path, parameters=None, cwd=None):
        raise RuntimeError("notebook failed")

    sent = _run(tmp_path, monkeypatch, instant, "daily", "dev", False, _boom)
    assert sent[0]["recipients"] == "errors@example.com"
    assert sent[0]["content"]["subject"] == (
        "Error Notification Daily NameX Stats for 2026-11-01 on dev"
    )
