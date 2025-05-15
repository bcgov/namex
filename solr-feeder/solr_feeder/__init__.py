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
from structured_logging import StructuredLogging

from solr_feeder.config import config
from solr_feeder.endpoints import endpoint
from solr_feeder.version import __version__


__all__ = ['create_application']


def create_application(config_name: str = os.getenv('APP_ENV') or 'production'):
    """Create the Flask application."""
    app = flask.Flask(__name__)
    app.logger = StructuredLogging().get_logger()
    app.config.from_object(config[config_name])
    endpoint.init_app(app)

    return app
