# Copyright © 2020 Province of British Columbia
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
"""
Provides end points to submit, retrieve and cancel a name analysis request.
"""
from http import HTTPStatus

from flask import current_app, request
from flask_restx import Resource, cors, fields
import requests  # noqa: I001; grouping out of order to make both pylint & isort happy
from requests import exceptions  # noqa: I001; grouping out of order to make both pylint & isort happy

from namex.constants import (BCProtectedNameEntityTypes,
                             BCUnprotectedNameEntityTypes, ValidLocations,
                             XproUnprotectedNameEntityTypes)
from namex.services.name_request.auto_analyse import AnalysisRequestActions
from namex.utils.auth import cors_preflight

from .api_namespace import api as name_analysis_api

NAME_ANALYSIS_REQUEST_SCHEMA = name_analysis_api.model('NameAnalysisRequest', {
    'name': fields.String,
    'location': fields.String,
    'entity_type_cd': fields.String,
    'request_action_cd': fields.String
})


def validate_name_request(location, entity_type, request_action):
    """ Validates the name analysis request."""
    # Raise error if location is invalid
    if location not in ValidLocations.list():
        raise ValueError('Invalid location provided')

    # Raise error if request_action is invalid
    if request_action not in AnalysisRequestActions.list():
        raise ValueError('Invalid request action provided')

    # Throw any errors related to invalid entity_type or request_action for a location
    if location == ValidLocations.CA_BC.value:
        is_protected = False
        is_unprotected = False
        valid_request_actions = []

        if entity_type in BCProtectedNameEntityTypes.list():
            is_protected = True
            valid_request_actions = [
                AnalysisRequestActions.NEW.value,
                AnalysisRequestActions.CHG.value,
                AnalysisRequestActions.MVE.value
            ]
        elif entity_type in BCUnprotectedNameEntityTypes.list():
            is_unprotected = True
            valid_request_actions = (AnalysisRequestActions.NEW.value, AnalysisRequestActions.DBA.value)

        if is_protected and is_unprotected:
            raise ValueError('An entity name cannot be both protected and unprotected')

        if is_protected and entity_type not in BCProtectedNameEntityTypes.list():
            raise ValueError('Invalid entity_type provided for a protected BC entity name')

        if is_unprotected and entity_type not in BCUnprotectedNameEntityTypes.list():
            raise ValueError('Invalid entity_type provided for an unprotected BC entity name')

    else:
        valid_location = location in [ValidLocations.CA_NOT_BC.value, ValidLocations.INTL.value]
        valid_request_actions = [
            AnalysisRequestActions.NEW.value,
            AnalysisRequestActions.AML.value,
            AnalysisRequestActions.CHG.value,
            AnalysisRequestActions.ASSUMED.value,
            AnalysisRequestActions.REN.value,
            AnalysisRequestActions.REH.value
        ]

        if not valid_location:
            raise ValueError('Invalid location provided')

        if entity_type not in XproUnprotectedNameEntityTypes.list():
            raise ValueError('Invalid entity_type provided for an XPRO entity')

    if request_action not in valid_request_actions:
        raise Exception('Operation not currently supported')

    return True


@cors_preflight('GET, POST, DELETE')
@name_analysis_api.route('/<string:identifier>', methods=['GET', 'DELETE', 'OPTIONS'])
@name_analysis_api.route('', methods=['POST', 'OPTIONS'])
class NameAnalysisResource(Resource):
    """Wrapper service for Name analyzer."""
    @staticmethod
    @cors.crossdomain(origin='*')
    @name_analysis_api.expect(NAME_ANALYSIS_REQUEST_SCHEMA)
    def post():
        """Posts a name analysis request to the name analyzer.
        Returns a identifier if the request is successful."""
        json_input = request.get_json()
        location = json_input.get('location')
        entity_type = json_input.get('entity_type_cd')
        request_action = json_input.get('request_action_cd')

        if not validate_name_request(location, entity_type, request_action):
            return {'error': 'Invalid Name Request.'}, HTTPStatus.BAD_REQUEST

        auto_analyze_svc_url = current_app.config.get('AUTO_ANALYZE_URL')
        try:
            headers = {'Content-Type': 'application/json'}
            rv = requests.post(url=auto_analyze_svc_url,
                               json=json_input,
                               headers=headers,
                               timeout=20.0)
            return rv.json(), rv.status_code
        except (exceptions.ConnectionError, exceptions.Timeout):
            return {'message': 'Unable to create name analyze request.'}, HTTPStatus.SERVICE_UNAVAILABLE

    @staticmethod
    @cors.crossdomain(origin='*')
    def get(identifier):
        """Retrieve the status of a name analysis request from the name analyzer."""
        if not identifier:
            return {'error': 'Invalid  name analysis request Identifier.'}, HTTPStatus.BAD_REQUEST
        try:
            auto_analyze_svc_url = '{}/{}'.format(current_app.config.get('AUTO_ANALYZE_URL'), identifier)
            headers = {}
            rv = requests.get(url=auto_analyze_svc_url, headers=headers, timeout=20.0)
            return rv.json(), rv.status_code

        except (exceptions.ConnectionError, exceptions.Timeout) as err:
            current_app.logger.error(f'Auto Analyze connection failure for {identifier}', err)
            return {'errors': [{'message': f'Unable to get name analysis results for the identifier {identifier}.'}]
                    }, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    @cors.crossdomain(origin='*')
    def delete(identifier):
        """Cancel the name analysis request corresponding to the given identifier."""
        if not identifier:
            return {'error': 'Invalid name analysis request identifier.'}, HTTPStatus.BAD_REQUEST

        try:
            auto_analyze_svc_url = '{}/{}'.format(current_app.config.get('AUTO_ANALYZE_URL'), identifier)
            headers = {}
            rv = requests.delete(url=auto_analyze_svc_url, headers=headers, timeout=20.0)
            return rv.json(), rv.status_code

        except (exceptions.ConnectionError, exceptions.Timeout) as err:
            current_app.logger.error(f'Auto Analyze connection failure for {identifier}', err)
            return {'errors':
                    [{'message': f'Unable to cancel name analysis for the identifier {identifier}.'}]
                    }, HTTPStatus.INTERNAL_SERVER_ERROR
