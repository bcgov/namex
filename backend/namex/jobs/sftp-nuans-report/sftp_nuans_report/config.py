"""Application configuration module."""

import os

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class Config:  # pylint: disable=too-few-public-methods
    """Base application configuration."""

    ENVIRONMENT = os.getenv('ENVIRONMENT', 'prod')
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    ERROR_EMAIL_RECIPIENTS = os.getenv('ERROR_EMAIL_RECIPIENTS', '')

    # Token
    ACCOUNT_SVC_AUTH_URL = os.getenv('KEYCLOAK_AUTH_TOKEN_URL', '')
    ACCOUNT_SVC_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID', '')
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv('KEYCLOAK_CLIENT_SECRET', '')

    # URLs
    NOTIFY_API_URL = (
        f"{os.getenv('NOTIFY_API_URL', '')}"
        f"{os.getenv('NOTIFY_API_VERSION', '')}/notify"
    )
    OCP_SFTP_URL = f"{os.getenv('OCP_SFTP_RELAY_URL', '')}/sftp/upload"

    # POSTGRESQL
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', '')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DATABASE_NAME = os.getenv('DATABASE_NAME', '')
    DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')

    DATABASE_SCHEMA = os.getenv('DATABASE_SCHEMA', 'public')
    DATABASE_IP_TYPE = os.getenv('DATABASE_IP_TYPE', 'private')
    DATABASE_OWNER = os.getenv('DATABASE_OWNER', 'postgres')

    if DATABASE_INSTANCE_CONNECTION_NAME := os.getenv(
        'DATABASE_INSTANCE_CONNECTION_NAME', None
    ):
        SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://'
    else:
        SQLALCHEMY_DATABASE_URI = (
            f'postgresql+pg8000://{DATABASE_USERNAME}:{DATABASE_PASSWORD}'
            f'@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
        )
