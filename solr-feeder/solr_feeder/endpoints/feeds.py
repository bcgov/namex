# Copyright © 2023 Province of British Columbia
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
"""Manages feeder api endpoints."""
from http import HTTPStatus

import flask
from flask import Blueprint, current_app

from solr_feeder import solr
from solr_feeder.services import update_search_cores

from .utils import feeds_validate


bp = Blueprint('FEEDER', __name__, url_prefix='/feeds')  # pylint: disable=invalid-name


# Feed the specified core with the given data.
@bp.post('')
def feed_solr():
    """Update the solr cores for namex and search.

    Expected payload for updating namex core:
        {
            solr_core: str,
            request: <raw str representation of solr update/delete object for request>
        }

    Expected payload for updating registries search core:
        {
            solr_core: str,
            identifier: str,
            legalType: str
        }
    """
    current_app.logger.debug('request raw data: %s', flask.request.data)
    json_data = flask.request.get_json()
    if error := feeds_validate(json_data):
        current_app.logger.error(error)
        return {'message': error}, HTTPStatus.BAD_REQUEST

    solr_core = json_data['solr_core']

    if solr_core == 'search':
        # update registries search AND bor search
        errors = update_search_cores(json_data['identifier'], json_data['legalType'])
        if errors:
            return error

    else:
        current_app.logger.debug('Updating namex core record...')
        error_response = solr.update_core(solr_core, json_data['request'])
        if error_response:
            current_app.logger.error(f'Error updating namex core: {error_response}')
            return {'message': error_response['message']}, error_response['status_code']

        current_app.logger.debug('Namex core updated.')

    return {'message': 'Solr core updated'}, HTTPStatus.OK
