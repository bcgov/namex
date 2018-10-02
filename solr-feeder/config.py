
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

    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
