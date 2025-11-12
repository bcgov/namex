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

    DB_SCHEMA = os.getenv('DATABASE_SCHEMA', 'public')
    DB_IP_TYPE = os.getenv('DATABASE_IP_TYPE', 'private')


    if DB_INSTANCE_CONNECTION_NAME := os.getenv('DATABASE_INSTANCE_CONNECTION_NAME', None):
        SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://'
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'


    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_ECHO = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True

