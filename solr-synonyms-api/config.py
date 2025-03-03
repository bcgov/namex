
import os

import dotenv


# Load all the environment variables from a .env file located in some directory above.
dotenv.load_dotenv(dotenv.find_dotenv())

CONFIGURATION = {
    'development': 'config.DevConfig',
    'testing': 'config.TestConfig',
    'production': 'config.Config',
    'default': 'config.Config'
}


class Config(object):
    """Create base config object."""

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    # The Flask secret key used to encrypt cookies. This must be kept secret and should be unique per environment. Do
    # not allow a missing value.
    SECRET_KEY = os.getenv('SOLR_SYNONYMS_API_FLASK_SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError('Environment variable SOLR_SYNONYMS_API_FLASK_SECRET_KEY in not defined')

    # Turn this off to get rid of warning messages. In future versions of SQLAlchemy, False will be the default and
    # this can be removed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # PostgreSQL Connection information.
    DATABASE_USER = os.getenv('SOLR_SYNONYMS_API_DATABASE_USERNAME', '')
    DATABASE_PASSWORD = os.getenv('SOLR_SYNONYMS_API_DATABASE_PASSWORD', '')
    DATABASE_HOST = os.getenv('SOLR_SYNONYMS_API_DATABASE_HOST', '')
    DATABASE_PORT = os.getenv('SOLR_SYNONYMS_API_DATABASE_PORT', '5432')
    DATABASE_NAME = os.getenv('SOLR_SYNONYMS_API_DATABASE_NAME', 'solr')
    if DATABASE_UNIX_SOCKET := os.getenv('SOLR_SYNONYMS_API_DATABASE_UNIX_SOCKET', None):
        SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@/{DATABASE_NAME}?host={DATABASE_UNIX_SOCKET}'
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{int(DATABASE_PORT)}/{DATABASE_NAME}'

    DEBUG = False
    TESTING = False


class DevConfig(Config):
    """Dev config."""

    DEBUG = True
    TESTING = True


class TestConfig(Config):
    """Test config."""

    DEBUG = True
    TESTING = True
