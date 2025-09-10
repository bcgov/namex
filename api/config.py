"""Config for initializing the namex-api."""

import os
import textwrap

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())

CONFIGURATION = {
    'development': 'config.DevConfig',
    'testing': 'config.TestConfig',
    'production': 'config.Config',
    'migration': 'config.MigrationConfig',
    'default': 'config.Config',
}


class Config(object):
    """Base config (also production config)."""

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    TESTING = (False,)
    DEBUG = False

    ALEMBIC_INI = 'migrations/alembic.ini'

    SECRET_KEY = 'a secret'  # noqa: S105

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SOLR_BASE_URL = os.getenv('SOLR_BASE_URL', None)

    SOLR_SYNONYMS_API_URL = f'{os.getenv("SOLR_SYNONYMS_API_URL", None)}{os.getenv("SOLR_SYNONYMS_API_VERSION", None)}'

    AUTO_ANALYZE_URL = os.getenv('AUTO_ANALYZE_URL', None)
    AUTO_ANALYZE_CONFIG = os.getenv('AUTO_ANALYZE_CONFIG', None)

    REPORT_SVC_URL = f'{os.getenv("REPORT_API_URL", None)}{os.getenv("REPORT_API_VERSION", None)}/reports'
    REPORT_TEMPLATE_PATH = os.getenv('REPORT_PATH', 'report-templates')

    PAYMENT_SVC_URL = os.getenv('PAY_API_URL', None)
    PAYMENT_SVC_VERSION = os.getenv('PAY_API_VERSION', None)

    AUTH_SVC_URL = f'{os.getenv("AUTH_API_URL", None)}{os.getenv("AUTH_API_VERSION", "/api/v1")}'

    COLIN_SVC_URL = f'{os.getenv("COLIN_SVC_URL", None)}{os.getenv("COLIN_SVC_VERSION", None)}'

    ENTITY_SVC_URL = f'{os.getenv("LEGAL_API_URL", None)}{os.getenv("LEGAL_API_VERSION", "/api/v2")}'

    NAME_REQUEST_URL = os.getenv('NAME_REQUEST_URL', '')
    NAMES_INFORMATION_URL = os.getenv(
        'NAMES_INFORMATION_URL',
        'https://www2.gov.bc.ca/gov/content/employment-business/business/managing-a-business/\
permits-licences/businesses-incorporated-companies/approval-business-name',
    )

    DECIDE_BUSINESS_URL = os.getenv('DECIDE_BUSINESS_URL', '')
    BUSINESS_CHANGES_URL = os.getenv('BUSINESS_CHANGES_URL', '')
    CORP_FORMS_URL = os.getenv('CORP_FORMS_URL', '')
    BUSINESS_URL = os.getenv('BUSINESS_URL', '')
    COLIN_URL = os.getenv('COLIN_URL', '')
    SOCIETIES_URL = os.getenv('SOCIETIES_URL', '')

    NAMEX_LD_SDK_ID = os.getenv('NAMEX_LD_SDK_ID', '')

    # POSTGRESQL
    DB_USER = os.getenv("DATABASE_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_NAME", "")
    DB_HOST = os.getenv("DATABASE_HOST", "")
    DB_PORT = int(os.getenv("DATABASE_PORT", "5432"))

    DB_SCHEMA = os.getenv("DATABASE_SCHEMA", "public")
    DB_IP_TYPE = os.getenv("DATABASE_IP_TYPE", "private")
    DB_OWNER = os.getenv("DATABASE_OWNER", "postgres")

    if DB_INSTANCE_CONNECTION_NAME := os.getenv("DATABASE_INSTANCE_CONNECTION_NAME", None):
        SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # KEYCLOAK & JWT_OIDC Settings
    JWT_OIDC_WELL_KNOWN_CONFIG = os.getenv('JWT_OIDC_WELL_KNOWN_CONFIG')
    JWT_OIDC_ALGORITHMS = os.getenv('JWT_OIDC_ALGORITHMS')
    JWT_OIDC_JWKS_URI = os.getenv('JWT_OIDC_JWKS_URI')
    JWT_OIDC_ISSUER = os.getenv('JWT_OIDC_ISSUER')
    JWT_OIDC_CACHING_ENABLED = os.getenv('JWT_OIDC_CACHING_ENABLED')
    JWT_OIDC_JWKS_CACHE_TIMEOUT = int(os.getenv('JWT_OIDC_JWKS_CACHE_TIMEOUT', '300'))

    JWT_OIDC_AUDIENCE = os.getenv('JWT_OIDC_AUDIENCE')

    ENTITY_SVC_AUTH_URL = os.getenv('KEYCLOAK_AUTH_TOKEN_URL', '')
    ENTITY_SERVICE_ACCOUNT_CLIENT_ID = os.getenv('ENTITY_SERVICE_ACCOUNT_CLIENT_ID', '')
    ENTITY_SERVICE_ACCOUNT_CLIENT_SECRET = os.getenv('ENTITY_SERVICE_ACCOUNT_CLIENT_SECRET', '')

    PAYMENT_SVC_AUTH_URL = os.getenv('KEYCLOAK_AUTH_TOKEN_URL', '')
    PAYMENT_SVC_AUTH_CLIENT_ID = os.getenv('NAME_REQUEST_SERVICE_ACCOUNT_CLIENT_ID', '')
    PAYMENT_SVC_CLIENT_SECRET = os.getenv('NAME_REQUEST_SERVICE_ACCOUNT_CLIENT_SECRET', '')

    DISABLE_NAMEREQUEST_SOLR_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_SOLR_UPDATES', 0))

    GCP_AUTH_KEY = os.getenv('BUSINESS_GCP_AUTH_KEY', None)
    NAMEX_NR_STATE_TOPIC = os.getenv('NAMEX_NR_STATE_TOPIC', '')
    EMAILER_TOPIC = os.getenv('NAMEX_MAILER_TOPIC', '')

    AUDIENCE = os.getenv('AUDIENCE', 'https://pubsub.googleapis.com/google.pubsub.v1.Subscriber')
    PUBLISHER_AUDIENCE = os.getenv('PUBLISHER_AUDIENCE', 'https://pubsub.googleapis.com/google.pubsub.v1.Publisher')

    # MRAS
    MRAS_SVC_URL = os.getenv('MRAS_SVC_URL', '')
    MRAS_SVC_API_KEY = os.getenv('MRAS_SVC_API_KEY', '')

    # Generate new NR Number
    NR_NUM_LIFESPAN = int(os.getenv('NR_NUM_LIFESPAN', 60))


class DevConfig(Config):
    """Dev config used for development."""

    TESTING = (False,)
    DEBUG = True

    DISABLE_NAMEREQUEST_SOLR_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_SOLR_UPDATES', 0))


class MigrationConfig(Config):  # pylint: disable=too-few-public-methods
    """Config for db migration."""

    TESTING = (False,)
    DEBUG = True

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

    LOCAL_DEV_MODE = os.getenv('LOCAL_DEV_MODE', False)
    # Set this in your .env to debug SQL Alchemy queries (for local development)
    SQLALCHEMY_ECHO = 'debug' if os.getenv('DEBUG_SQL_QUERIES', False) else False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=int(DB_PORT), name=DB_NAME
    )
    EMAILER_TOPIC = os.getenv('NAMEX_MAILER_TOPIC', '')

    DISABLE_NAMEREQUEST_SOLR_UPDATES = int(os.getenv('DISABLE_NAMEREQUEST_SOLR_UPDATES', 0))

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
                'n': 'AN-fWcpCyE5KPzHDjigLaSUVZI0uYrcGcc40InVtl-rQRDmAh-C2W8H4_Hxhr5VLc6crsJ2LiJTV_E72S03pzpOOaaYV6-TzAjCou2GYJIXev7f6Hh512PuG5wyxda_TlBSsI-gvphRTPsKCnPutrbiukCYrnPuWxX5_cES9eStR',
                'e': 'AQAB',
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
                'n': 'AN-fWcpCyE5KPzHDjigLaSUVZI0uYrcGcc40InVtl-rQRDmAh-C2W8H4_Hxhr5VLc6crsJ2LiJTV_E72S03pzpOOaaYV6-TzAjCou2GYJIXev7f6Hh512PuG5wyxda_TlBSsI-gvphRTPsKCnPutrbiukCYrnPuWxX5_cES9eStR',
                'e': 'AQAB',
                'd': 'C0G3QGI6OQ6tvbCNYGCqq043YI_8MiBl7C5dqbGZmx1ewdJBhMNJPStuckhskURaDwk4-8VBW9SlvcfSJJrnZhgFMjOYSSsBtPGBIMIdM5eSKbenCCjO8Tg0BUh_xa3CHST1W4RQ5rFXadZ9AeNtaGcWj2acmXNO3DVETXAX3x0',
                'p': 'APXcusFMQNHjh6KVD_hOUIw87lvK13WkDEeeuqAydai9Ig9JKEAAfV94W6Aftka7tGgE7ulg1vo3eJoLWJ1zvKM',
                'q': 'AOjX3OnPJnk0ZFUQBwhduCweRi37I6DAdLTnhDvcPTrrNWuKPg9uGwHjzFCJgKd8KBaDQ0X1rZTZLTqi3peT43s',
                'dp': 'AN9kBoA5o6_Rl9zeqdsIdWFmv4DB5lEqlEnC7HlAP-3oo3jWFO9KQqArQL1V8w2D4aCd0uJULiC9pCP7aTHvBhc',
                'dq': 'ANtbSY6njfpPploQsF9sU26U0s7MsuLljM1E8uml8bVJE1mNsiu9MgpUvg39jEu9BtM2tDD7Y51AAIEmIQex1nM',
                'qi': 'XLE5O360x-MhsdFXx8Vwz4304-MJg-oGSJXCK_ZWYOB_FGXFRTfebxCsSYi0YwJo-oNu96bvZCuMplzRI1liZw',
            }
        ]
    }

    JWT_OIDC_TEST_PRIVATE_KEY_PEM = textwrap.dedent("""
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
    -----END RSA PRIVATE KEY-----""")
