import os

import psycopg2

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


# def test_database_connection_succeed():
#     status = False
#     try:
#         connection = psycopg2.connect(user=os.getenv('DATABASE_USERNAME', ''),
#                                       password=os.getenv('DATABASE_PASSWORD', ''),
#                                       host=os.getenv('DATABASE_HOST', ''),
#                                       port=os.getenv('DATABASE_PORT', '5432'),
#                                       database=os.getenv('DATABASE_NAME', ''))
#         connection.cursor()
#         status = True
#     except Exception:
#         status = False
#     finally:
#         assert status


# def test_sftp_connection_succeed():    # pylint:disable=unused-argument
#     status = False
#     try:
#         SftpService.get_connection()
#         status = True
#     except Exception:
#         status = False
#     finally:
#         assert status
