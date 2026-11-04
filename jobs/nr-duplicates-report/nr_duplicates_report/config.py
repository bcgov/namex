import os
from dotenv import load_dotenv, find_dotenv
import base64

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class Config(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    ENVIRONMENT = os.getenv('ENVIRONMENT', '')

    # POSTGRESQL
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', '')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DATABASE_NAME = os.getenv('DATABASE_NAME', '')
    DATABASE_HOST = os.getenv('DATABASE_HOST', '')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
    DATABASE_SCHEMA = os.getenv('DATABASE_SCHEMA', 'public')
    if DATABASE_INSTANCE_CONNECTION_NAME := os.getenv('DATABASE_INSTANCE_CONNECTION_NAME', None):
        SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://'
    else:
        SQLALCHEMY_DATABASE_URI = (
            f'postgresql+pg8000://{DATABASE_USERNAME}:{DATABASE_PASSWORD}'
            f'@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
        )

    # Token Retrieval
    ACCOUNT_SVC_AUTH_URL = os.getenv("KEYCLOAK_AUTH_TOKEN_URL", "")
    ACCOUNT_SVC_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "")
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")

    # Notebook Config
    NUMBER_OF_DAYS_NR = os.getenv('NUMBER_OF_DAYS_NR', '1')
    NUMBER_OF_DAYS_PAYMENT = os.getenv('NUMBER_OF_DAYS_PAYMENT', '1')

    # OCP Relay
    OCP_RELAY_URL = os.getenv('OCP_RELAY_URL', '')

    # Email
    NOTIFY_API_URL = f"{os.getenv('NOTIFY_API_URL', '') + os.getenv('NOTIFY_API_VERSION', '')}/notify"
    REPORT_RECIPIENTS = os.getenv('REPORT_RECIPIENTS', '')
    ERROR_EMAIL_RECIPIENTS = os.getenv('ERROR_EMAIL_RECIPIENTS', '')

    # Google Storage
    TYPE = os.getenv('TYPE', '')
    PROJECT_ID = os.getenv('PROJECT_ID', '')
    CLIENT_ID = os.getenv('CLIENT_ID', '')
    CLIENT_EMAIL = os.getenv('CLIENT_EMAIL', '')
    AUTH_URI = os.getenv('AUTH_URI', '')
    TOKEN_URI = os.getenv('TOKEN_URI', '')
    AUTH_PROVIDER_X509_cert_URL = os.getenv('AUTH_PROVIDER_X509_cert_URL', '')
    CLIENT_X509_CERT_URL = os.getenv('CLIENT_X509_CERT_URL', '')
    PRIVATE_KEY_ID = os.getenv('PRIVATE_KEY_ID', '')
    try:
        pk_raw = os.getenv('PRIVATE_KEY', '').strip()
        pk_padded = pk_raw + '=' * (-len(pk_raw) % 4)
        PRIVATE_KEY = base64.b64decode(pk_padded).decode()
    except Exception:
        PRIVATE_KEY = os.getenv('PRIVATE_KEY', '')
