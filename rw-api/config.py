import os
from dotenv import load_dotenv, find_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class Config(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # postgres
    DB_USER = os.getenv('DATABASE_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DB_NAME = os.getenv('DATABASE_NAME', '')
    DB_HOST = os.getenv('DATABASE_HOST', '')
    DB_PORT = os.getenv('DATABASE_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME,
    )

    # oidc -- don't know where this info is going -- what are client secrets?
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    OIDC_OPENID_REALM = os.getenv('OIDC_OPENID_REALM', '')
    OIDC_CLIENT_SECRETS = os.getenv('OIDC_SECRETS_FILE', 'client_secrets/client_secrets.json')
    OIDC_USER_INFO_ENABLED = True
    OIDC_SCOPES = ['openid', 'email', 'profile']
    TESTING = False
    DEBUG = False

class TestConfig(Config):
    OIDC_CLIENT_SECRETS = os.getenv('OIDC_TEST_SECRETS_FILE', 'client_secrets/client_secrets.json')
    TESTING = True
    DEBUG = True