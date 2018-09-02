
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
    # The Flask secret key used to encrypt cookies. This must be kept secret, and should be unique per environment. Do
    # not allow a missing value.
    SECRET_KEY = os.getenv('SOLR_FEEDER_FLASK_SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError('Environment variable SOLR_FEEDER_FLASK_SECRET_KEY in not defined')

    # Turn this off to get rid of warning messages. In future versions of SQLAlchemy, False will be the default and
    # this can be removed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # PostgreSQL Connection information.
    NAMES_DATABASE_USER = os.getenv('SOLR_FEEDER_NAMES_DATABASE_USERNAME', '')
    NAMES_DATABASE_PASSWORD = os.getenv('SOLR_FEEDER_NAMES_DATABASE_PASSWORD', '')
    NAMES_DATABASE_HOST = os.getenv('SOLR_FEEDER_NAMES_DATABASE_HOST', '')
    NAMES_DATABASE_PORT = os.getenv('SOLR_FEEDER_NAMES_DATABASE_PORT', '5432')
    NAMES_DATABASE_NAME = os.getenv('SOLR_FEEDER_NAMES_DATABASE_NAME', 'BC_REGISTRIES_NAMES')
    NAMES_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=NAMES_DATABASE_USER, password=NAMES_DATABASE_PASSWORD, host=NAMES_DATABASE_HOST,
        port=int(NAMES_DATABASE_PORT), name=NAMES_DATABASE_NAME)

    SQLALCHEMY_BINDS = {
        'bc_registries_names_fdw': NAMES_DATABASE_URI
    }

    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
