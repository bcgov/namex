"""Application configuration module for the Bad Name Notifier service."""

# pylint: disable=too-few-public-methods
import os

from dotenv import load_dotenv

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the .env file from the project root
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    """Base configuration class."""

    # Database Configuration
    DB_USER = os.getenv("DATABASE_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_NAME", "")
    DB_HOST = os.getenv("DATABASE_HOST", "")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")

    DB_SCHEMA = os.getenv("DATABASE_SCHEMA", "public")
    DB_IP_TYPE = os.getenv("DATABASE_IP_TYPE", "private")
    DB_OWNER = os.getenv("DATABASE_OWNER", "")

    if DB_INSTANCE_CONNECTION_NAME := os.getenv(
        "DATABASE_INSTANCE_CONNECTION_NAME", None
    ):
        SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    # Email Configuration
    EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")
    NOTIFY_API_URL = (
        f"{os.getenv('NOTIFY_API_URL', '')}"
        f"{os.getenv('NOTIFY_API_VERSION', '')}"
        "/notify"
    )
    ACCOUNT_SVC_AUTH_URL = os.getenv("KEYCLOAK_AUTH_TOKEN_URL", "")
    ACCOUNT_SVC_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "")
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")

    # General Settings
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    """Development-specific configuration."""

    DEBUG = True
    TESTING = False


class TestConfig(Config):
    """Testing-specific configuration."""

    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    """Production-specific configuration."""

    DEBUG = False
    TESTING = False


# Environment-specific configuration mapping
APP_CONFIG = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
    "default": ProdConfig,
}


def get_named_config(config_name: str = "default"):
    """Return the configuration object based on the name.

    :raise: KeyError: if an unknown configuration is requested
    """
    if config_name not in APP_CONFIG:
        raise KeyError(f"Unknown configuration: {config_name}")
    return APP_CONFIG[config_name]
