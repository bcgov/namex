
import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv(), override=True)

CONFIGURATION = {
    'development': 'config.DevConfig',
    'testing': 'config.TestConfig',
    'production': 'config.Config',
    'default': 'config.Config'
}


class Config(object):
    SECRET_KEY = 'My Secret'

    # Normal Keycloak parameters.
    OIDC_CLIENT_SECRETS = os.getenv('SOLR_ADMIN_APP_OIDC_CLIENT_SECRETS', '')
    OIDC_SCOPES = ['openid', 'email', 'profile']
    OIDC_VALID_ISSUERS = [os.getenv('SOLR_ADMIN_APP_OIDC_VALID_ISSUERS', '')]
    OVERWRITE_REDIRECT_URI = os.getenv('SOLR_ADMIN_APP_OVERWRITE_REDIRECT_URI', '')

    print("OIDC" + OIDC_CLIENT_SECRETS)
    # Undocumented Keycloak parameter: allows sending cookies without the secure flag, which we need for the local
    # non-TLS HTTP server. Set this to non-"True" for local development, and use the default everywhere else.
    OIDC_ID_TOKEN_COOKIE_SECURE = os.getenv('SOLR_ADMIN_APP_OIDC_ID_TOKEN_COOKIE_SECURE', 'True') == 'True'

    # Turn this off to get rid of warning messages. In future versions of SQLAlchemy, False will be the default and
    # this can be removed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # PostgreSQL Connection information.
    DATABASE_USER = os.getenv('SOLR_ADMIN_APP_DATABASE_USERNAME', '')
    DATABASE_PASSWORD = os.getenv('SOLR_ADMIN_APP_DATABASE_PASSWORD', '')
    DATABASE_HOST = os.getenv('SOLR_ADMIN_APP_DATABASE_HOST', '')
    DATABASE_PORT = os.getenv('SOLR_ADMIN_APP_DATABASE_PORT', '54321')
    DATABASE_NAME = os.getenv('SOLR_ADMIN_APP_DATABASE_NAME', 'solr')

    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=int(DATABASE_PORT), name=DATABASE_NAME)

    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_ECHO = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    from solr_admin.keycloak import Keycloak

    class FakeOidc:
        user_loggedin = True

        def user_getfield(self, key):
            return 'Joe'

    Keycloak._oidc = FakeOidc()

