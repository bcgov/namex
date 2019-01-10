import os
from dotenv import load_dotenv, find_dotenv

#this will load all the envars from a .env file
load_dotenv(find_dotenv())


class BaseConfig(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    MAX_ROW_LIMIT = os.getenv('MAX_ROWS','100')
    MIN_DELAY_SECONDS = os.getenv('MIN_DELAY_SECONDS', '600')
    SECRET_KEY = 'a secret'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    NRO_SERVICE_ACCOUNT = os.getenv('NRO_SERVICE_ACCOUNT', 'nro_service_account')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_MAX_OVERFLOW = 10

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


class Config(BaseConfig):
    DEBUG = False
    TESTING = False


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    # POSTGRESQL
    DB_USER = os.getenv('DATABASE_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD','')
    DB_NAME = os.getenv('DATABASE_NAME_TEST', '')
    DB_HOST = os.getenv('DATABASE_HOST','')
    DB_PORT = os.getenv('DATABASE_PORT','5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
         user=DB_USER,
         password=DB_PASSWORD,
         host=DB_HOST,
         port=int(DB_PORT),
         name=DB_NAME,
    )
