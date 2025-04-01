import os
from dotenv import load_dotenv, find_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class Config(object):
    _DB_USER = os.getenv("NAMEX_DATABASE_USERNAME", "")
    _DB_PASSWORD = os.getenv("NAMEX_DATABASE_PASSWORD", "")
    _DB_NAME = os.getenv("NAMEX_DATABASE_NAME", "")
    _DB_HOST = os.getenv("NAMEX_DATABASE_HOST", "")
    _DB_PORT = os.getenv("NAMEX_DATABASE_PORT", "5432")
    if DB_UNIX_SOCKET := os.getenv('NAMEX_DATABASE_UNIX_SOCKET', None):
        NAMEX_DATABASE_URI = f'postgresql+psycopg2://{_DB_USER}:{_DB_PASSWORD}@/{_DB_NAME}?host={DB_UNIX_SOCKET}'
    else:
        NAMEX_DATABASE_URI = f'postgresql://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}:{int(_DB_PORT)}/{_DB_NAME}'
        
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


