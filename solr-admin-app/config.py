
import os

from dotenv import load_dotenv, find_dotenv


# Load all the environment variables from a .env file located in the project root.
load_dotenv(find_dotenv())

CONFIGURATION = {
    "development": "config.DevConfig",
    "testing": "config.TestConfig",
    "production": "config.Config",
    "default": "config.Config"
}


class Config(object):
    # Create secret key so we can use sessions.
    SECRET_KEY = os.urandom(24)

    # Turn this off to get rid of warning messages. In future versions of SQLAlchemy, false will be the default and
    # this can be removed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # PostgreSQL Connection information.
    DB_USER = os.getenv("SOLR_ADMIN_DATABASE_USERNAME", "")
    DB_PASSWORD = os.getenv("SOLR_ADMIN_DATABASE_PASSWORD", "")
    DB_HOST = os.getenv("SOLR_ADMIN_DATABASE_HOST", "")
    DB_PORT = os.getenv("SOLR_ADMIN_DATABASE_PORT", "5432")
    DB_NAME = os.getenv("SOLR_ADMIN_DATABASE_NAME", "solr")

    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{name}".format(
         user=DB_USER,
         password=DB_PASSWORD,
         host=DB_HOST,
         port=int(DB_PORT),
         name=DB_NAME,
    )

    TESTING = False
    DEBUG = False


class DevConfig(Config):
    SQLALCHEMY_ECHO = True
    TESTING = False
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
