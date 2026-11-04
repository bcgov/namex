"""Tests for the duplicates report."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock

from notebookreport import processnotebooks, report_run_date

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
    assert 'ORDER BY n.name, r.nr_num' in source


def test_report_run_date_november():
    """Test the report date in November."""
    moment = datetime(2026, 11, 4, 3, 30, tzinfo=timezone.utc)
    assert report_run_date(moment) == '2026-11-03'


def test_report_run_date_january():
    """Test the report date in January."""
    moment = datetime(2026, 1, 16, 7, 30, tzinfo=timezone.utc)
    assert report_run_date(moment) == '2026-01-15'


def test_processnotebooks_failure(monkeypatch, tmp_path):
    """Test a notebook failure."""
    monkeypatch.setattr('notebookreport.pm.execute_notebook', Mock(side_effect=RuntimeError('notebook failed')))
    monkeypatch.setattr('notebookreport.send_email', Mock())
    status = processnotebooks('nr_duplicates_report/daily', str(tmp_path) + os.sep)
    assert status is False
