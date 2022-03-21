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
import random

from dotenv import find_dotenv, load_dotenv


# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())

CONFIGURATION = {
    'development': 'namex_pay.config.DevConfig',
    'testing': 'namex_pay.config.TestConfig',
    'production': 'namex_pay.config.ProdConfig',
    'default': 'namex_pay.config.ProdConfig'
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


class _Config():  # pylint: disable=too-few-public-methods
    """Base class configuration that should set reasonable defaults.

    Used as the base for all the other configurations.
    """

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    PAYMENT_SVC_URL = os.getenv('PAYMENT_SVC_URL', '')

    SENTRY_DSN = os.getenv('SENTRY_DSN', None)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DB_NAME = os.getenv('DATABASE_NAME', '')
    DB_HOST = os.getenv('DATABASE_HOST', '')
    DB_PORT = os.getenv('DATABASE_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}'

    # ORACLE - LEGACY NRO NAMESDB
    NRO_USER = os.getenv('NRO_USER', '')
    NRO_SCHEMA = os.getenv('NRO_SCHEMA', None)
    NRO_PASSWORD = os.getenv('NRO_PASSWORD', '')
    NRO_DB_NAME = os.getenv('NRO_DB_NAME', '')
    NRO_HOST = os.getenv('NRO_HOST', '')
    NRO_PORT = int(os.getenv('NRO_PORT', '1521'))

    NATS_SERVERS = os.getenv('NATS_SERVERS', 'nats://localhost:4222')
    NATS_CLIENT_NAME = os.getenv('NATS_CLIENT_NAME', 'namex.worker')
    NATS_CLUSTER_ID = os.getenv('NATS_CLUSTER_ID', 'test-cluster')
    NATS_QUEUE = os.getenv('NATS_QUEUE', 'namerequest-processor')
    NATS_NR_STATE_SUBJECT = os.getenv('NATS_NR_STATE_SUBJECT', 'namex.event')
    NATS_EMAILER_SUBJECT = os.getenv('NATS_EMAILER_SUBJECT', 'entity.email')

    NATS_CONNECTION_OPTIONS = {
        'servers': os.getenv('NATS_SERVERS', 'nats://127.0.0.1:4222').split(','),
        'name': os.getenv('NATS_CLIENT_NAME', 'entity.filing.worker')

    }
    STAN_CONNECTION_OPTIONS = {
        'cluster_id': os.getenv('NATS_CLUSTER_ID', 'test-cluster'),
        'client_id': str(random.SystemRandom().getrandbits(0x58)),
        'ping_interval': 1,
        'ping_max_out': 5,
    }

    SUBSCRIPTION_OPTIONS = {
        'subject': os.getenv('NATS_SUBJECT', 'entity.filings'),
        'queue': os.getenv('NATS_QUEUE', 'filing-worker'),
        'durable_name': os.getenv('NATS_QUEUE', 'filing-worker') + '_durable',
    }

    FILER_PUBLISH_OPTIONS = {
        'subject': os.getenv('NATS_FILER_SUBJECT', 'entity.filing.filer'),
    }

    EMAIL_PUBLISH_OPTIONS = {
        'subject': os.getenv('NATS_EMAILER_SUBJECT', 'entity.email'),
    }

    ENVIRONMENT = os.getenv('ENVIRONMENT', 'prod')


class DevConfig(_Config):  # pylint: disable=too-few-public-methods
    """Creates the Development Config object."""

    TESTING = False
    DEBUG = True


class TestConfig(_Config):  # pylint: disable=too-few-public-methods
    """In support of testing only.

    Used by the py.test suite
    """

    DEBUG = True
    TESTING = True
    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_TEST_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_TEST_PASSWORD', '')
    DB_NAME = os.getenv('DATABASE_TEST_NAME', '')
    DB_HOST = os.getenv('DATABASE_TEST_HOST', '')
    DB_PORT = os.getenv('DATABASE_TEST_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}'


class ProdConfig(_Config):  # pylint: disable=too-few-public-methods
    """Production environment configuration."""

    TESTING = False
    DEBUG = False
