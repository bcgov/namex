
import os

import dotenv

# Load all the environment variables from a .env file located in some directory above.
dotenv.load_dotenv(dotenv.find_dotenv())

class Config(object):
    """Create base config object."""

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
     # The Flask secret key used to encrypt cookies. This must be kept secret and should be unique per environment. Do
    # not allow a missing value.
    SECRET_KEY = os.getenv("SOLR_SYNONYMS_API_FLASK_SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("Environment variable SOLR_SYNONYMS_API_FLASK_SECRET_KEY in not defined")

    # Turn this off to get rid of warning messages. In future versions of SQLAlchemy, False will be the default and
    # this can be removed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # POSTGRESQL
    DB_USER = os.getenv("DATABASE_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_NAME", "")
    DB_HOST = os.getenv("DATABASE_HOST", "")
    DB_PORT = int(os.getenv("DATABASE_PORT", "5432"))

    DB_SCHEMA = os.getenv("DATABASE_SCHEMA", "public")
    DB_IP_TYPE = os.getenv("DATABASE_IP_TYPE", "private")
    DB_OWNER = os.getenv("DATABASE_OWNER", "postgres")

    if DB_INSTANCE_CONNECTION_NAME := os.getenv("DATABASE_INSTANCE_CONNECTION_NAME", None):
        SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DEBUG = False
    TESTING = False


class DevConfig(Config):
    """Dev config."""

    DEBUG = True
    TESTING = True


class TestConfig(Config):
    """Test config."""

    DEBUG = True
    TESTING = True

    # POSTGRESQL
    DB_USER = os.getenv("DATABASE_TEST_USERNAME", "postgres")
    DB_PASSWORD = os.getenv("DATABASE_TEST_PASSWORD", "postgres")
    DB_NAME = os.getenv("DATABASE_TEST_NAME", "unittesting")
    DB_HOST = os.getenv("DATABASE_TEST_HOST", "localhost")
    DB_PORT = os.getenv("DATABASE_TEST_PORT", "5432")
    SQLALCHEMY_DATABASE_URI = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}"

class MigrationConfig(Config):
    """Config for db migration."""

    TESTING = False
    DEBUG = True

CONFIGURATION = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": Config,
    "default": Config,
}
