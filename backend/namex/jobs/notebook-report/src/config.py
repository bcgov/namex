import os

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class Config(object):
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'postgres')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'unittesting')
    DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')

    DATABASE_SCHEMA = os.getenv('DATABASE_SCHEMA', 'public')
    DATABASE_IP_TYPE = os.getenv('DATABASE_IP_TYPE', 'private')
    DATABASE_OWNER = os.getenv('DATABASE_OWNER', 'postgres')

    if DATABASE_INSTANCE_CONNECTION_NAME := os.getenv('DATABASE_INSTANCE_CONNECTION_NAME', None):
        SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://'
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
        
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    APP_FILE = os.getenv('APP_FILE', '')
    DAILY_REPORT_RECIPIENTS = os.getenv('DAILY_REPORT_RECIPIENTS', '')
    WEEKLY_REPORT_NAMEX_RECIPIENTS = os.getenv('WEEKLY_REPORT_NAMEX_RECIPIENTS', '')    
    WEEK_REPORT_DATE = os.getenv('WEEK_REPORT_DATE', '[0,1,2,3,4,5]')
    ERROR_EMAIL_RECIPIENTS = os.getenv('ERROR_EMAIL_RECIPIENTS', '')
    ENVIRONMENT = os.getenv('ENVIRONMENT', '')
     
    NOTIFY_API_URL = f"{os.getenv("NOTIFY_API_URL", "") + os.getenv("NOTIFY_API_VERSION", "")}/notify"
    NOTIFY_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
    NOTIFY_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
    KEYCLOAK_AUTH_TOKEN_URL = os.getenv("KEYCLOAK_AUTH_TOKEN_URL")


