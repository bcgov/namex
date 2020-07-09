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


def on_nro_save_success(name_request):
    # Added the oracle request_id in new_nr, need to save it postgres
    # set the furnished_flag='Y' for approved and conditionally approved
    if name_request.stateCd in [State.APPROVED, State.CONDITIONAL]:
        name_request.furnished = 'Y'


@cors_preflight('POST')
@api.route('/', strict_slashes=False, methods=['POST', 'OPTIONS'])
class NameRequests(BaseNameRequest):
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def post(self):
        try:
            self._before_create_or_update()

            # Create a new DRAFT name request
            nr_model = self.create_name_request()

            def create_model_collections(nr, resource):
                """
                :param nr: The name request model
                :return:
                """
                # Map the request data and save so we have a name request ID to use for collection ops
                nr = self.map_request_data(nr, True)  # Set map_draft_attrs to True
                nr = self.save_request(nr)
                # Map applicants from the request data to the name request
                nr = self.map_request_applicants(nr)
                # Map any submitted names from the request data to the name request
                nr = self.map_request_names(nr)
                # Save
                nr = self.save_request(nr)
                return nr

            # Transition the DRAFT to the state specified in the request:
            # eg. one of [State.DRAFT, State.COND_RESERVE, State.RESERVED]
            self.apply_state_change(nr_model, self.request_state_code, create_model_collections)

            # Save the request to NRO and back to postgres
            if nr_model.stateCd in [State.DRAFT, State.APPROVED, State.CONDITIONAL]:
                nr_model = self.save_request_to_nro(nr_model, on_nro_save_success)

            nr_model = self.save_request(nr_model)

            # Record the event
            EventRecorder.record(self.user, Event.POST, nr_model, self.request_data)

            # Update SOLR
            self.create_or_update_solr_doc(nr_model)

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
            self._before_create_or_update()

            nr_model = Request.find_by_nr(nr_num)
            self.nr_num = nr_model.nrNum
            self.nr_id = nr_model.id

            def update_model_collections(nr, resource):
                """
                :param nr: The name request model
                :return:
                """
                nr = self.map_request_data(nr, False)
                # Map applicants from the request data to the name request
                nr = self.map_request_applicants(nr)
                # Map any submitted names from the request data to the name request
                nr = self.map_request_names(nr)
                # Save
                nr = self.save_request(nr)
                return nr

            def update_reserved_names_state(nr):
                nr = self.map_request_names(nr)
                nr = self.save_request(nr)
                return nr

            # If there's no payment token, just update the data
            if nr_model.payment_token is None:
                # If no payment token...
                if nr_model.stateCd in [State.DRAFT, State.COND_RESERVE, State.RESERVED]:
                    self.apply_state_change(nr_model, nr_model.stateCd, update_model_collections)

            # If there IS a payment token, we need to update the name request state and the request names state
            if nr_model.payment_token:
                if nr_model.stateCd == State.COND_RESERVE:
                    self.apply_state_change(nr_model, State.CONDITIONAL, update_reserved_names_state)
                if nr_model.stateCd == State.RESERVED:
                    self.apply_state_change(nr_model, State.APPROVED, update_reserved_names_state)

            # Save the request to NRO and back to postgres
            if nr_model.stateCd in [State.DRAFT, State.APPROVED, State.CONDITIONAL]:
                nr_model = self.save_request_to_nro(nr_model, on_nro_save_success)

            nr_model = self.save_request(nr_model)

            # Record the event
            EventRecorder.record(self.user, Event.PUT, nr_model, self.request_data)

            # Update SOLR
            if nr_model.stateCd in [State.RESERVED, State.COND_RESERVE]:
                self.create_or_update_solr_doc(nr_model)

            current_app.logger.debug(nr_model.json())
            return jsonify(nr_model.json()), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)
