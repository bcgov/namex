import os
import logging


class Config(object):

    NRO_SERVICE_ACCOUNT = 'nro_service_account'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

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

    # POSTGRESQL ORACLE_FDW
    FDW_DB_USER = os.getenv('FDW_DATABASE_USERNAME', '')
    FDW_DB_PASSWORD = os.getenv('FDW_DATABASE_PASSWORD', '')
    FDW_DB_NAME = os.getenv('FDW_DATABASE_NAME', '')
    FDW_DB_HOST = os.getenv('FDW_DATABASE_HOST', '')
    FDW_DB_PORT = os.getenv('FDW_DATABASE_PORT', '54321')
    SQLALCHEMY_BINDS = {
        'nro_db':        'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
            user=FDW_DB_USER,
            password=FDW_DB_PASSWORD,
            host=FDW_DB_HOST,
            port=int(FDW_DB_PORT),
            name=FDW_DB_NAME
        )
    }
