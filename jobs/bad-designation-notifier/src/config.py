import os
from dotenv import find_dotenv, load_dotenv

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the .env file from the project root
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Config:

    PROJECT_ROOT = BASE_DIR
    
    # Database Configuration
    _DB_USER = os.getenv("NAMEX_DATABASE_USERNAME", "")
    _DB_PASSWORD = os.getenv("NAMEX_DATABASE_PASSWORD", "")
    _DB_NAME = os.getenv("NAMEX_DATABASE_NAME", "")
    _DB_HOST = os.getenv("NAMEX_DATABASE_HOST", "")
    _DB_PORT = os.getenv("NAMEX_DATABASE_PORT", "5432")
    if DB_UNIX_SOCKET := os.getenv('NAMEX_DATABASE_UNIX_SOCKET', None):
        NAMEX_DATABASE_URI = f'postgresql+psycopg2://{_DB_USER}:{_DB_PASSWORD}@/{_DB_NAME}?host={DB_UNIX_SOCKET}'
    else:
        NAMEX_DATABASE_URI = f'postgresql://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}:{int(_DB_PORT)}/{_DB_NAME}'

    # Email Configuration
    EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")
    NOTIFY_API_URL = f"{os.getenv("NOTIFY_API_URL", "") + os.getenv("NOTIFY_API_VERSION", "")}/notify"
    ACCOUNT_SVC_AUTH_URL = os.getenv("KEYCLOAK_AUTH_TOKEN_URL", "")
    ACCOUNT_SVC_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "")
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")

    # General Settings
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    pass


# Environment-specific configuration mapping
_APP_CONFIG = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
    "default": ProdConfig,
}


def get_named_config(config_name: str = "default"):
    """Return the configuration object based on the name."""
    try:
        return _APP_CONFIG[config_name]
    except KeyError:
        raise KeyError(f"Unknown configuration: {config_name}")
