import os

import psycopg2
import sqlalchemy
from unittest.mock import patch, MagicMock

# from sftp_nuans_report.services.sftp import SftpService


def test_connection_failed():
    status = False
    try:
        connection = psycopg2.connect(
            user=os.getenv('FAKE_PG_USER', ''),
            password=os.getenv('FAKE_PG_PASSWORD', ''),
            host=os.getenv('FAKE_PG_HOST', ''),
            port=os.getenv('FAKE_PG_PORT', '5432'),
            database=os.getenv('FAKE_PG_DB_NAME', ''),
        )

        connection.cursor()
        status = True
    except Exception:
        status = False
    finally:
        assert not status

@patch('cloud_sql_connector.getconn')
def test_database_connection_succeed(mock_getconn):
    mock_connection = MagicMock()
    mock_getconn.return_value = lambda: mock_connection

    engine = sqlalchemy.create_engine(
        'postgresql+pg8000://',
        creator=mock_getconn.return_value
    )

    assert engine is not None



