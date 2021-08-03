"""Config for initializing the namex-api."""
import os
import random

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())

CONFIGURATION = {
    'development': 'config.DevConfig',
    'testing': 'config.TestConfig',
    'production': 'config.Config',
    'default': 'config.Config'
}


class Config(object):
    """Base config (also production config)."""

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = 'a secret'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    NRO_SERVICE_ACCOUNT = os.getenv('NRO_SERVICE_ACCOUNT', 'nro_service_account')

    SOLR_BASE_URL = os.getenv('SOLR_BASE_URL', None)
    SOLR_SYNONYMS_API_URL = os.getenv('SOLR_SYNONYMS_API_URL', None)
    NRO_EXTRACTOR_URI = os.getenv('NRO_EXTRACTOR_URI', None)
    AUTO_ANALYZE_URL = os.getenv('AUTO_ANALYZE_URL', None)
    AUTO_ANALYZE_CONFIG = os.getenv('AUTO_ANALYZE_CONFIG', None)
    REPORT_SVC_URL = os.getenv('REPORT_SVC_URL', None)
    REPORT_TEMPLATE_PATH = os.getenv('REPORT_PATH', 'report-templates')

    ALEMBIC_INI = 'migrations/alembic.ini'

    # POSTGRESQL
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
        name=DB_NAME
    )
    # ORACLE - LEGACY NRO NAMESDB
    NRO_USER = os.getenv('NRO_USER', '')
    NRO_SCHEMA = os.getenv('NRO_SCHEMA', None)
    NRO_PASSWORD = os.getenv('NRO_PASSWORD', '')
    NRO_DB_NAME = os.getenv('NRO_DB_NAME', '')
    NRO_HOST = os.getenv('NRO_HOST', '')
    NRO_PORT = int(os.getenv('NRO_PORT', '1521'))

    # JWT_OIDC Settings
    JWT_OIDC_WELL_KNOWN_CONFIG = os.getenv('JWT_OIDC_WELL_KNOWN_CONFIG')
    JWT_OIDC_ALGORITHMS = os.getenv('JWT_OIDC_ALGORITHMS')
    JWT_OIDC_JWKS_URI = os.getenv('JWT_OIDC_JWKS_URI')
    JWT_OIDC_ISSUER = os.getenv('JWT_OIDC_ISSUER')
    JWT_OIDC_AUDIENCE = os.getenv('JWT_OIDC_AUDIENCE')
    JWT_OIDC_CLIENT_SECRET = os.getenv('JWT_OIDC_CLIENT_SECRET')
    JWT_OIDC_CACHING_ENABLED = os.getenv('JWT_OIDC_CACHING_ENABLED')

    JWT_OIDC_JWKS_CACHE_TIMEOUT = int(os.getenv('JWT_OIDC_JWKS_CACHE_TIMEOUT', '300'))

    TESTING = False,
    DEBUG = False

    # You can disable NRO updates for Name Requests by setting the variable in your .env / OpenShift configuration
    DISABLE_NAMEREQUEST_NRO_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_NRO_UPDATES', 0))
    DISABLE_NAMEREQUEST_SOLR_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_SOLR_UPDATES', 0))
    DISABLE_NAMEREQUEST_NATS_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_NATS_UPDATES', 0))

    # NATS
    NATS_SERVERS = os.getenv('NATS_SERVERS', 'nats://localhost:4222')
    NATS_CLIENT_NAME = os.getenv('NATS_CLIENT_NAME', 'namex.worker')
    NATS_CLUSTER_ID = os.getenv('NATS_CLUSTER_ID', 'test-cluster')
    NATS_QUEUE = os.getenv('NATS_QUEUE', 'namerequest-processor')
    NATS_NR_STATE_SUBJECT = os.getenv('NATS_NR_STATE_SUBJECT', 'namex.event')


class DevConfig(Config):
    """Dev config used for development."""

    TESTING = False,
    DEBUG = True

    # We can't run NRO locally unless you're provisioned, you can disable NRO updates for Name Requests by setting the variable in your .env
    DISABLE_NAMEREQUEST_NRO_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_NRO_UPDATES', 0))
    DISABLE_NAMEREQUEST_SOLR_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_SOLR_UPDATES', 0))
    DISABLE_NAMEREQUEST_NATS_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_NATS_UPDATES', 0))


class TestConfig(Config):
    """Test config used for pytests."""

    DEBUG = True
    TESTING = True
    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_TEST_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_TEST_PASSWORD', '')
    DB_NAME = os.getenv('DATABASE_TEST_NAME', '')
    DB_HOST = os.getenv('DATABASE_TEST_HOST', '')
    DB_PORT = os.getenv('DATABASE_TEST_PORT', '5432')
    # Allows for NRO add / update bypass if necessary (for local development)
    LOCAL_DEV_MODE = os.getenv('LOCAL_DEV_MODE', False)
    # Set this in your .env to debug SQL Alchemy queries (for local development)
    SQLALCHEMY_ECHO = 'debug' if os.getenv('DEBUG_SQL_QUERIES', False) else False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        name=DB_NAME
    )

    # We can't run NRO locally for running our tests
    DISABLE_NAMEREQUEST_NRO_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_NRO_UPDATES', 1))
    DISABLE_NAMEREQUEST_SOLR_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_SOLR_UPDATES', 0))
    DISABLE_NAMEREQUEST_NATS_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_NATS_UPDATES', 1))

    # JWT OIDC settings
    # JWT_OIDC_TEST_MODE will set jwt_manager to use
    JWT_OIDC_TEST_MODE = True
    JWT_OIDC_TEST_AUDIENCE = 'example'
    JWT_OIDC_TEST_ISSUER = 'https://example.localdomain/auth/realms/example'
    JWT_OIDC_TEST_KEYS = {
        'keys': [
            {
                'kid': 'flask-jwt-oidc-test-client',
                'kty': 'RSA',
                'alg': 'RS256',
                'use': 'sig',
                'n': 'AN-fWcpCyE5KPzHDjigLaSUVZI0uYrcGcc40InVtl-rQRDmAh-C2W8H4_Hxhr5VLc6crsJ2LiJTV_E72S03pzpOOaaYV6-TzAjCou2GYJIXev7f6Hh512PuG5wyxda_TlBSsI-gvphRTPsKCnPutrbiukCYrnPuWxX5_cES9eStR',  # noqa: E501
                'e': 'AQAB'
            }
        ]
    }

    JWT_OIDC_TEST_PRIVATE_KEY_JWKS = {
        'keys': [
            {
                'kid': 'flask-jwt-oidc-test-client',
                'kty': 'RSA',
                'alg': 'RS256',
                'use': 'sig',
                'n': 'AN-fWcpCyE5KPzHDjigLaSUVZI0uYrcGcc40InVtl-rQRDmAh-C2W8H4_Hxhr5VLc6crsJ2LiJTV_E72S03pzpOOaaYV6-TzAjCou2GYJIXev7f6Hh512PuG5wyxda_TlBSsI-gvphRTPsKCnPutrbiukCYrnPuWxX5_cES9eStR',  # noqa: E501
                'e': 'AQAB',
                'd': 'C0G3QGI6OQ6tvbCNYGCqq043YI_8MiBl7C5dqbGZmx1ewdJBhMNJPStuckhskURaDwk4-8VBW9SlvcfSJJrnZhgFMjOYSSsBtPGBIMIdM5eSKbenCCjO8Tg0BUh_xa3CHST1W4RQ5rFXadZ9AeNtaGcWj2acmXNO3DVETXAX3x0',  # noqa: E501
                'p': 'APXcusFMQNHjh6KVD_hOUIw87lvK13WkDEeeuqAydai9Ig9JKEAAfV94W6Aftka7tGgE7ulg1vo3eJoLWJ1zvKM',
                'q': 'AOjX3OnPJnk0ZFUQBwhduCweRi37I6DAdLTnhDvcPTrrNWuKPg9uGwHjzFCJgKd8KBaDQ0X1rZTZLTqi3peT43s',
                'dp': 'AN9kBoA5o6_Rl9zeqdsIdWFmv4DB5lEqlEnC7HlAP-3oo3jWFO9KQqArQL1V8w2D4aCd0uJULiC9pCP7aTHvBhc',
                'dq': 'ANtbSY6njfpPploQsF9sU26U0s7MsuLljM1E8uml8bVJE1mNsiu9MgpUvg39jEu9BtM2tDD7Y51AAIEmIQex1nM',
                'qi': 'XLE5O360x-MhsdFXx8Vwz4304-MJg-oGSJXCK_ZWYOB_FGXFRTfebxCsSYi0YwJo-oNu96bvZCuMplzRI1liZw'
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
