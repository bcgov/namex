"""Config for this service."""
import os
import sys

from dotenv import find_dotenv, load_dotenv


# this will load all the envars from a .env file
load_dotenv(find_dotenv())

CONFIGURATION = {
    'development': 'auto_analyser_uat.config.DevConfig',
    'testing': 'auto_analyser_uat.config.TestConfig',
    'production': 'auto_analyser_uat.config.ProdConfig',
    'default': 'auto_analyser_uat.config.ProdConfig'
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
    SECRET_KEY = 'a secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # URLS
    AUTO_ANALYSE_URL = os.getenv('AUTO_ANALYSE_URL', None)

    # job options
    MAX_ROWS = os.getenv('MAX_ROWS', '100')  # max NRs to test
    UAT_TYPE = os.getenv('UAT_TYPE', 'uat_rejection')  # uat_rejection, uat_accuracy, uat_accuracy_update
    EXCLUDED_NAMES = os.getenv('EXCLUDED_NAMES', None)  # if set, skips names in file
    CSV_FILE = os.getenv('CSV_FILE', None)  # if set, only tests names in file
    PREV_JOB_ID = os.getenv('PREV_JOB_ID', None)  # if set, only tests names tested by given job id

    # UAT database
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

    # Namex database
    NAMEX_DB_USER = os.getenv('NAMEX_DATABASE_USERNAME', '')
    NAMEX_DB_PASSWORD = os.getenv('NAMEX_DATABASE_PASSWORD', '')
    NAMEX_DB_NAME = os.getenv('NAMEX_DATABASE_NAME', '')
    NAMEX_DB_HOST = os.getenv('NAMEX_DATABASE_HOST', '')
    NAMEX_DB_PORT = os.getenv('NAMEX_DATABASE_PORT', '5432')
    NAMEX_SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=NAMEX_DB_USER,
        password=NAMEX_DB_PASSWORD,
        host=NAMEX_DB_HOST,
        port=int(NAMEX_DB_PORT),
        name=NAMEX_DB_NAME,
    )

    SQLALCHEMY_BINDS = {
        'uat_db': SQLALCHEMY_DATABASE_URI,
        'namex': NAMEX_SQLALCHEMY_DATABASE_URI
    }


class DevConfig(Config):
    """Dev environment config."""

    DEBUG = True
    TESTING = True


class TestConfig(Config):
    """Test environment config."""

    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    """Prod environment config."""

    SECRET_KEY = os.getenv('SECRET_KEY', None)

    if not SECRET_KEY:
        SECRET_KEY = os.urandom(24)
        print('WARNING: SECRET_KEY being set as a one-shot', file=sys.stderr)

    TESTING = False
    DEBUG = False
