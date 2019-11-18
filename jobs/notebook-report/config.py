import os
from dotenv import load_dotenv, find_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class Config(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PG_USER = os.getenv('PG_USER', '')
    PG_PASSWORD = os.getenv('PG_PASSWORD','')
    PG_NAME = os.getenv('PG_DB_NAME','')
    PG_HOST = os.getenv('PG_HOST','')
    PG_PORT = os.getenv('PG_PORT','5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
         user=PG_USER,
         password=PG_PASSWORD,
         host=PG_HOST,
         port=int(PG_PORT),
         name=PG_NAME,
    )
