import re
from flask import request, jsonify
from flask_restplus import cors
from flask import current_app
from sqlalchemy import func

from namex.utils.logging import setup_logging
from namex.utils.util import cors_preflight

from namex.models import Request, Event, State, Applicant
from namex.criteria.request import RequestQueryCriteria

from namex.services import EventRecorder

from .utils import handle_exception, get_query_param_str, normalize_nr_num
from .base_name_request import api, BaseNameRequest, nr_request

from .exceptions import *

setup_logging()  # Important to do this first

SOLR_CORE = 'possible.conflicts'


def parse_nr_num(nr_num_str):
    nr_num = normalize_nr_num(nr_num_str) if nr_num_str else None
    if nr_num_str and not nr_num:
        raise InvalidInputError(message='Invalid NR number format provided')

    return nr_num


@cors_preflight('GET, POST')
@api.route('/', strict_slashes=False, methods=['GET', 'POST', 'OPTIONS'])
class NameRequests(BaseNameRequest):
    @cors.crossdomain(origin='*')
    @api.doc(params={
        'nrNum': 'NR Number - nrNum or emailAddress is required',
        'emailAddress': 'The applicant\'s email address - emailAddress or nrNum is required',
        'phoneNumber': 'The applicant\'s phone number - optional',
        'addrLine1': 'The applicant\'s address - optional'
    })
    def get(self):
        try:
            filters = []

            # Validate the request
            if len(request.args) == 0:
                raise InvalidInputError(message='No query parameters were specified in the request')

            nr_num_query_str = get_query_param_str('nrNum')
            email_address_query_str = get_query_param_str('emailAddress')

            if not nr_num_query_str and not email_address_query_str:
                raise InvalidInputError(message='Either an nrNum or emailAddress must be provided')

            # Continue
            nr_num = parse_nr_num(nr_num_query_str)
            email_address = email_address_query_str

            phone_number = get_query_param_str('phoneNumber')
            address_line = get_query_param_str('addrLine1')

            if nr_num:
                filters.append(func.lower(Request.nrNum) == nr_num.lower())
            if phone_number:
                strip_phone_number_chars_regex = r'[(\-)(\+)(\s)(\(|\))]'
                filters.append(
                    Request.applicants.any(
                        func.regexp_replace(Applicant.phoneNumber, strip_phone_number_chars_regex, '').contains(re.sub(strip_phone_number_chars_regex, '', phone_number))
                    )
                )

            if email_address:
                filters.append(
                    Request.applicants.any(
                        func.lower(Applicant.emailAddress).startswith(email_address.lower())
                    )
                )

            if address_line:
                # Addresses are all in uppercase cast
                filters.append(
                    Request.applicants.any(
                        func.lower(Applicant.addrLine1).startswith(address_line.lower())
                    )
                )

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
            # This validates the app config and processes the JSON request data, and stores it on the Resource instance.
            self._before_create_or_update()

            # Create a new DRAFT name request
            nr_model = self.create_name_request()

            def handle_name_request_creation(nr, resource):
                """
                All logic for creating the name request goes inside this handler, which is invoked on successful state change.
                :param nr: The name request model
                :param resource A reference to the current Resource instance (this controller)
                """
                # Map the request data and save so we have a name request ID to use for collection ops
                nr = resource.map_request_data(nr, True)  # Set map_draft_attrs to True
                nr = resource.save_request(nr)
                # Map applicants from the request data to the name request
                nr = resource.map_request_applicants(nr)
                # Map any submitted names from the request data to the name request
                nr = resource.map_request_names(nr)
                # Save
                nr = resource.save_request(nr)
                # Return the updated name request
                return nr

            # Handle state changes
            # Use apply_state_change to change state, as it enforces the State change pattern

            # Transition the DRAFT to the state specified in the request:
            # eg. one of [State.DRAFT, State.COND_RESERVE, State.RESERVED]
            nr_model = self.apply_state_change(nr_model, self.request_state_code, handle_name_request_creation)

            # Record the event
            EventRecorder.record(self.user, Event.POST, nr_model, self.request_data)

            # Update Solr - note that we don't save DRAFT name requests to Solr
            if nr_model.stateCd in [State.COND_RESERVE, State.RESERVED]:
                self.create_solr_nr_doc(SOLR_CORE, nr_model)

            current_app.logger.debug(nr_model.json())
            return jsonify(nr_model.json()), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)


@cors_preflight('GET, PUT')
@api.route('/<string:nr_num>', strict_slashes=False, methods=['GET', 'PUT', 'OPTIONS'])
class NameRequest(BaseNameRequest):
    @cors.crossdomain(origin='*')
    def get(self, nr_num):
        try:
            nr_num = parse_nr_num(nr_num)
            name_request = Request.find_by_nr(nr_num)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the NR from the db.', 500)

        return jsonify(name_request.json()), 200

    # REST Method Handlers
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def put(self, nr_num):
        try:
            # This validates the app config and processes the JSON request data, and stores it on the Resource instance.
            self._before_create_or_update()

            # Find the existing name request
            nr_num = parse_nr_num(nr_num)
            nr_model = Request.find_by_nr(nr_num)
            self.nr_num = nr_model.nrNum
            self.nr_id = nr_model.id

            # Declare our update handlers functions

            def handle_name_request_update(nr, resource):
                """
                Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
                :param nr: The name request model
                :param resource A reference to the current Resource instance (this controller)
                :return:
                """
                nr = resource.map_request_data(nr, False)
                # Map applicants from the request data to the name request
                nr = resource.map_request_applicants(nr)
                # Map any submitted names from the request data to the name request
                nr = resource.map_request_names(nr)
                # Save
                nr = resource.save_request(nr)
                # Return the updated name request
                return nr

            def handle_name_request_approval(nr, resource):
                """
                This method is for updating certain parts of the name request eg. its STATE when a payment token is present in the request.
                :param nr:
                :param resource:
                :return:
                """
                # Update the names, we can ignore everything else as this is only
                # invoked when we're completing a payment.
                nr = resource.map_request_names(nr)
                nr = resource.save_request(nr)
                # Return the updated name request
                return nr

            def on_nro_save_success(nr, resource):
                """
                :param nr:
                :param resource:
                :return:
                """

                nr = resource.save_request(nr)
                # Return the updated name request
                return nr

            # Handle state changes
            # Use apply_state_change to change state, as it enforces the State change pattern

            """
            This is the handler for a regular PUT from the frontend.
            """
            # If no payment token...
            if nr_model.payment_token is None and nr_model.stateCd in [State.DRAFT, State.COND_RESERVE, State.RESERVED]:
                # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
                nr_model = self.apply_state_change(nr_model, nr_model.stateCd, handle_name_request_update)

            """
            This is the handler for a special PUT case where a payment has been received 
            and we need to APPROVE or CONDITIONALLY APPROVE a name request:
            1. When the payment ID is set, check to see if we need to update the entity state.
            2a. If the entity is in a COND_RESERVE state, update its state to CONDITIONAL.   
            2b. If the entity is in a RESERVED state, update its state to APPROVED.
            3. Execute the callback handler (do any custom update logic and save the name request here).
            """
            # If the state is COND_RESERVE update state to CONDITIONAL, and update the name request as required
            if nr_model.payment_token and nr_model.stateCd == State.COND_RESERVE:
                # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
                nr_model = self.apply_state_change(nr_model, State.CONDITIONAL, handle_name_request_approval)
                # If the state is RESERVED update state to APPROVED, and update the name request as required
            elif nr_model.payment_token and nr_model.stateCd == State.RESERVED:
                # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
                nr_model = self.apply_state_change(nr_model, State.APPROVED, handle_name_request_approval)

            temp_nr_num = None
            # Save the request to NRO and back to postgres ONLY if the state is DRAFT, CONDITIONAL, or APPROVED
            # this is after fees are accepted
            if nr_model.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED]:
                existing_nr_num = nr_model.nrNum
                # This updates NRO, it should return the nr_model with the updated nrNum, which we save back to postgres in the on_nro_save_success handler
                nr_model = self.save_request_to_nro(nr_model, on_nro_save_success)
                # Set the temp NR number if its different
                if nr_model.nrNum != existing_nr_num:
                    temp_nr_num = existing_nr_num

            # Record the event
            EventRecorder.record(self.user, Event.PUT, nr_model, self.request_data)

            # Update SOLR
            if nr_model.stateCd in [State.COND_RESERVE, State.RESERVED, State.CONDITIONAL, State.APPROVED]:
                self.create_solr_nr_doc(SOLR_CORE, nr_model)
                if temp_nr_num:
                    # This performs a safe delete, we check to see if the temp ID exists before deleting
                    self.delete_solr_doc(SOLR_CORE, temp_nr_num)

            current_app.logger.debug(nr_model.json())
            return jsonify(nr_model.json()), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)
