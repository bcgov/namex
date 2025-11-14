import os

from dotenv import find_dotenv, load_dotenv

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the .env file from the project root
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Config:

    PROJECT_ROOT = BASE_DIR
    
    # Database Configuration
    DB_USER = os.getenv('DATABASE_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'postgres')
    DB_NAME = os.getenv('DATABASE_NAME', 'unittesting')
    DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DB_PORT = os.getenv('DATABASE_PORT', '5432')

    DB_SCHEMA = os.getenv('DATABASE_SCHEMA', 'public')
    DB_IP_TYPE = os.getenv('DATABASE_IP_TYPE', 'private')
    DB_OWNER = os.getenv('DATABASE_OWNER', 'postgres')

    if DB_INSTANCE_CONNECTION_NAME := os.getenv('DATABASE_INSTANCE_CONNECTION_NAME', None):
        SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://'
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

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
