# Copyright © 2022 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Manage endpoints."""
from flask import Blueprint, Flask  # noqa: I001


class Endpoint:  # pylint: disable=too-few-public-methods
    """Manage the mounting, traversal and redirects for an enpoint."""

    def __init__(self, name: str, bps: list, app: Flask = None):
        """Initialize the endpoint and mount the blueprints to it."""
        self.app = None
        self.bp = Blueprint(name, __name__, url_prefix='/api/v1')

        for bp in bps:  # pylint: disable=invalid-name
            self.bp.register_blueprint(bp)

        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Add the version endpoint to the app."""
        if not app:
            raise Exception('Cannot initialize without a Flask App.')
        self.app = app
        self.app.register_blueprint(self.bp)
