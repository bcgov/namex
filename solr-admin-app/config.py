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

    # Keycloak
    KEYCLOAK_AUTH_TOKEN_URL = os.getenv("KEYCLOAK_AUTH_TOKEN_URL")
    JWT_OIDC_WELL_KNOWN_CONFIG = os.getenv("JWT_OIDC_WELL_KNOWN_CONFIG")
    JWT_OIDC_AUDIENCE = os.getenv('JWT_OIDC_AUDIENCE')
    JWT_OIDC_CLIENT_SECRET = os.getenv('JWT_OIDC_CLIENT_SECRET')
    OIDC_REDIRECT_URI = os.getenv('OIDC_REDIRECT_URI')

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


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_ECHO = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True

