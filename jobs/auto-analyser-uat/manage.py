# Copyright © 2019 Province of British Columbia
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

"""Manage the database for this service."""
import logging

from flask import url_for
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager  # class for handling a set of commands

# pylint: disable=unused-import; included so it can build the database migrations
from auto_analyser_uat import create_app, models  # NOQA:F401
from auto_analyser_uat.models import db


APP = create_app()
MIGRATE = Migrate(APP, db)
MANAGER = Manager(APP)

MANAGER.add_command('db', MigrateCommand)


@MANAGER.command
def list_routes():
    """List routes."""
    output = []
    for rule in APP.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = '[{0}]'.format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = ('{:50s} {:20s} {}'.format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


if __name__ == '__main__':
    logging.log(logging.INFO, 'Running the Manager')
    MANAGER.run()
