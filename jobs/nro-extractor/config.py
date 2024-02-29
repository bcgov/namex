import os
from dotenv import load_dotenv, find_dotenv

#this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())

class BaseConfig(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    MAX_ROW_LIMIT = os.getenv('MAX_ROWS','100')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    NRO_SERVICE_ACCOUNT = os.getenv('NRO_SERVICE_ACCOUNT', 'nro_service_account')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_MAX_OVERFLOW = 10

    # POSTGRESQL
    DB_USER = os.getenv('PG_USER', '')
    DB_PASSWORD = os.getenv('PG_PASSWORD','')
    DB_NAME = os.getenv('PG_NAME','')
    DB_HOST = os.getenv('PG_HOST','')
    DB_PORT = os.getenv('PG_PORT','5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
         user=DB_USER,
         password=DB_PASSWORD,
         host=DB_HOST,
         port=int(DB_PORT),
         name=DB_NAME,
    )

    NRO_USER = os.getenv('NRO_USER', '')
    NRO_SCHEMA = os.getenv('NRO_SCHEMA', None)
    NRO_PASSWORD = os.getenv('NRO_PASSWORD', '')
    NRO_DB_NAME = os.getenv('NRO_DB_NAME', '')
    NRO_HOST = os.getenv('NRO_HOST', '')
    NRO_PORT = int(os.getenv('NRO_PORT', '1521'))

    GCP_AUTH_KEY = os.getenv("GCP_AUTH_KEY", None)
    NAMEX_NR_STATE_TOPIC = os.getenv("NAMEX_NR_STATE_TOPIC", "namex-pay-dev")
    NAMEX_RECEIPT_TOPIC = os.getenv("EMAILER_TOPIC", "namex-receipt-dev")


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
