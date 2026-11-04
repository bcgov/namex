"""test job for the notebook."""
import os

import psycopg2

from notebookreport import processnotebooks


def test_connection_failed():
    """Test connection failed for the notebook."""
    status = False
    try:
        connection = psycopg2.connect(user=os.getenv('FAKE_PG_USER', ''),
                                      password=os.getenv('FAKE_PG_PASSWORD', ''),
                                      host=os.getenv('FAKE_PG_HOST', ''),
                                      port=os.getenv('FAKE_PG_PORT', '5432'),
                                      database=os.getenv('FAKE_PG_DB_NAME', ''))

        connection.cursor()
        status = True
    except Exception:  # noqa: B902
        status = False
    finally:
        assert status is False


def test_connection_succeed():
    """Test connection succeed for the notebook report."""
    status = False
    try:
        connection = psycopg2.connect(user=os.getenv('PG_USER', ''),
                                      password=os.getenv('PG_PASSWORD', ''),
                                      host=os.getenv('PG_HOST', ''),
                                      port=os.getenv('PG_PORT', '5432'),
                                      database=os.getenv('PG_DB_NAME', ''))
        connection.cursor()
        status = True
    except Exception:  # noqa: B902
        status = False
    finally:
        assert status is True


def test_daily_notebook_report():
    """Test daily notebook report."""
    status = processnotebooks('daily')

    assert status is True
