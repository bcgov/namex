import os
import base64
import tempfile
import atexit
import dotenv
import json

dotenv.load_dotenv(dotenv.find_dotenv(), override=True)

CONFIGURATION = {
    'development': 'config.DevConfig',
    'testing': 'config.TestConfig',
    'production': 'config.Config',
    'default': 'config.Config'
}


class Config(object):
    SECRET_KEY = 'My Secret'

    _keycloak_secrets_b64 = os.getenv("SOLR_ADMIN_APP_OIDC_CLIENT_SECRETS")
    try:
        # Write the JSON to a temporary file.
        decoded = base64.b64decode(_keycloak_secrets_b64).decode("utf-8")
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(decoded)
            OIDC_CLIENT_SECRETS = temp_file.name
            _temp_oidc_client_secrets_path = temp_file.name
    except Exception as e:
        raise ValueError("Failed to decode and create temporary Keycloak secrets file.") from e

    OIDC_SCOPES = ['openid', 'email', 'profile']
    OIDC_VALID_ISSUERS = [os.getenv('SOLR_ADMIN_APP_OIDC_VALID_ISSUERS', 'http://localhost:8081/auth/realms/master')]
    OVERWRITE_REDIRECT_URI = os.getenv('SOLR_ADMIN_APP_OVERWRITE_REDIRECT_URI', '')

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

    if DB_UNIX_SOCKET := os.getenv('NAMES_ADMIN_DATABASE_UNIX_SOCKET', None):
        SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@/{DATABASE_NAME}?host={DB_UNIX_SOCKET}'
        SQLALCHEMY_BINDS = {'synonyms': f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@/{DATABASE_NAME}?host={DB_UNIX_SOCKET}'}
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{int(DATABASE_PORT)}/{DATABASE_NAME}'
        SQLALCHEMY_BINDS = {'synonyms': f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{int(DATABASE_PORT)}/{DATABASE_NAME}'}

    DEBUG = False
    TESTING = False

    @staticmethod
    def cleanup_temp_file():
        """Delete the temporary OIDC client secrets file on exit."""
        temp_path = getattr(Config, '_temp_oidc_client_secrets_path', None)
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                pass

# Register the cleanup function with atexit.
atexit.register(Config.cleanup_temp_file)


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_ECHO = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True

