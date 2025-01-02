import os
from dotenv import find_dotenv, load_dotenv

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the .env file from the project root
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Config:
    # Database Configuration
    DB_USER = os.getenv("NAMEX_DATABASE_USERNAME", "")
    DB_PASSWORD = os.getenv("NAMEX_DATABASE_PASSWORD", "")
    DB_NAME = os.getenv("NAMEX_DATABASE_NAME", "")
    DB_HOST = os.getenv("NAMEX_DATABASE_HOST", "")
    DB_PORT = os.getenv("NAMEX_DATABASE_PORT", "5432")
    NAMEX_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Email Configuration
    EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "")
    SMTP_USER = os.getenv("SMTP_USER", "")

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
