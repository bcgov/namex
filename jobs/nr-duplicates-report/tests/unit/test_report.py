"""Tests for the duplicates report."""
import json
import os
from datetime import datetime, timezone
from http import HTTPStatus
from pathlib import Path
from unittest.mock import Mock

from flask.globals import _cv_app
from notebookreport import (findfiles, processnotebooks, report_run_date,
                            send_email)
from util.email import process_attachments, send_email_notification
from util.token import get_bearer_token


def _clear_app_context():
    ctx = _cv_app.get(None)
    while ctx is not None:
        ctx.pop()
        ctx = _cv_app.get(None)


NOTEBOOK = Path(__file__).resolve().parents[2] / 'nr_duplicates_report' / 'daily' / 'nr-duplicates.ipynb'


def _notebook_source():
    notebook = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
    return '\n'.join(''.join(cell['source']) for cell in notebook['cells'])


def test_duplicate_query():
    """Test the duplicate query."""
    source = _notebook_source()
    assert "state_cd = 'DRAFT'" in source
    assert 'America/Vancouver' in source
    assert "INTERVAL '7 days'" in source
    assert 'n.choice = 1' in source
    assert "NOT LIKE 'NR L%'" in source
    assert 'name_without_designation' in source
    assert 'n.designation' in source
    assert 'name AS "NR NAME"' in source
    assert 'ORDER BY name, nr_num' in source


def test_report_run_date_november():
    """Test the report date in November."""
    moment = datetime(2026, 11, 4, 3, 30, tzinfo=timezone.utc)
    assert report_run_date(moment) == '2026-11-03'


def test_report_run_date_january():
    """Test the report date in January."""
    moment = datetime(2026, 1, 16, 7, 30, tzinfo=timezone.utc)
    assert report_run_date(moment) == '2026-01-15'


def test_report_run_date_now(monkeypatch):
    """Test the report date when the caller does not pass one."""
    class FixedDate(datetime):
        """FixedDate."""

        @classmethod
        def now(cls, tz=None):
            """now."""
            return datetime(2026, 11, 4, 3, 30, tzinfo=timezone.utc)

    monkeypatch.setattr('notebookreport.datetime', FixedDate)
    assert report_run_date() == '2026-11-03'


def test_findfiles(tmp_path):
    """Test finding a notebook file."""
    (tmp_path / 'Report.TXT').write_text('x', encoding='utf-8')
    (tmp_path / 'other.csv').write_text('x', encoding='utf-8')
    found = list(findfiles(str(tmp_path), '*.txt'))
    assert found == [os.path.join(str(tmp_path), 'Report.TXT')]


def test_send_email(app, monkeypatch):
    """Test the report mail and the error mail."""
    notify = Mock()
    monkeypatch.setattr('notebookreport.send_email_notification', notify)
    monkeypatch.setattr('notebookreport.Config.ERROR_EMAIL_RECIPIENTS', '[a@example.com, b@example.com]')
    monkeypatch.setattr('notebookreport.Config.REPORT_RECIPIENTS', ['c@example.com'])
    monkeypatch.setenv('ENVIRONMENT', 'dev')
    with app.app_context():
        send_email('ERROR', 'boom')
        send_email('', '')
    monkeypatch.setenv('ENVIRONMENT', 'prod')
    with app.app_context():
        send_email('', '')
    assert notify.call_count == 3


def test_processnotebooks_success(monkeypatch, tmp_path):
    """Test a notebook that finishes."""
    def execute(notebook, output, parameters=None):
        Path(output).write_text('ok', encoding='utf-8')

    monkeypatch.setattr('notebookreport.pm.execute_notebook', execute)
    monkeypatch.setattr('notebookreport.send_email', Mock())
    status = processnotebooks('nr_duplicates_report/daily', str(tmp_path) + os.sep)
    _clear_app_context()
    assert status is True


def test_processnotebooks_failure(monkeypatch, tmp_path):
    """Test a notebook failure."""
    monkeypatch.setattr('notebookreport.pm.execute_notebook', Mock(side_effect=RuntimeError('notebook failed')))
    monkeypatch.setattr('notebookreport.send_email', Mock())
    status = processnotebooks('nr_duplicates_report/daily', str(tmp_path) + os.sep)
    _clear_app_context()
    assert status is False


def test_send_email_notification(app, monkeypatch, tmp_path):
    """Test the notify call."""
    attachment = tmp_path / 'nr_duplicates.csv'
    attachment.write_text('id', encoding='utf-8')
    monkeypatch.setattr('util.email.get_bearer_token', Mock(return_value='token'))
    response = Mock(status_code=HTTPStatus.OK, text='ok')
    monkeypatch.setattr('util.email.requests.post', Mock(return_value=response))
    with app.app_context():
        send_email_notification(['a@example.com'], 'subject', 'body', [str(attachment)])
        response.status_code = HTTPStatus.BAD_REQUEST
        send_email_notification(['a@example.com'], 'subject', 'body', [])


def test_send_email_notification_without_recipients(app):
    """Test a mail with no recipients."""
    with app.app_context():
        try:
            send_email_notification([], 'subject', 'body', [])
            raised = False
        except ValueError:
            raised = True
    assert raised is True


def test_process_attachments_failure(app, tmp_path):
    """Test an attachment that cannot be read."""
    with app.app_context():
        try:
            process_attachments([str(tmp_path / 'missing.csv')])
            raised = False
        except OSError:
            raised = True
    assert raised is True


def test_bearer_token(app, monkeypatch):
    """Test the service token."""
    wrapped = get_bearer_token.__func__ if isinstance(get_bearer_token, staticmethod) else get_bearer_token
    wrapped.cache_clear()
    response = Mock()
    response.json.return_value = {'access_token': 'abc'}
    monkeypatch.setattr('util.token.requests.post', Mock(return_value=response))
    with app.app_context():
        assert get_bearer_token() == 'abc'
        wrapped.cache_clear()
        response.json.side_effect = ValueError('not json')
        assert get_bearer_token() is None
