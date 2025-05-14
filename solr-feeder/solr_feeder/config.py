
# Copyright © 2023 Province of British Columbia
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


class Config():  # pylint: disable=too-few-public-methods;
    """Base class configuration that should set reasonable defaults.

    Used as the base for all the other configurations.
    """

    SECRET_KEY = 'a secret'

    POD_NAMESPACE = os.getenv('POD_NAMESPACE', 'unknown')

    COLIN_API_URL = os.getenv('COLIN_API_URL', 'http://') + \
        os.getenv('COLIN_API_VERSION', '/api/v1')

    SEARCH_API_URL = os.getenv('REGISTRIES_SEARCH_API_INTERNAL_URL', 'http://') \
        + os.getenv('REGISTRIES_SEARCH_API_VERSION', '/api/v1')

    BOR_API_URL = os.getenv('BOR_API_INTERNAL_URL', '') \
        + os.getenv('BOR_API_VERSION', '')

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
    try:
        BOR_API_TIMEOUT = int(os.getenv('SOLR_FEEDER_BOR_API_TIMEOUT', '30'))
    except:  # pylint: disable=bare-except; # noqa: B901, E722
        BOR_API_TIMEOUT = 30

    try:
        NAMEX_SOLR_TIMEOUT = int(os.getenv('NAMEX_SOLR_TIMEOUT', '20'))
    except:  # pylint: disable=bare-except; # noqa: B901, E722
        NAMEX_SOLR_TIMEOUT = 20

    KEYCLOAK_AUTH_TOKEN_URL = os.getenv('KEYCLOAK_AUTH_TOKEN_URL')
    KEYCLOAK_SERVICE_ACCOUNT_ID = os.getenv('NDS_SERVICE_ACCOUNT_CLIENT_ID')
    KEYCLOAK_SERVICE_ACCOUNT_SECRET = os.getenv('NDS_SERVICE_ACCOUNT_SECRET')

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods;
    """Development config."""

    DEBUG = True
    TESTING = True


class UnitTestingConfig(Config):  # pylint: disable=too-few-public-methods;
    """Testing config."""

    DEBUG = True
    TESTING = True


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods;
    """Production config."""

    SECRET_KEY = os.getenv('SOLR_FEEDER_FLASK_SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError('Environment variable SOLR_FEEDER_FLASK_SECRET_KEY in not defined')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'unitTesting': UnitTestingConfig,
}
