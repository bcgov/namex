
import os

import flask
import sentry_sdk  # noqa: I001; grouped for pylint
from sentry_sdk.integrations.flask import FlaskIntegration  # noqa: I001; grouped for pylint

from solr_feeder.config import config
from solr_feeder.endpoints import endpoint
from solr_feeder.version import __version__


__all__ = ['create_application']


# Create the Flask application
def create_application(config_name: str = os.getenv('APP_ENV') or 'production', **kwargs):
    # Create application
    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])
    # Configure Sentry
    if dsn := app.config.get('SENTRY_DSN'):
        sentry_sdk.init(  # pylint: disable=E0110
            dsn=dsn,
            integrations=[FlaskIntegration()],
            environment=app.config.get('POD_NAMESPACE'),
            release=f'solr-feeder@{__version__}',
            traces_sample_rate=app.config.get('SENTRY_TSR')
        )
    endpoint.init_app(app)

    return app
