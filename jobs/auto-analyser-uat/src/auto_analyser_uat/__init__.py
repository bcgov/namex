# Copyright © 2020 Province of British Columbia
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
"""The Auto Analyse UAT service."""
import os

from flask import Flask, current_app  # noqa: I001
# noqa:I004, I003
from auto_analyser_uat import config
from auto_analyser_uat.models import db


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')) -> Flask:
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)
    app.config.from_object(config.CONFIGURATION[run_mode])
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app
