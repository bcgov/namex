# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""All of the configuration for the service is captured here.

All items are loaded, or have Constants defined here that
are loaded into the Flask configuration.
All modules and lookups get their configuration from the
Flask config, rather than reading environment variables directly
or by accessing this configuration directly.
"""
import os

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())

CONFIGURATION = {
    'development': 'config.DevConfig',
    'testing': 'config.TestConfig',
    'production': 'config.ProdConfig',
    'default': 'config.ProdConfig'
}


def get_named_config(config_name: str = 'production'):
    """Return the configuration object based on the name.

    :raise: KeyError: if an unknown configuration is requested
    """
    if config_name in ['production', 'staging', 'default']:
        app_config = ProdConfig()
    elif config_name == 'testing':
        app_config = TestConfig()
    elif config_name == 'development':
        app_config = DevConfig()
    else:
        raise KeyError(f'Unknown configuration: {config_name}')
    return app_config


class Config():  # pylint: disable=too-few-public-methods
    """Base class configuration that should set reasonable defaults.

    Used as the base for all the other configurations.
    """

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PAYMENT_SVC_URL = os.getenv('PAY_API_URL', None)
    PAYMENT_SVC_VERSION = os.getenv('PAY_API_VERSION', None)

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

    EMAILER_TOPIC = os.getenv('NAMEX_MAILER_TOPIC', '')
    NAMEX_NR_STATE_TOPIC = os.getenv('NAMEX_NR_STATE_TOPIC', '')
    AUDIENCE = os.getenv('AUDIENCE', 'https://pubsub.googleapis.com/google.pubsub.v1.Subscriber')
    PUBLISHER_AUDIENCE = os.getenv('PUBLISHER_AUDIENCE', 'https://pubsub.googleapis.com/google.pubsub.v1.Publisher')
    DEBUG_REQUEST = os.getenv('DEBUG_REQUEST', False)

    ENVIRONMENT = os.getenv('ENVIRONMENT', 'prod')


class DevConfig(Config):  # pylint: disable=too-few-public-methods
    """Creates the Development Config object."""

    TESTING = False
    DEBUG = True


class TestConfig(Config):  # pylint: disable=too-few-public-methods
    """In support of testing only.

    Used by the py.test suite
    """

    DEBUG = True
    TESTING = True
    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_TEST_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DATABASE_TEST_PASSWORD', 'postgres')
    DB_NAME = os.getenv('DATABASE_TEST_NAME', 'unittesting')
    DB_HOST = os.getenv('DATABASE_TEST_HOST', 'localhost')
    DB_PORT = os.getenv('DATABASE_TEST_PORT', '5432')
    if os.getenv('TEST_USE_LOCAL_DB', False):
        SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}'
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}'

    EMAILER_TOPIC = os.getenv('NAMEX_MAILER_TOPIC', '')
    NAMEX_NR_STATE_TOPIC = os.getenv('NAMEX_NR_STATE_TOPIC', '')

class ProdConfig(Config):  # pylint: disable=too-few-public-methods
    """Production environment configuration."""

    TESTING = False
    DEBUG = False

class MigrationConfig(Config):
    """Config for db migration."""

    TESTING = False
    DEBUG = True
