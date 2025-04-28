# Copyright © c2021 Province of British Columbia
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
import re
import traceback

from flask import current_app, jsonify, make_response, request
from sqlalchemy import func

from namex.criteria.request import RequestQueryCriteria
from namex.models import Applicant, Event, Request, State
from namex.services import EventRecorder
from namex.services.audit_trail.hotjar_tracking import HotjarTracking
from namex.services.name_request.exceptions import (
    InvalidInputError,
    NameRequestException,
    NameRequestIsAlreadySubmittedError,
)
from namex.services.name_request.name_request_state import get_nr_state_actions
from namex.services.name_request.utils import get_mapped_entity_and_action_code
from namex.services.statistics.wait_time_statistics import WaitTimeStatsService
from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight, full_access_to_name_request

from .api_models import nr_request
from .api_namespace import api
from .base_nr_resource import BaseNameRequestResource
from .utils import parse_nr_num


@cors_preflight('GET, POST')
@api.route('/', strict_slashes=False, methods=['GET', 'POST', 'OPTIONS'])
class NameRequestsResource(BaseNameRequestResource):
    """Class to handle all name requests."""

    def get(self):
        """Name request search."""
        try:
            if not full_access_to_name_request(request):
                return {'message': 'You do not have access to this NameRequest.'}, 403

            filters = []

            bcreg_nr = None if request.headers['Bcreg-Nr'] == 'null' else request.headers['Bcreg-Nr']
            bcreg_nrl = None if request.headers['Bcreg-Nrl'] == 'null' else request.headers['Bcreg-Nrl']
            nr_num_query_str = bcreg_nr or bcreg_nrl
            email_address_query_str = request.headers['Bcreg-User-Email']
            phone_number_query_str = request.headers['Bcreg-User-Phone']

            if not nr_num_query_str:
                raise InvalidInputError(message='An nrNum must be provided')
            else:
                if not email_address_query_str and not phone_number_query_str:
                    raise InvalidInputError(message='Either an emailAddress or phoneNumber must be provided')

            # Continue
            nr_num = parse_nr_num(nr_num_query_str)
            email_address = email_address_query_str
            phone_number = phone_number_query_str
            # Filter on addresses
            # address_line = get_query_param_str('addrLine1')

            if nr_num:
                filters.append(func.lower(Request.nrNum) == nr_num.lower())
            if phone_number:
                strip_phone_number_chars_regex = r'[^0-9]'
                filters.append(
                    Request.applicants.any(
                        func.regexp_replace(Applicant.phoneNumber, strip_phone_number_chars_regex, '', 'g').contains(
                            re.sub(strip_phone_number_chars_regex, '', phone_number)
                        )
                    )
                )

            if email_address:
                filters.append(
                    Request.applicants.any(func.lower(Applicant.emailAddress).startswith(email_address.lower()))
                )

            criteria = RequestQueryCriteria(nr_num=nr_num, filters=filters)

            results = Request.find_by_criteria(criteria)

            if not results:
                results = []

        except InvalidInputError as err:
            return handle_exception(err, err.message, 400)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the NR from the db.', 500)

        if nr_num and len(results) == 1:
            nr_model = results[0]

            if nr_model.requestTypeCd and (not nr_model.entity_type_cd or not nr_model.request_action_cd):
                # If requestTypeCd is set, but a request_entity (entity_type_cd) and a request_action (request_action_cd)
                # are not, use get_mapped_entity_and_action_code to map the values from the requestTypeCd
                entity_type, request_action = get_mapped_entity_and_action_code(nr_model.requestTypeCd)
                nr_model.entity_type_cd = entity_type
                nr_model.request_action_cd = request_action

            response_data = nr_model.json()

            # If draft, get the wait time and oldest queued request
            if nr_model.stateCd == 'DRAFT':
                service = WaitTimeStatsService()
                wait_time_response = service.get_waiting_time_dict()
                response_data.update(wait_time_response)

            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = get_nr_state_actions(results[0].stateCd, results[0])
            return make_response(jsonify(response_data), 200)
        elif len(results) > 0:
            # We won't add the list of valid Name Request actions for the given state to the response if we're sending back a list
            # If the user / client accessing this data needs the Name Request actions, GET the individual record using NameRequest.get
            # This method, NameRequests.get is for Existing NR Search
            return make_response(jsonify([result.json() for result in results]), 200)

        # We won't add the list of valid Name Request actions for the given state to the response if we're sending back a list
        # If the user / client accessing this data needs the Name Request actions, GET the individual record using NameRequest.get
        # This method, NameRequests.get is for Existing NR Search
        return make_response(jsonify(results), 200)

    @api.expect(nr_request)
    def post(self):
        """Create a new name request."""
        try:
            # Creates a new NameRequestService, validates the app config, and sets the request data to the NameRequestService instance
            self.initialize()
            nr_svc = self.nr_service

            name_search_string = ''
            user_email = ''
            # user id
            submitter = nr_svc.request_data.get('applicants')
            for item, _index in zip(submitter, range(len(submitter))):
                user_email = item.get('emailAddress')

            # collect submitted user data names choices
            customer_data = nr_svc.request_names
            # loop through the list of choices obtained
            for item, index in zip(customer_data, range(len(customer_data))):
                # concat them with format saving as namesearch
                name_search_string += f'|{index + 1}{item.get("name")}{index + 1}|'
            # if same user submitted the request of same name choices again raise exception otherwise continue creating nr
            if Request().find_existing_name_by_user(name_search_string, user_email):
                raise NameRequestIsAlreadySubmittedError()
            # Create a new DRAFT name request
            nr_model = nr_svc.create_name_request()

            # Handle state changes
            # Use update_nr as it enforces the State change pattern
            # Transition the DRAFT to the state specified in the request:
            # eg. one of [State.DRAFT, State.COND_RESERVE, State.RESERVED]
            nr_model = self.update_nr(nr_model, nr_svc.request_state_code, self.handle_nr_create)

            # Record the event
            EventRecorder.record(nr_svc.user, Event.POST, nr_model, nr_model.json())

            # Record the hotjar user id
            if self.request_data.get('hotjarUserId'):
                HotjarTracking.record(nr_model, self.request_data.get('hotjarUserId'))

            nr_model.stateCd = State.PENDING_PAYMENT
            nr_model.save_to_db()

            # Update Solr - note that we don't save DRAFT name requests to Solr for corp entities only
            if nr_model.stateCd in [State.COND_RESERVE, State.RESERVED] and nr_model.entity_type_cd in [
                'CR',
                'UL',
                'BC',
                'CP',
                'PA',
                'XCR',
                'XUL',
                'XCP',
                'CC',
                'FI',
                'XCR',
                'XUL',
                'XCP',
            ]:
                SOLR_CORE = 'possible.conflicts'
                self.create_solr_nr_doc(SOLR_CORE, nr_model)

            current_app.logger.debug(nr_model.json())
            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = nr_svc.current_state_actions
            return make_response(jsonify(response_data), 201)
        except NameRequestException as err:
            current_app.logger.error('NameRequestException occurred: %s', traceback.format_exc())
            return handle_exception(err, err.message, 500)
        except Exception as err:
            current_app.logger.error('NameRequestException occurred: %s', traceback.format_exc())
            return handle_exception(err, repr(err), 500)
