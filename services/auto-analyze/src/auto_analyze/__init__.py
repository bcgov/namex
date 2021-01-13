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

# IMPORTANT: Without this, Flask-SQLAlchemy may not work!
# See https://pgjones.gitlab.io/quart/how_to_guides/flask_extensions.html
# This is important as this will add modules purporting to be Flask modules for later use by the extension.
import quart.flask_patch
# Thanks!

import asyncio
import os
from time import time

import config  # pylint: disable=wrong-import-order; # noqa: I001
from namex import models
from namex.models import db, ma
from namex.services.name_request.auto_analyse.name_analysis_utils import get_flat_list, get_synonyms_dictionary
from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService
from .analyzer import get_substitutions_dictionary
from quart import Quart, jsonify, request

from synonyms.services import SynonymService

from .analyzer import auto_analyze, clean_name, get_compound_synonyms, update_name_tokens

# Set config
QUART_APP = os.getenv('QUART_APP')
RUN_MODE = os.getenv('FLASK_ENV', 'production')

app: Quart


def register_shellcontext(quart_app):
    """
    Register shell context objects.
    """
    def shell_context():
        """
        Shell context objects.
        """
        return {
            'app': quart_app,
            # 'jwt': jwt,
            'db': db,
            'models': models
        }

    quart_app.shell_context_processor(shell_context)


async def create_app(run_mode):
    try:
        print('CREATING APPLICATION')
        quart_app = Quart(__name__)
        quart_app.config.from_object(config.CONFIGURATION[run_mode])
        db.app = quart_app
        quart_app.db = db
        db.init_app(quart_app)
        ma.init_app(quart_app)
    except Exception as err:
        print('Error creating application in auto-analyze service: ' + repr(err.with_traceback(None)))
        raise

    @quart_app.after_request
    def after_request(response):
        # if db is not None:
        #     print('Closing AutoAnalyze service DB connections')
        #     db.engine.dispose()

        return response

    @quart_app.after_request
    def add_version(response):
        os.getenv('OPENSHIFT_BUILD_COMMIT', '')
        return response

    register_shellcontext(quart_app)
    await quart_app.app_context().push()
    return quart_app

loop = asyncio.get_event_loop()
loop.set_debug(True)
app = loop.run_until_complete(create_app(RUN_MODE))


@app.route('/', methods=['POST'])
async def main():
    """
    The auto analyze service used to analyze an array of names!
    """
    name_analysis_service = ProtectedNameAnalysisService()
    syn_svc = SynonymService()
    np_svc_with_prep_data = name_analysis_service.name_processing_service
    np_svc_with_prep_data.prepare_data()

    json_data = await request.get_json()
    list_dist = json_data.get('list_dist')
    list_desc = json_data.get('list_desc')
    list_name = json_data.get('list_name')
    dict_substitution = json_data.get('dict_substitution')
    dict_synonyms = json_data.get('dict_synonyms')
    # TODO: Lucas - this limit is temporary we need to throttle the async loops
    #  that process the names so we don't crash due to too many connections
    matches = json_data.get('names')[:25]

    app.logger.debug('Number of matches: {0}'.format(len(matches)))

    start_time = time()
    # result = await asyncio.gather(
    #     *[auto_analyze(name, list_name, list_dist, list_desc, dict_substitution, dict_synonyms, np_svc_prep_data)
    #       for
    #       name in matches]
    # )
    name_tokens_clean_dict_list = await asyncio.gather(
        *[clean_name(name, np_svc_with_prep_data) for name in matches]
    )
    name_tokens_clean_dict = dict(pair for d in name_tokens_clean_dict_list for pair in d.items())

    stand_alone_words = np_svc_with_prep_data.get_stand_alone_words()

    list_words = list(set(get_flat_list(list(name_tokens_clean_dict.values()))))

    dict_all_simple_synonyms = get_synonyms_dictionary(syn_svc, dict_synonyms, list_words)
    dict_all_compound_synonyms = get_compound_synonyms(np_svc_with_prep_data, name_tokens_clean_dict,
                                                       syn_svc, dict_all_simple_synonyms)

    dict_all_synonyms = {**dict_synonyms, **dict_all_simple_synonyms}

    # Need to split in compound terms the name
    name_tokens_clean_dict = update_name_tokens(list(dict_all_compound_synonyms.keys()), name_tokens_clean_dict)

    list_words = list(set(get_flat_list(list(name_tokens_clean_dict.values()))))

    dict_all_substitutions = get_substitutions_dictionary(syn_svc, dict_substitution, dict_all_synonyms, list_words)

    result = await asyncio.gather(
        *[auto_analyze(name, name_tokens, list_name, list_dist, list_desc, dict_all_substitutions,
                       dict_all_synonyms, dict_all_compound_synonyms, stand_alone_words, name_analysis_service) for
          name, name_tokens in name_tokens_clean_dict.items()]
    )

    print('### Conflict analysis for {count} matches in {time} seconds ###'.format(
        count=len(matches),
        time=(time() - start_time)
    ))
    print('### Average match analysis time: {time} seconds / name ###'.format(
        time=((time() - start_time) / len(matches))
    ))

    return jsonify(result=result)


if __name__ == '__main__':
    app.run(port=7000, host='localhost')
