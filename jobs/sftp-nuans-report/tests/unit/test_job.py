import os

import psycopg2
import sqlalchemy
from cloud_sql_connector import DBConfig, getconn

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

def test_database_connection_succeed():
    config = DBConfig(
        instance_name=os.getenv("DATABASE_INSTANCE_CONNECTION_NAME"),
        database=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USERNAME"),
        ip_type="public",
        schema=os.getenv("DATABASE_SCHEMA"),
    )

    # SQLAlchemy engine
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn(config)
    )

    assert engine is not None



