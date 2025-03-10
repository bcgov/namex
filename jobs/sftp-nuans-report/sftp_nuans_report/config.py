import os
from dotenv import load_dotenv, find_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())

class Config(object):
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'prod')
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  
    ERROR_EMAIL_RECIPIENTS = os.getenv('ERROR_EMAIL_RECIPIENTS', '')

    # Token
    ACCOUNT_SVC_AUTH_URL = os.getenv("KEYCLOAK_AUTH_TOKEN_URL", "")
    ACCOUNT_SVC_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "")
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")

    # URLs
    NOTIFY_API_URL = f"{os.getenv("NOTIFY_API_URL", "") + os.getenv("NOTIFY_API_VERSION", "")}/notify"
    OCP_SFTP_URL = f"{os.getenv("OCP_SFTP_RELAY_URL", "")}/sftp/upload"

    # POSTGRESQL
    PG_USER = os.getenv('PG_USER', '')
    PG_PASSWORD = os.getenv('PG_PASSWORD', '')
    PG_NAME = os.getenv('PG_DB_NAME', '')
    PG_HOST = os.getenv('PG_HOST', '')
    PG_PORT = os.getenv('PG_PORT', '5432')
    if DB_UNIX_SOCKET := os.getenv('PG_UNIX_SOCKET', None):
        SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@/{PG_NAME}?host={DB_UNIX_SOCKET}'
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{int(PG_PORT)}/{PG_NAME}'
