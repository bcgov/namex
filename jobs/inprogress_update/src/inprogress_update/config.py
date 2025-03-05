"""Config setup for inprogress updater job."""
import os

from dotenv import find_dotenv, load_dotenv


# this will load all the envars from a .env file
load_dotenv(find_dotenv())


class BaseConfig(object):
    """Base config."""

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DISABLE_NAMEREQUEST_NATS_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_NATS_UPDATES', 1))
    MIN_CLIENT_DELAY_SECONDS = os.getenv('MIN_CLIENT_DELAY_SECONDS', '300')
    MIN_EXAMINE_DELAY_SECONDS = os.getenv('MIN_EXAMINE_DELAY_SECONDS', '300')
    MAX_ROWS_LIMIT = os.getenv('MAX_ROWS_LIMIT', '100')
    MIN_DELAY_SECONDS = os.getenv('MIN_DELAY_SECONDS', '600')
    SECRET_KEY = 'a secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NRO_SERVICE_ACCOUNT = os.getenv('NRO_SERVICE_ACCOUNT', 'nro_service_account')
    SQLALCHEMY_MAX_OVERFLOW = 10



    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DB_NAME = os.getenv('DATABASE_NAME', '')
    DB_HOST = os.getenv('DATABASE_HOST', '')
    DB_PORT = os.getenv('DATABASE_PORT', '5432')
    if DB_UNIX_SOCKET := os.getenv('DB_UNIX_SOCKET', None):
        SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host={DB_UNIX_SOCKET}'
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}'

    # Normalize the b64 key: strip whitespace and add padding as needed.
    _key = os.getenv('GCP_AUTH_KEY', None)
    GCP_AUTH_KEY = None if _key is None else "".join(_key.split()) + "=" * (-len("".join(_key.split())) % 4)

    EMAILER_TOPIC = os.getenv('EMAILER_TOPIC', '')
    NAMEX_NR_STATE_TOPIC = os.getenv('NAMEX_NR_STATE_TOPIC', '')


class Config(BaseConfig):
    """Normal config."""

    DEBUG = False
    TESTING = False


class TestConfig(BaseConfig):
    """Test config."""

    DEBUG = True
    TESTING = True

    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_TEST_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_TEST_PASSWORD', '')
    DB_NAME = os.getenv('DATABASE_TEST_NAME', '')
    DB_HOST = os.getenv('DATABASE_TEST_HOST', '')
    DB_PORT = os.getenv('DATABASE_TEST_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
         user=DB_USER,
         password=DB_PASSWORD,
         host=DB_HOST,
         port=int(DB_PORT),
         name=DB_NAME,
    )
