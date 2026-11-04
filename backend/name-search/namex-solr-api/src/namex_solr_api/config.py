# Copyright © 2025 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
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


class Config:
    """Base class configuration that should set reasonable defaults.

    Used as the base for all the other configurations.
    """

    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SOLR_SVC_NAMEX_LEADER_CORE = os.getenv("SOLR_SVC_NAMEX_LEADER_CORE", "name_request")
    SOLR_SVC_NAMEX_FOLLOWER_CORE = os.getenv("SOLR_SVC_NAMEX_FOLLOWER_CORE", "name_request_follower")
    SOLR_SVC_NAMEX_LEADER_URL = os.getenv("SOLR_SVC_NAMEX_LEADER_URL", "http://localhost:8863/solr")
    SOLR_SVC_NAMEX_FOLLOWER_URL = os.getenv("SOLR_SVC_NAMEX_FOLLOWER_URL", "http://localhost:8863/solr")
    # TODO: return a 400 if a call exceeds this
    # Non-strict possible-conflicts cap. Keep in sync with MAX_HIGHLIGHTED_DOCS
    # so the extra rows can still be classified into Examiner buckets.
    SOLR_SVC_NAMEX_MAX_ROWS = int(os.getenv("SOLR_SVC_NAMEX_MAX_ROWS", "200"))
    SOLR_SVC_NAMEX_TIMEOUT = int(os.getenv("SOLR_SVC_NAMEX_TIMEOUT", "60"))
    SOLR_SVC_NAMEX_MAX_HIGHLIGHTED_DOCS = int(os.getenv("SOLR_SVC_NAMEX_MAX_HIGHLIGHTED_DOCS", "200"))

    AUTH_SVC_URL = os.getenv("AUTH_API_URL", "") + os.getenv("AUTH_API_VERSION", "")

    # Used by /sync endpoint
    MAX_BATCH_UPDATE_NUM = int(os.getenv("MAX_BATCH_UPDATE_NUM", "500"))
    # Used by /sync heartbeat
    LAST_REPLICATION_THRESHOLD = int(os.getenv("LAST_REPLICATION_THRESHOLD", "24"))  # hours
    
    # Conflict match-prep skip tokens (NameX words_to_filter_from_name) plus the
    # previous Solr legal-designation fallback used by /nrs trailing strip.
    # Spaced entries are phrases (trailing strip only; token skip ignores them).
    # Deployed Cloud Run injects DESIGNATIONS from 1Password via vaults.gcp.env
    # (op://solr/$APP_ENV/namex-search/DESIGNATIONS). Env is space-separated
    # tokens; this Python list is unioned in so skip words and phrases remain
    # even if 1Password only has legal suffixes.
    # Ranking/boosts use the raw query and do not apply this list.
    DEFAULT_DESIGNATIONS = [  # noqa: RUF012
        "association",
        "assoc",
        "assoc.",
        "assn",
        "assn.",
        "company",
        "co",
        "co.",
        "corporation",
        "corp",
        "corp.",
        "incorporated",
        "inc",
        "inc.",
        "incorporee",
        "liability",
        "limited",
        "ltd",
        "ltd.",
        "limitee",
        "ltee",
        "ltee.",
        "society",
        "soc",
        "soc.",
        "ulc",
        "ulc.",
        "unlimited",
        # Previous Solr DESIGNATIONS fallback (unique items).
        "l.l.c.",
        "limited liability co.",
        "limited liability company",
        "limited liability partnership",
        "llc",
        "llp",
        "sencrl",
        "societe a responsabilite limitee",
        "societe en nom collectif a responsabilite limitee",
        "srl",
        "unlimited liability company",
    ]
    # Env is space-separated so it cannot preserve phrases.
    # FUTURE: Make it a comma separated list from the env
    _designations_env = os.getenv("DESIGNATIONS", "")
    DESIGNATIONS = _designations_env.split() if _designations_env else DEFAULT_DESIGNATIONS

    # Cache stuff
    CACHE_TYPE = os.getenv("CACHE_TYPE", "FileSystemCache")
    CACHE_DIR = os.getenv("CACHE_DIR", "cache")
    try:
        CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "300"))
    except (TypeError, ValueError):
        CACHE_DEFAULT_TIMEOUT = 300

    # DB stuff
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALEMBIC_INI = "migrations/alembic.ini"

    DB_USER = os.getenv("DATABASE_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_NAME", "")
    DB_HOST = os.getenv("DATABASE_HOST", "")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")
    CLOUDSQL_INSTANCE_CONNECTION_NAME = os.getenv("DATABASE_INSTANCE_CONNECTION_NAME", "")
    DB_IP_TYPE = os.getenv("DATABASE_IP_TYPE", "private").lower()
    DB_MIN_POOL_SIZE = os.getenv("DATABASE_MIN_POOL_SIZE", "2")
    DB_MAX_POOL_SIZE = os.getenv("DATABASE_MAX_POOL_SIZE", "10")
    DB_CONN_WAIT_TIMEOUT = os.getenv("DATABASE_CONN_WAIT_TIMEOUT", "5")
    DB_CONN_TIMEOUT = os.getenv("DATABASE_CONN_TIMEOUT", "900")

    if CLOUDSQL_INSTANCE_CONNECTION_NAME:
        SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"
    elif DB_UNIX_SOCKET := os.getenv("DATABASE_UNIX_SOCKET", None):
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host={DB_UNIX_SOCKET}"
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_ENGINE_OPTIONS = {  # noqa: RUF012
        "pool_pre_ping": True,
        "pool_size": int(DB_MIN_POOL_SIZE),
        "max_overflow": int(DB_MAX_POOL_SIZE) - int(DB_MIN_POOL_SIZE),
        "pool_recycle": int(DB_CONN_TIMEOUT),
        "pool_timeout": int(DB_CONN_WAIT_TIMEOUT),
    }

    # JWT_OIDC Settings
    JWT_OIDC_WELL_KNOWN_CONFIG = os.getenv("JWT_OIDC_WELL_KNOWN_CONFIG")
    JWT_OIDC_ALGORITHMS = os.getenv("JWT_OIDC_ALGORITHMS")
    JWT_OIDC_JWKS_URI = os.getenv("JWT_OIDC_JWKS_URI")
    JWT_OIDC_ISSUER = os.getenv("JWT_OIDC_ISSUER")
    JWT_OIDC_AUDIENCE = os.getenv("JWT_OIDC_AUDIENCE")
    JWT_OIDC_CLIENT_SECRET = os.getenv("JWT_OIDC_CLIENT_SECRET")
    JWT_OIDC_CACHING_ENABLED = os.getenv("JWT_OIDC_CACHING_ENABLED")
    JWT_OIDC_TOKEN_URL = os.getenv("JWT_OIDC_TOKEN_URL")
    try:
        JWT_OIDC_JWKS_CACHE_TIMEOUT = int(os.getenv("JWT_OIDC_JWKS_CACHE_TIMEOUT"))
        if not JWT_OIDC_JWKS_CACHE_TIMEOUT:
            JWT_OIDC_JWKS_CACHE_TIMEOUT = 300
    except (TypeError, ValueError):
        JWT_OIDC_JWKS_CACHE_TIMEOUT = 300

    JWT_OIDC_UNIQUE_USER_KEY = os.getenv("JWT_OIDC_UNIQUE_USER_KEY", "idp_userid")
    JWT_OIDC_USERNAME = os.getenv("JWT_OIDC_USERNAME", "username")
    JWT_OIDC_FIRSTNAME = os.getenv("JWT_OIDC_FIRSTNAME", "firstname")
    JWT_OIDC_LASTNAME = os.getenv("JWT_OIDC_LASTNAME", "lastname")
    JWT_OIDC_LOGIN_SOURCE = os.getenv("JWT_OIDC_LOGIN_SOURCE", "loginSource")


class DevelopmentConfig(Config):
    """Config object for development environment."""

    DEBUG = True
    DEVELOPMENT = True
    TESTING = False


class UnitTestingConfig(Config):
    """Config object for unit testing environment."""

    DEBUG = True
    DEVELOPMENT = False
    TESTING = True
    POD_NAMESPACE = "unittest"
    # API urls
    AUTH_SVC_URL = os.getenv("AUTH_API_TEST_URL", "http://auth-api.mock") + os.getenv("AUTH_API_VERSION", "")
    # SOLR
    SOLR_SVC_LEADER_CORE = os.getenv("SOLR_SVC_LEADER_TEST_CORE", "bor")
    SOLR_SVC_FOLLOWER_CORE = os.getenv("SOLR_SVC_FOLLOWER_TEST_CORE", "bor")
    SOLR_SVC_LEADER_URL = os.getenv("SOLR_SVC_LEADER_TEST_URL", "http://localhost:8990/solr")
    SOLR_SVC_FOLLOWER_URL = os.getenv("SOLR_SVC_FOLLOWER_TEST_URL", "http://localhost:8990/solr")
    TEMP_SOLR_SVC_TEST_URL = os.getenv("TEMP_SOLR_SVC_TEST_URL", "http://localhost:8991/solr")
    # POSTGRESQL
    DB_USER = os.getenv("DATABASE_TEST_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_TEST_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_TEST_NAME", "")
    DB_HOST = os.getenv("DATABASE_TEST_HOST", "")
    DB_PORT = os.getenv("DATABASE_TEST_PORT", "5432")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}"

    # JWT OIDC settings
    # JWT_OIDC_TEST_MODE will set jwt_manager to use
    JWT_OIDC_TEST_MODE = True
    JWT_OIDC_TEST_AUDIENCE = "example"
    JWT_OIDC_TEST_ISSUER = "https://example.localdomain/auth/realms/example"
    JWT_OIDC_TEST_KEYS = {  # noqa: RUF012
        "keys": [
            {
                "kid": "flask-jwt-oidc-test-client",
                "kty": "RSA",
                "alg": "RS256",
                "use": "sig",
                "n": "AN-fWcpCyE5KPzHDjigLaSUVZI0uYrcGcc40InVtl-rQRDmAh-C2W8H4_Hxhr5VLc6crsJ2LiJTV_E72S03pzpOOaaYV6-TzAjCou2GYJIXev7f6Hh512PuG5wyxda_TlBSsI-gvphRTPsKCnPutrbiukCYrnPuWxX5_cES9eStR",
                "e": "AQAB",
            }
        ]
    }

    JWT_OIDC_TEST_PRIVATE_KEY_JWKS = {  # noqa: RUF012
        "keys": [
            {
                "kid": "flask-jwt-oidc-test-client",
                "kty": "RSA",
                "alg": "RS256",
                "use": "sig",
                "n": "AN-fWcpCyE5KPzHDjigLaSUVZI0uYrcGcc40InVtl-rQRDmAh-C2W8H4_Hxhr5VLc6crsJ2LiJTV_E72S03pzpOOaaYV6-TzAjCou2GYJIXev7f6Hh512PuG5wyxda_TlBSsI-gvphRTPsKCnPutrbiukCYrnPuWxX5_cES9eStR",
                "e": "AQAB",
                "d": "C0G3QGI6OQ6tvbCNYGCqq043YI_8MiBl7C5dqbGZmx1ewdJBhMNJPStuckhskURaDwk4-8VBW9SlvcfSJJrnZhgFMjOYSSsBtPGBIMIdM5eSKbenCCjO8Tg0BUh_xa3CHST1W4RQ5rFXadZ9AeNtaGcWj2acmXNO3DVETXAX3x0",
                "p": "APXcusFMQNHjh6KVD_hOUIw87lvK13WkDEeeuqAydai9Ig9JKEAAfV94W6Aftka7tGgE7ulg1vo3eJoLWJ1zvKM",
                "q": "AOjX3OnPJnk0ZFUQBwhduCweRi37I6DAdLTnhDvcPTrrNWuKPg9uGwHjzFCJgKd8KBaDQ0X1rZTZLTqi3peT43s",
                "dp": "AN9kBoA5o6_Rl9zeqdsIdWFmv4DB5lEqlEnC7HlAP-3oo3jWFO9KQqArQL1V8w2D4aCd0uJULiC9pCP7aTHvBhc",
                "dq": "ANtbSY6njfpPploQsF9sU26U0s7MsuLljM1E8uml8bVJE1mNsiu9MgpUvg39jEu9BtM2tDD7Y51AAIEmIQex1nM",
                "qi": "XLE5O360x-MhsdFXx8Vwz4304-MJg-oGSJXCK_ZWYOB_FGXFRTfebxCsSYi0YwJo-oNu96bvZCuMplzRI1liZw",
            }
        ]
    }

    JWT_OIDC_TEST_PRIVATE_KEY_PEM = """
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDfn1nKQshOSj8xw44oC2klFWSNLmK3BnHONCJ1bZfq0EQ5gIfg
tlvB+Px8Ya+VS3OnK7Cdi4iU1fxO9ktN6c6TjmmmFevk8wIwqLthmCSF3r+3+h4e
ddj7hucMsXWv05QUrCPoL6YUUz7Cgpz7ra24rpAmK5z7lsV+f3BEvXkrUQIDAQAB
AoGAC0G3QGI6OQ6tvbCNYGCqq043YI/8MiBl7C5dqbGZmx1ewdJBhMNJPStuckhs
kURaDwk4+8VBW9SlvcfSJJrnZhgFMjOYSSsBtPGBIMIdM5eSKbenCCjO8Tg0BUh/
xa3CHST1W4RQ5rFXadZ9AeNtaGcWj2acmXNO3DVETXAX3x0CQQD13LrBTEDR44ei
lQ/4TlCMPO5bytd1pAxHnrqgMnWovSIPSShAAH1feFugH7ZGu7RoBO7pYNb6N3ia
C1idc7yjAkEA6Nfc6c8meTRkVRAHCF24LB5GLfsjoMB0tOeEO9w9Ous1a4o+D24b
AePMUImAp3woFoNDRfWtlNktOqLel5PjewJBAN9kBoA5o6/Rl9zeqdsIdWFmv4DB
5lEqlEnC7HlAP+3oo3jWFO9KQqArQL1V8w2D4aCd0uJULiC9pCP7aTHvBhcCQQDb
W0mOp436T6ZaELBfbFNulNLOzLLi5YzNRPLppfG1SRNZjbIrvTIKVL4N/YxLvQbT
NrQw+2OdQACBJiEHsdZzAkBcsTk7frTH4yGx0VfHxXDPjfTj4wmD6gZIlcIr9lZg
4H8UZcVFN95vEKxJiLRjAmj6g273pu9kK4ymXNEjWWJn
-----END RSA PRIVATE KEY-----"""


class ProductionConfig(Config):
    """Config object for production environment."""

    DEBUG = False
    DEVELOPMENT = False
    TESTING = False


class MigrationConfig:
    """Config object for migration environment."""

    ALEMBIC_INI = "migrations/alembic.ini"

    DB_USER = os.getenv("DATABASE_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_NAME", "")
    DB_HOST = os.getenv("DATABASE_HOST", "")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")
    CLOUDSQL_INSTANCE_CONNECTION_NAME = os.getenv("DATABASE_INSTANCE_CONNECTION_NAME", "")
    DB_IP_TYPE = os.getenv("DATABASE_IP_TYPE", "public").lower()
    DB_MIN_POOL_SIZE = os.getenv("DATABASE_MIN_POOL_SIZE", "2")
    DB_MAX_POOL_SIZE = os.getenv("DATABASE_MAX_POOL_SIZE", "10")
    DB_CONN_WAIT_TIMEOUT = os.getenv("DATABASE_CONN_WAIT_TIMEOUT", "5")
    DB_CONN_TIMEOUT = os.getenv("DATABASE_CONN_TIMEOUT", "900")

    if CLOUDSQL_INSTANCE_CONNECTION_NAME:
        SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"
    elif DB_UNIX_SOCKET := os.getenv("DATABASE_UNIX_SOCKET", None):
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host={DB_UNIX_SOCKET}"
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
