import os
from dotenv import load_dotenv, find_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class Config(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # fdw-registry
    DB1_USER = os.getenv('DATABASE_USERNAME', '')
    DB1_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DB1_NAME = os.getenv('DATABASE_NAME', '')
    DB1_HOST = os.getenv('DATABASE_HOST', '')
    DB1_PORT = os.getenv('DATABASE_PORT', '5432')

    # fdw-names
    DB2_USER = os.getenv('NAMES_DATABASE_USERNAME', '')
    DB2_PASSWORD = os.getenv('NAMES_DATABASE_PASSWORD', '')
    DB2_NAME = os.getenv('NAMES_DATABASE_NAME', '')
    DB2_HOST = os.getenv('NAMES_DATABASE_HOST', '')
    DB2_PORT = os.getenv('NAMES_DATABASE_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=DB1_USER,
        password=DB1_PASSWORD,
        host=DB1_HOST,
        port=DB1_PORT,
        name=DB1_NAME,
    )
    SQLALCHEMY_BINDS = {
        'db1': SQLALCHEMY_DATABASE_URI,
        'db2': 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
            user=DB2_USER,
            password=DB2_PASSWORD,
            host=DB2_HOST,
            port=DB2_PORT,
            name=DB2_NAME,
        )
    }

    # JWT_OIDC Settings
    JWT_OIDC_WELL_KNOWN_CONFIG = os.getenv('JWT_OIDC_WELL_KNOWN_CONFIG')
    JWT_OIDC_ALGORITHMS = os.getenv('JWT_OIDC_ALGORITHMS')
    JWT_OIDC_JWKS_URI = os.getenv('JWT_OIDC_JWKS_URI')
    JWT_OIDC_ISSUER = os.getenv('JWT_OIDC_ISSUER')
    JWT_OIDC_AUDIENCE = os.getenv('JWT_OIDC_AUDIENCE')
    JWT_OIDC_CLIENT_SECRET = os.getenv('JWT_OIDC_CLIENT_SECRET')

    TESTING = False
    DEBUG = False


class TestConfig(Config):

    TESTING = True
    DEBUG = True