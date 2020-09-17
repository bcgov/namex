"""Config for this service."""
import os
import sys

from dotenv import find_dotenv, load_dotenv


# this will load all the envars from a .env file
load_dotenv(find_dotenv())

CONFIGURATION = {
    'development': 'config.DevConfig',
    'testing': 'config.TestConfig',
    'production': 'config.ProdConfig',
    'default': 'config.ProdConfig'
}


def get_named_config(config_name: str = 'production'):
    """Return the configuration object based on the name."""
    if config_name in ['production', 'staging', 'default']:
        config = ProdConfig()
    elif config_name == 'testing':
        config = TestConfig()
    elif config_name == 'development':
        config = DevConfig()
    else:
        raise KeyError(f"Unknown configuration '{config_name}'")
    return config


class Config(object):
    """Base config init."""

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    MAX_ROW_LIMIT = os.getenv('MAX_ROWS', '100')
    MIN_DELAY_SECONDS = os.getenv('MIN_DELAY_SECONDS', '600')
    SECRET_KEY = 'a secret'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STALE_THRESHOLD = os.getenv('STALE_THRESHOLD', '1800')
    MAX_ROWS_LIMIT = os.getenv('STALE_THRESHOLD', '100')
    SOLR_BASE_URL = os.getenv('SOLR_BASE_URL', None)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_MAX_OVERFLOW = 10

    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DB_NAME = os.getenv('DATABASE_NAME', '')
    DB_HOST = os.getenv('DATABASE_HOST', '')
    DB_PORT = os.getenv('DATABASE_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        name=DB_NAME,
    )


class DevConfig(Config):
    """Dev environment config."""

    DEBUG = True
    TESTING = True


class TestConfig(Config):
    """Test environment config."""

    DEBUG = True
    TESTING = True

    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DB_NAME = os.getenv('DATABASE_NAME_TEST', '')
    DB_HOST = os.getenv('DATABASE_HOST', '')
    DB_PORT = os.getenv('DATABASE_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        name=DB_NAME,
    )


class ProdConfig(Config):
    """Prod environment config."""

    SECRET_KEY = os.getenv('SECRET_KEY', None)

    if not SECRET_KEY:
        SECRET_KEY = os.urandom(24)
        print('WARNING: SECRET_KEY being set as a one-shot', file=sys.stderr)

    TESTING = False
    DEBUG = False
