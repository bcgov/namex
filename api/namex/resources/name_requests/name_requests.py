import re
from sqlalchemy import func

from flask import request, jsonify, current_app
from flask_restplus import cors

from namex.utils.logging import setup_logging
from namex.utils.util import cors_preflight

from namex.models import Request, Event, State, Applicant
from namex.criteria.request import RequestQueryCriteria

from namex.services import EventRecorder
from namex.services.name_request.utils import handle_exception, get_query_param_str
from namex.services.name_request.exceptions import \
    NameRequestException, InvalidInputError

from .configuration import SOLR_CORE
from .api_namespace import api
from .api_models import nr_request
from .resource import NameRequestResource
from .utils import parse_nr_num

setup_logging()  # Important to do this first


@cors_preflight('GET, POST')
@api.route('/', strict_slashes=False, methods=['GET', 'POST', 'OPTIONS'])
class NameRequests(NameRequestResource):
    @cors.crossdomain(origin='*')
    @api.doc(params={
        'nrNum': 'NR Number - This field is required',
        'emailAddress': 'The applicant\'s email address - an emailAddress or a phoneNumber is required',
        'phoneNumber': 'The applicant\'s phone number - a phoneNumber or an emailAddress is required',
        # 'addrLine1': 'The applicant\'s address - optional'
    })
    def get(self):
        try:
            filters = []

            # Validate the request
            if len(request.args) == 0:
                raise InvalidInputError(message='No query parameters were specified in the request')

            nr_num_query_str = get_query_param_str('nrNum')
            email_address_query_str = get_query_param_str('emailAddress')
            phone_number_query_str = get_query_param_str('phoneNumber')

            if not nr_num_query_str:
                raise InvalidInputError(message='An nrNum must be provided')
            else:
                if not email_address_query_str and not phone_number_query_str:
                    raise InvalidInputError(message='Either an emailAddress or phoneNumber must be provided')

            # Continue
            nr_num = parse_nr_num(nr_num_query_str)
            email_address = email_address_query_str

            phone_number = get_query_param_str('phoneNumber')
            # Filter on addresses
            # address_line = get_query_param_str('addrLine1')

            if nr_num:
                filters.append(func.lower(Request.nrNum) == nr_num.lower())
            if phone_number:
                strip_phone_number_chars_regex = r"[^0-9]"
                filters.append(
                    Request.applicants.any(
                        func.regexp_replace(Applicant.phoneNumber, strip_phone_number_chars_regex, '', 'g').contains(re.sub(strip_phone_number_chars_regex, '', phone_number))
                    )
                )

            if email_address:
                filters.append(
                    Request.applicants.any(
                        func.lower(Applicant.emailAddress).startswith(email_address.lower())
                    )
                )

            '''
            Filter on addresses
            if address_line:
                filters.append(
                    Request.applicants.any(
                        func.lower(Applicant.addrLine1).startswith(address_line.lower())
                    )
                )
            '''

            criteria = RequestQueryCriteria(
                nr_num=nr_num,
                filters=filters
            )

            results = Request.find_by_criteria(criteria)

            if not results:
                results = []

        except InvalidInputError as err:
            return handle_exception(err, err.message, 400)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the NR from the db.', 500)

        if nr_num and len(results) == 1:
            return jsonify(results[0].json()), 200
        elif len(results) > 0:
            return jsonify(list(map(lambda result: result.json(), results))), 200

        return jsonify(results), 200

    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def post(self):
        try:
            # Creates a new NameRequestService, validates the app config, and sets the request data to the NameRequestService instance
            self.initialize()
            nr_svc = self.nr_service

            # Create a new DRAFT name request
            nr_model = nr_svc.create_name_request()

            # Handle state changes
            # Use apply_state_change to change state, as it enforces the State change pattern
            # Transition the DRAFT to the state specified in the request:
            # eg. one of [State.DRAFT, State.COND_RESERVE, State.RESERVED]
            nr_model = nr_svc.apply_state_change(nr_model, nr_svc.request_state_code, self.handle_nr_creation)

            # Record the event
            EventRecorder.record(nr_svc.user, Event.POST, nr_model, nr_svc.request_data)

            # Update Solr - note that we don't save DRAFT name requests to Solr
            if nr_model.stateCd in [State.COND_RESERVE, State.RESERVED]:
                self.create_solr_nr_doc(SOLR_CORE, nr_model)

            current_app.logger.debug(nr_model.json())
            return jsonify(nr_model.json()), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)

    """
    These Event callback 'actions' are fired off when Name Request state change is triggered.
    They are defined as static methods so we can easily test NameRequestService independently of this Resource (endpoint).
    """

    @staticmethod
    def handle_nr_creation(nr, svc):
        """
        All logic for creating the name request goes inside this handler, which is invoked on successful state change.
        :param nr: The name request model
        :param svc A reference to the current Resource instance (this controller)
        """
        # Map the request data and save so we have a name request ID to use for collection ops
        nr = svc.map_request_data(nr, True)  # Set map_draft_attrs to True
        nr = svc.save_request(nr)
        # Map applicants from the request data to the name request
        nr = svc.map_request_applicants(nr)
        # Map any submitted names from the request data to the name request
        nr = svc.map_request_names(nr)
        # Save
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr
