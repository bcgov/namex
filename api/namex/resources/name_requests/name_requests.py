from flask import jsonify
from flask_restplus import cors
from namex.utils.util import cors_preflight
from flask import current_app

from namex.utils.logging import setup_logging

from namex.models import Request, Event, State

from namex.services import EventRecorder

from .utils import handle_exception
from .base_name_request import api, BaseNameRequest, nr_request

from .exceptions import *

setup_logging()  # Important to do this first

SOLR_CORE = 'possible.conflicts'

@cors_preflight('POST')
@api.route('/', strict_slashes=False, methods=['POST', 'OPTIONS'])
class NameRequests(BaseNameRequest):
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
