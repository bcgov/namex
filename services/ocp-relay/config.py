import os

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (ocp-sftp-relay)
load_dotenv(find_dotenv())


class Config:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    TESTING = False
    DEBUG = False
    SECRET_KEY = "a secret"

    # Keycloak Settings
    JWT_OIDC_WELL_KNOWN_CONFIG = os.getenv("JWT_OIDC_WELL_KNOWN_CONFIG")
    JWT_OIDC_ALGORITHMS = os.getenv("JWT_OIDC_ALGORITHMS")
    JWT_OIDC_ISSUER = os.getenv("JWT_OIDC_ISSUER")
    JWT_OIDC_CACHING_ENABLED = os.getenv("JWT_OIDC_CACHING_ENABLED")
    JWT_OIDC_JWKS_CACHE_TIMEOUT = int(os.getenv("JWT_OIDC_JWKS_CACHE_TIMEOUT", "300"))
    JWT_OIDC_AUDIENCE = os.getenv("JWT_OIDC_AUDIENCE")

    # SFTP Settings
    SFTP_HOST = os.getenv("SFTP_HOST")
    SFTP_PORT = os.getenv("SFTP_PORT")
    SFTP_HOST_KEY = os.getenv("SFTP_HOST_KEY")
    SFTP_USERNAME = os.getenv("SFTP_USERNAME")
    BCREG_FTP_PRIVATE_KEY = os.getenv("BCREG_FTP_PRIVATE_KEY").replace("\\n", "\n")
    BCREG_FTP_PRIVATE_KEY_PASSPHRASE = os.getenv("BCREG_FTP_PRIVATE_KEY_PASSPHRASE")

    # Pay DB
    PAY_DB_NAME = os.getenv("PAY_DB_NAME")
    PAY_HOST = os.getenv("PAY_HOST")
    PAY_PORT = os.getenv("PAY_PORT")
    PAY_USER = os.getenv("PAY_USER")
    PAY_PASSWORD = os.getenv("PAY_PASSWORD")
    PAY_SQLALCHEMY_DATABASE_URI = f"postgresql://{PAY_USER}:{PAY_PASSWORD}@" f"{PAY_HOST}:{int(PAY_PORT)}/{PAY_DB_NAME}"

    # Colin DB
    COLIN_DB_NAME = os.getenv("COLIN_DB_NAME")
    COLIN_HOST = os.getenv("COLIN_HOST")
    COLIN_PORT = os.getenv("COLIN_PORT")
    COLIN_USER = os.getenv("COLIN_USER")
    COLIN_PASSWORD = os.getenv("COLIN_PASSWORD")
