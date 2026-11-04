# Copyright © 2021 Province of British Columbia
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
    'development': 'nr_day_job.config.DevConfig',
    'testing': 'nr_day_job.config.TestConfig',
    'production': 'nr_day_job.config.ProdConfig',
    'default': 'nr_day_job.config.ProdConfig'
}


def get_named_config(config_name: str = 'production'):
    """Return the configuration object based on the name.

    :raise: KeyError: if an unknown configuration is requested
    """
    if config_name in ['production', 'staging', 'default']:
        config = ProdConfig()
    elif config_name == 'testing':
        config = TestConfig()
    elif config_name == 'development':
        config = DevConfig()
    else:
        raise KeyError(f'Unknown configuration: {config_name}')
    return config


class Config():  # pylint: disable=too-few-public-methods
    """Base class configuration that should set reasonable defaults.

    Used as the base for all the other configurations.
    """

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'postgres')
    DB_NAME = os.getenv('DATABASE_NAME', 'unittesting')
    DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DB_PORT = os.getenv('DATABASE_PORT', '5432')

    DB_SCHEMA = os.getenv('DATABASE_SCHEMA', 'public')
    DB_IP_TYPE = os.getenv('DATABASE_IP_TYPE', 'private')
    DB_OWNER = os.getenv('DATABASE_OWNER', 'postgres')

    if DB_INSTANCE_CONNECTION_NAME := os.getenv('DATABASE_INSTANCE_CONNECTION_NAME', None):
        SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://'
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    EMAILER_TOPIC = os.getenv('NAMEX_MAILER_TOPIC', '')
    NAMEX_NR_STATE_TOPIC = os.getenv('NAMEX_NR_STATE_TOPIC', '')

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
    SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}'

class ProdConfig(Config):  # pylint: disable=too-few-public-methods
    """Production environment configuration."""

    TESTING = False
    DEBUG = False
