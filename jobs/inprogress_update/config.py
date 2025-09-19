"""Config setup for inprogress updater job."""
import os

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file
load_dotenv(find_dotenv())


class BaseConfig(object):
    """Base config."""

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    MIN_CLIENT_DELAY_SECONDS = os.getenv('MIN_CLIENT_DELAY_SECONDS', '300')
    MIN_EXAMINE_DELAY_SECONDS = os.getenv('MIN_EXAMINE_DELAY_SECONDS', '300')
    MAX_ROWS_LIMIT = os.getenv('MAX_ROWS_LIMIT', '100')
    MIN_DELAY_SECONDS = os.getenv('MIN_DELAY_SECONDS', '600')
    SECRET_KEY = 'a secret'  # noqa: S105
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NRO_SERVICE_ACCOUNT = os.getenv('NRO_SERVICE_ACCOUNT', 'nro_service_account')
    SQLALCHEMY_MAX_OVERFLOW = 10

    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'postgres')
    DB_NAME = os.getenv('DATABASE_NAME', 'unittesting')
    DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DB_PORT = int(os.getenv('DATABASE_PORT', '5432'))

    DB_SCHEMA = os.getenv('DATABASE_SCHEMA', 'public')
    DB_IP_TYPE = os.getenv('DATABASE_IP_TYPE', 'private')
    DB_OWNER = os.getenv('DATABASE_OWNER', 'postgres')

    if DB_INSTANCE_CONNECTION_NAME := os.getenv('DATABASE_INSTANCE_CONNECTION_NAME', None):
        SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://'
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

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
    DB_USER = os.getenv('DATABASE_TEST_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DATABASE_TEST_PASSWORD', 'postgres')
    DB_NAME = os.getenv('DATABASE_TEST_NAME', 'unittesting')
    DB_HOST = os.getenv('DATABASE_TEST_HOST', 'localhost')
    DB_PORT = os.getenv('DATABASE_TEST_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}'
