import os
from dotenv import load_dotenv, find_dotenv

#this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())

configuration = {
    "development": "config.DevConfig",
    "testing": "config.TestConfig",
    "production": "config.Config",
    "default": "config.Config"
}


class Config(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SOLR_BASE_URL=os.getenv('SOLR_BASE_URL', None)

    ALEMBIC_INI='migrations/alembic.ini'

    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD','')
    DB_NAME = os.getenv('DATABASE_NAME','')
    DB_HOST = os.getenv('DATABASE_HOST','')
    DB_PORT = os.getenv('DATABASE_PORT','5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
         user=DB_USER,
         password=DB_PASSWORD,
         host=DB_HOST,
         port=int(DB_PORT),
         name=DB_NAME,
    )

    # OIDC
    SECRET_KEY = os.getenv('SECRET_KEY','')
    OIDC_OPENID_REALM = os.getenv('OIDC_OPENID_REALM','')
    OIDC_CLIENT_SECRETS = os.getenv('OIDC_SECRETS_FILE','client_secrets/client_secrets.json')
    OIDC_USER_INFO_ENABLED = True
    OIDC_SCOPES = ['openid', 'email', 'profile']
    TESTING = False,
    DEBUG = False


class DevConfig(Config):
    TESTING = False,
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_TEST_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_TEST_PASSWORD','')
    DB_NAME = os.getenv('DATABASE_TEST_NAME','')
    DB_HOST = os.getenv('DATABASE_TEST_HOST','')
    DB_PORT = os.getenv('DATABASE_TEST_PORT','5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
         user=DB_USER,
         password=DB_PASSWORD,
         host=DB_HOST,
         port=int(DB_PORT),
         name=DB_NAME,
    )
