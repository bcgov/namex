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
"""The service that analyizes an array of names."""
# This is important as this will add modules purporting to be Flask modules for later use by the extension.
# Without this, Flask-SQLAlchemy may not work!
import quart.flask_patch
# Thanks!

import asyncio
import os

from quart import Quart, jsonify, request
import config
from nltk.stem import PorterStemmer

porter = PorterStemmer()

from namex import models
from namex.models import db, ma
from .analyzer import auto_analyze

# Set config
QUART_APP = os.getenv('QUART_APP')
RUN_MODE = os.getenv('FLASK_ENV', 'production')


async def create_app(run_mode):
    try:
        print('CREATING APPLICATION')
        quart_app = Quart(__name__)
        quart_app.config.from_object(config.CONFIGURATION[run_mode])
        db.init_app(quart_app)
        ma.init_app(quart_app)
    except Exception as err:
        print('Error creating application in auto-analyze service: ' + repr(err.with_traceback(None)))
        raise

    @quart_app.after_request
    def add_version(response):
        os.getenv('OPENSHIFT_BUILD_COMMIT', '')
        return response

    register_shellcontext(quart_app)
    await quart_app.app_context().push()
    return quart_app


def register_shellcontext(quart_app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'app': quart_app,
            # 'jwt': jwt,
            'db': db,
            'models': models
        }

    quart_app.shell_context_processor(shell_context)


loop = asyncio.get_event_loop()
app = loop.run_until_complete(create_app(RUN_MODE))
db.app = app  # Just set it, see if it works...


@app.route('/', methods=['POST'])
async def private_service():
    """Return the outcome of this private service call."""
    json_data = await request.get_json()
    list_dist = json_data.get("list_dist")
    list_desc = json_data.get("list_desc")
    list_name = json_data.get("list_name")
    dict_substitution = json_data.get("dict_substitution")
    dict_synonyms = json_data.get("dict_synonyms")
    matches = json_data.get('names')

    print("Number of matches: ", len(matches))
    result = await asyncio.gather(
        *[auto_analyze(name, list_name, list_dist, list_desc, dict_substitution, dict_synonyms) for name in matches]
    )
    return jsonify(result=result)


if __name__ == "__main__":
    app.run(port=7000, host='localhost')

