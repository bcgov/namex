
import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv(), override=True)

CONFIGURATION = {
    'development': 'config.DevConfig',
    'testing': 'config.TestConfig',
    'production': 'config.Config',
    'default': 'config.Config'
}


class Config(object):
    SECRET_KEY = 'My Secret'

    # Normal Keycloak parameters.
    OIDC_CLIENT_SECRETS = os.getenv('SOLR_ADMIN_APP_OIDC_CLIENT_SECRETS', 'solr-admin-app/keycloak_client_secrets/secrets.json')
    OIDC_SCOPES = ['openid', 'email', 'profile']
    OIDC_VALID_ISSUERS = [os.getenv('SOLR_ADMIN_APP_OIDC_VALID_ISSUERS', 'http://localhost:8081/auth/realms/master')]
    OVERWRITE_REDIRECT_URI = os.getenv('SOLR_ADMIN_APP_OVERWRITE_REDIRECT_URI', '')

    print("OIDC" + OIDC_CLIENT_SECRETS)
    # Undocumented Keycloak parameter: allows sending cookies without the secure flag, which we need for the local
    # non-TLS HTTP server. Set this to non-"True" for local development, and use the default everywhere else.
    OIDC_ID_TOKEN_COOKIE_SECURE = os.getenv('SOLR_ADMIN_APP_OIDC_ID_TOKEN_COOKIE_SECURE', 'True') == 'True'

    # Turn this off to get rid of warning messages. In future versions of SQLAlchemy, False will be the default and
    # this can be removed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # PostgreSQL Connection information.
    DATABASE_USER = os.getenv('NAMES_ADMIN_DATABASE_USERNAME', '')
    DATABASE_PASSWORD = os.getenv('NAMES_ADMIN_DATABASE_PASSWORD', '')
    DATABASE_HOST = os.getenv('NAMES_ADMIN_DATABASE_HOST', '')
    DATABASE_PORT = os.getenv('NAMES_ADMIN_DATABASE_PORT', '5432')
    DATABASE_NAME = os.getenv('NAMES_ADMIN_DATABASE_NAME', '')

    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=int(DATABASE_PORT),
        name=DATABASE_NAME)

    SYNONYMS_DATABASE_USER = os.getenv('NAMES_ADMIN_SYNONYMS_DATABASE_USERNAME', '')
    SYNONYMS_DATABASE_PASSWORD = os.getenv('NAMES_ADMIN_SYNONYMS_DATABASE_PASSWORD', '')
    SYNONYMS_DATABASE_HOST = os.getenv('NAMES_ADMIN_SYNONYMS_DATABASE_HOST', '')
    SYNONYMS_DATABASE_PORT = os.getenv('NAMES_ADMIN_SYNONYMS_DATABASE_PORT', '5432')
    SYNONYMS_DATABASE_NAME = os.getenv('NAMES_ADMIN_SYNONYMS_DATABASE_NAME', 'synonyms')
    SQLALCHEMY_BINDS = {
        'synonyms': 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
            user=SYNONYMS_DATABASE_USER,
            password=SYNONYMS_DATABASE_PASSWORD,
            host=SYNONYMS_DATABASE_HOST,
            port=int(SYNONYMS_DATABASE_PORT),
            name=SYNONYMS_DATABASE_NAME)
    }

    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_ECHO = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True


