from flask import jsonify, current_app
from flask_restplus import cors

from namex.utils.logging import setup_logging
from namex.utils.util import cors_preflight

from namex.models import Request, State

from namex.services.name_request.utils import handle_exception
from namex.services.name_request.exceptions import \
    NameRequestException

from .api_namespace import api
from .api_models import nr_request
from .resource import NameRequestResource
from .utils import parse_nr_num

setup_logging()  # Important to do this first


@cors_preflight('GET, PUT, PATCH')
@api.route('/<string:nr_num>', strict_slashes=False, methods=['GET', 'PUT', 'PATCH', 'OPTIONS'])
class NameRequest(NameRequestResource):
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
        """
        Handles general update operations including update when a payment token is present.
        NOT used for updates that only change the Name Request state. Use 'patch' instead.

        State changes handled:
        - to DRAFT
        - to COND_RESERVE
        - to RESERVED
        - COND_RESERVE to CONDITIONAL
        - RESERVED to APPROVED

        :param nr_num:
        :return:
        """
        try:
            # Creates a new NameRequestService, validates the app config, and sets the request data to the NameRequestService instance
            self.initialize()
            nr_svc = self.nr_service

            # Find the existing name request
            nr_num = parse_nr_num(nr_num)
            nr_model = Request.find_by_nr(nr_num)
            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            # If no payment token just do a regular update...
            # This handles updates if the NR state is DRAFT, COND_RESERVE or RESERVED
            if nr_model.payment_token is None and nr_model.stateCd in [State.DRAFT, State.COND_RESERVE, State.RESERVED]:
                nr_model = self.update_nr(nr_model)
            elif nr_model.payment_token:
                # This handles updates if the NR state is COND_RESERVE or RESERVED and a payment token is present
                # If the state is COND_RESERVE update state to CONDITIONAL
                # If the state is RESERVED update state to APPROVED
                # Then update the name request as required
                nr_model = self.process_payment(nr_model)

            # This handles the updates for NRO and Solr, if necessary
            self.update_network_services(nr_model)

            current_app.logger.debug(nr_model.json())
            return jsonify(nr_model.json()), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)

    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def patch(self, nr_num):
        """
        Handles updates that ONLY involve Name Request state changes.
        NOT used for updates that change Name Request data. Use 'put' instead.

        We use this to:
        - Cancel an NR
        - Update the Payment

        State changes handled:
        - to CANCELLED
        - to INPROGRESS
        - to HOLD
        - to APPROVED
        - to REJECTED

        :param nr_num:
        :return:
        """
        try:
            # Creates a new NameRequestService, validates the app config, and sets the request data to the NameRequestService instance
            self.initialize()
            nr_svc = self.nr_service

            # Find the existing name request
            nr_num = parse_nr_num(nr_num)
            nr_model = Request.find_by_nr(nr_num)
            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            if nr_model.payment_token is not None:
                raise NameRequestException(message='Invalid request state for PATCH - payment token should not be present!')

            # This handles updates if the NR state is 'patchable'
            if nr_model.stateCd in [State.CANCELLED, State.INPROGRESS, State.HOLD, State.APPROVED, State.REJECTED]:
                nr_model = self.update_nr_state(nr_model, nr_model.stateCd)  # TODO: Pass state code in request

            # This handles the updates for NRO and Solr, if necessary
            self.update_network_services(nr_model)

            current_app.logger.debug(nr_model.json())
            return jsonify(nr_model.json()), 200

        except NameRequestException as err:
            return handle_exception(err, err.message, 500)

    def update_nr(self, nr_model):
        nr_svc = self.nr_service

        # Use apply_state_change to change state, as it enforces the State change pattern
        # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
        return nr_svc.apply_state_change(nr_model, nr_model.stateCd, self.handle_nr_update)

    def update_nr_state(self, nr_model, new_state):
        """
        State changes handled:
        - to CANCELLED
        - to INPROGRESS
        - to HOLD
        - to APPROVED
        - to REJECTED
        :param nr_model:
        :param new_state:
        :return:
        """
        nr_svc = self.nr_service

        # Use apply_state_change to change state, as it enforces the State change pattern
        # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
        if new_state in [State.CANCELLED, State.INPROGRESS, State.HOLD, State.APPROVED, State.REJECTED]:
            nr_model = nr_svc.apply_state_change(nr_model, new_state, self.on_nr_state_changed)

        return nr_model

    def process_payment(self, nr_model):
        nr_svc = self.nr_service

        # Use apply_state_change to change state, as it enforces the State change pattern
        # If the state is COND_RESERVE update state to CONDITIONAL, and update the name request as required
        if nr_model.payment_token and nr_model.stateCd == State.COND_RESERVE:
            # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
            nr_model = nr_svc.apply_state_change(nr_model, State.CONDITIONAL, self.handle_nr_approval)
            # If the state is RESERVED update state to APPROVED, and update the name request as required
        elif nr_model.payment_token and nr_model.stateCd == State.RESERVED:
            # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
            nr_model = nr_svc.apply_state_change(nr_model, State.APPROVED, self.handle_nr_approval)

        return nr_model

    """
    These Event callback 'actions' are fired off when Name Request state change is triggered.
    They are defined as static methods so we can easily test NameRequestService independently of this Resource (endpoint).
    """

    @staticmethod
    def handle_nr_update(nr, svc):
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        :param nr: The name request model
        :param svc A reference to the current Resource instance (this controller)
        :return:
        """
        nr = svc.map_request_data(nr, False)
        # Map applicants from the request data to the name request
        nr = svc.map_request_applicants(nr)
        # Map any submitted names from the request data to the name request
        nr = svc.map_request_names(nr)
        # Save
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr

    @staticmethod
    def on_nr_state_changed(nr, svc):
        """
        Just save. Nothing else to do here.
        :param nr: The name request model
        :param svc A reference to the current Resource instance (this controller)
        :return:
        """
        # Save
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr

    @staticmethod
    def handle_nr_approval(nr, svc):
        """
        This method is for updating certain parts of the name request eg. its STATE when a payment token is present in the request.
        :param nr:
        :param svc:
        :return:
        """
        # Update the names, we can ignore everything else as this is only
        # invoked when we're completing a payment.
        nr = svc.map_request_names(nr)
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr

    @staticmethod
    def on_nro_save_success(nr, svc):
        """
        Just save. Nothing else to do here.
        :param nr:
        :param svc:
        :return:
        """
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr
