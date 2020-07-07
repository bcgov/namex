from flask import jsonify
from flask_restplus import cors
from namex.utils.util import cors_preflight
from flask import current_app

from namex.utils.logging import setup_logging

from namex.models import Request, State

from .abstract import handle_exception, \
    map_request_applicants

from .name_request import api, nr_request, \
    BaseNameRequest

setup_logging()  # Important to do this first


@cors_preflight('POST')
@api.route('/', strict_slashes=False, methods=['POST', 'OPTIONS'])
class NameRequests(BaseNameRequest):
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def post(self):
        self._before_create_or_update()

        name_request = self.create_name_request()
        name_request = self.map_request_data(name_request)
        request_data = self.request_data
        nr_id = self.nr_id

        def on_success():
            try:
                nr = Request.find_by_nr(name_request.nrNum)
                # Map applicants from the request data to the name request
                applicants = map_request_applicants(request_data, nr_id)
                nr.applicants = applicants
                nr.save_to_db()

            except Exception as err:
                return handle_exception(err, 'Error saving request applicants.', 500)

        self.save_request(name_request, on_success)

        try:
            updated_nr = Request.find_by_nr(name_request.nrNum)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the New NR from the db.', 500)

        self.create_or_update_names(updated_nr)
        self.update_solr_doc(updated_nr, name_request)

        current_app.logger.debug(name_request.json())
        return jsonify(name_request.json()), 200


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
    # @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def put(self, nr_num):
        self._before_create_or_update()

        name_request = Request.find_by_nr(nr_num)
        self.nr_num = name_request.nrNum
        self.nr_id = name_request.id

        # TODO: Technically we should replace / update the data and applicants
        def on_success():
            try:
                # This isn't required as per the TODO above...
                # nr = Request.find_by_nr(name_request.nrNum)
                # Map applicants from the request data to the name request
                # applicants = map_request_applicants(request_data, nr_id)
                # nr.applicants = applicants
                # nr.save_to_db()
                pass
            except Exception as err:
                return handle_exception(err, 'Error saving request applicants.', 500)

        if name_request.stateCd in [State.DRAFT, State.COND_RESERVE, State.RESERVED]:
            name_request.stateCd = State.APPROVED

        self.save_request(name_request, on_success)

        try:
            updated_nr = Request.find_by_nr(name_request.nrNum)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the New NR from the db.', 500)

        # self.create_or_update_names(updated_nr)
        self.update_solr_doc(updated_nr, name_request)

        current_app.logger.debug(name_request.json())
        return jsonify(name_request.json()), 200
