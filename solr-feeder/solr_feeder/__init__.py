# Copyright © 2023 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Manages app creation."""
import os

import flask
import sentry_sdk  # noqa: I001; grouped for pylint
from sentry_sdk.integrations.flask import FlaskIntegration  # noqa: I001; grouped for pylint

from solr_feeder.config import config
from solr_feeder.endpoints import endpoint
from solr_feeder.version import __version__


__all__ = ['create_application']


# Create the Flask application
def create_application(config_name: str = os.getenv('APP_ENV') or 'production'):
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
