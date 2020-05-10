import os
from dotenv import load_dotenv, find_dotenv

#this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class Config(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    MAX_ROW_LIMIT = os.getenv('MAX_ROWS', '100')
    MIN_DELAY_SECONDS = os.getenv('MIN_DELAY_SECONDS', '600')

    SOLR_SYNONYMS_API_URL = os.getenv('SOLR_SYNONYMS_API_URL', '')

    SECRET_KEY = 'a secret'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # POSTGRESQL-SOLR
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
