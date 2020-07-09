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


@cors_preflight('POST')
@api.route('/', strict_slashes=False, methods=['POST', 'OPTIONS'])
class NameRequests(BaseNameRequest):
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def post(self):
        self._before_create_or_update()

        name_request = self.map_request_data(self.create_name_request())
        request_state_code = self.request_state_code

        name_request = self.save_request(name_request)

        try:
            nr_model = Request.find_by_nr(name_request.nrNum)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the New NR from the db.', 500)

        # Map applicants from the request data to the name request
        nr_model = self.map_request_applicants(nr_model)
        nr_model = self.save_request(nr_model)

        # Map any submitted names and save the request
        nr_model = self.map_request_names(nr_model)
        nr_model = self.save_request(nr_model)

        try:
            # Save the request to NRO
            # nr_model = self.save_request_to_nro(nr_model, request_state_code)
            nr_model = self.save_request(nr_model)
            EventRecorder.record(self.user, Event.POST, name_request, self.request_data)
        except Exception as err:
            return handle_exception(err, 'Error saving nr and names.', 500)

        # Update SOLR
        self.update_solr_doc(nr_model, name_request)

        current_app.logger.debug(nr_model.json())
        return jsonify(nr_model.json()), 200


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

            existing_name_request = Request.find_by_nr(nr_num)
            self.nr_num = existing_name_request.nrNum
            self.nr_id = existing_name_request.id

            name_request = self.map_request_data(existing_name_request)
            name_request = self.save_request(name_request)

            try:
                nr_model = Request.find_by_nr(name_request.nrNum)
            except Exception as err:
                return handle_exception(err, 'Error retrieving the Updated NR from the db.', 500)

            # If there's no payment token, just update the data
            if nr_model.payment_token is None:
                # Map applicants from the request data to the name request
                nr_model = self.map_request_applicants(nr_model)
                nr_model = self.save_request(nr_model)

                # Map any submitted names and save the request
                nr_model = self.map_request_names(nr_model)
                nr_model = self.save_request(nr_model)
            else:
                # If there IS a payment token, update the name request state
                if nr_model.stateCd == State.COND_RESERVE:
                    self.apply_state_change(nr_model, State.CONDITIONAL)
                if nr_model.stateCd == State.RESERVED:
                    self.apply_state_change(nr_model, State.APPROVED)

                nr_model = self.save_request(nr_model)

            # TODO: Update nro to use REAL NR Num
            try:
                # Save the request to NRO
                # request_state_code = self.request_state_code
                # nr_model = self.save_request_to_nro(nr_model, request_state_code)
                # TOD: Update this event recorder!
                EventRecorder.record(self.user, Event.PUT, name_request, self.request_data)
            except Exception as err:
                return handle_exception(err, 'Error saving nr and names.', 500)

            # Update SOLR
            self.update_solr_doc(nr_model, name_request)

            current_app.logger.debug(nr_model.json())
            return jsonify(nr_model.json()), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)
