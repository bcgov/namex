
import os

import dotenv


# Load all the environment variables from a .env file located in some directory above.
dotenv.load_dotenv(dotenv.find_dotenv())

CONFIGURATION = {
    'development': 'solr_feeder.config.DevConfig',
    'testing': 'solr_feeder.config.TestConfig',
    'production': 'solr_feeder.config.ProdConfig',
    'default': 'solr_feeder.config.ProdConfig'
}


class _Config(object):
    """Base class configuration that should set reasonable defaults.

    Used as the base for all the other configurations.
    """

    SECRET_KEY = 'a secret'
    
    COLIN_API_URL = os.getenv('COLIN_SVC_URL', 'http://') + \
        os.getenv('COLIN_SVC_VERSION', '/api/v1')

    SEARCH_API_URL = os.getenv('REGISTRIES_SEARCH_API_INTERNAL_URL', 'http://') \
        + os.getenv('REGISTRIES_SEARCH_API_VERSION', '/api/v1')

    # External API Timeouts
    try:
        AUTH_API_TIMEOUT = int(os.getenv('AUTH_API_TIMEOUT', '20'))
    except:  # pylint: disable=bare-except; # noqa: B901, E722
        AUTH_API_TIMEOUT = 20
    try:
        COLIN_API_TIMEOUT = int(os.getenv('COLIN_API_TIMEOUT', '20'))
    except:  # pylint: disable=bare-except; # noqa: B901, E722
        COLIN_API_TIMEOUT = 20
    try:
        SEARCH_API_TIMEOUT = int(os.getenv('SEARCH_API_TIMEOUT', '20'))
    except:  # pylint: disable=bare-except; # noqa: B901, E722
        SEARCH_API_TIMEOUT = 20

    KEYCLOAK_AUTH_TOKEN_URL = os.getenv('KEYCLOAK_AUTH_TOKEN_URL')
    KEYCLOAK_SERVICE_ACCOUNT_ID = os.getenv('BUSINESS_SEARCH_SERVICE_ACCOUNT_CLIENT_ID')
    KEYCLOAK_SERVICE_ACCOUNT_SECRET = os.getenv('BUSINESS_SEARCH_SERVICE_ACCOUNT_SECRET')

    DEBUG = False
    TESTING = False


class DevConfig(_Config):
    DEBUG = True
    TESTING = True


class TestConfig(_Config):
    DEBUG = True
    TESTING = True

class ProdConfig(_Config):
    SECRET_KEY = os.getenv('SOLR_FEEDER_FLASK_SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError('Environment variable SOLR_FEEDER_FLASK_SECRET_KEY in not defined')
