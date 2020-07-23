from flask import jsonify, request, current_app
from flask_restplus import cors

from namex.utils.logging import setup_logging
from namex.utils.util import cors_preflight

from namex.models import Request, State

from namex.services.name_request.utils import handle_exception
from namex.services.name_request.name_request_state import get_nr_state_actions
from namex.services.name_request.exceptions import \
    NameRequestException, InvalidInputError

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
            nr_model = Request.find_by_nr(nr_num)

            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = get_nr_state_actions(get_nr_state_actions(nr_model.stateCd))
            return jsonify(response_data), 200
        except Exception as err:
            return handle_exception(err, 'Error retrieving the NR from the db.', 500)

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
            # Creates a new NameRequestService, validates the app config, and sets request_data to the NameRequestService instance
            self.initialize()
            nr_svc = self.nr_service

            # Find the existing name request
            nr_num = parse_nr_num(nr_num)
            nr_model = Request.find_by_nr(nr_num)
            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            valid_update_states = [State.DRAFT, State.COND_RESERVE, State.RESERVED]

            # This could be moved out, but it's fine here for now
            def validate_put_request(data):
                is_valid = False
                msg = ''
                if data.payment_token or (data.payment_token is None and data.stateCd in valid_update_states):
                    is_valid = True

                return is_valid, msg

            is_valid_put, validation_msg = validate_put_request(self.request_data)
            validation_msg = validation_msg if not len(validation_msg) > 0 else 'Invalid request for PUT'

            if not is_valid_put:
                raise InvalidInputError(message=validation_msg)

            # This handles updates if the NR state is DRAFT, COND_RESERVE or RESERVED
            # If no payment token just do a regular update...
            if nr_model.stateCd in valid_update_states and nr_model.payment_token is None:
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
            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = nr_svc.current_state_actions
            return jsonify(response_data), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)

    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def patch(self, nr_num):
        """
        Update a specific set of fields. Fields excluded from the payload will not be updated.

        The following data format is expected eg. update State, and clear the field:
        payload = {
            changed: [{ field: 'stateCd', value: 'CANCELLED' }],  # Fields to update
            cleared: [{ field: 'hasBeenReset' }]  # Fields to clear (todo: implement this!)
        }


        This is mostly used for updates that ONLY involve Name Request state changes.
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
            # Creates a new NameRequestService, validates the app config, and sets request_data to the NameRequestService instance
            def initialize(resource):
                """
                Override the default initialization (instead of self.initialize())
                :return:
                """
                resource.validate_config(current_app)

                # Store a copy of request_data to our class instance
                resource.request_data = request.get_json()

                if not self.request_data:
                    self.log_error('Error getting json input.', None)
                    raise InvalidInputError()

                # Unlike the inherited initialize(), we don't want to set the NameRequestService's request_data just yet
                # This is a partial update operation and we will need to selectively map the request data over
                # -> self.nr_service.request_data = self.request_data

            initialize(self)

            nr_svc = self.nr_service

            # Find the existing name request
            nr_num = parse_nr_num(nr_num)
            nr_model = Request.find_by_nr(nr_num)
            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            valid_states = [State.CANCELLED, State.INPROGRESS, State.HOLD, State.APPROVED, State.REJECTED]

            # This could be moved out, but it's fine here for now
            def validate_patch_request(data):
                is_valid = False
                msg = ''
                # This handles updates if the NR state is 'patchable'
                if data.stateCd in valid_states:
                    # Get the SQL alchemy columns and associations
                    is_valid = True
                else:
                    msg = 'Invalid state change requested - the NR state cannot be changed to [' + data.stateCd + ']'

                return is_valid, msg

            is_valid_patch, validation_msg = validate_patch_request(self.request_data)
            validation_msg = validation_msg if not len(validation_msg) > 0 else 'Invalid request for PATCH'

            if not is_valid_patch:
                raise InvalidInputError(message=validation_msg)

            if nr_model.payment_token is not None:
                raise NameRequestException(message='Invalid request state for PATCH - payment token should not be present!')

            # This handles updates if the NR state is 'patchable'
            nr_model = self.update_nr_state(nr_model, nr_model.stateCd)  # TODO: Pass state code in request

            # This handles the updates for NRO and Solr, if necessary
            self.update_network_services(nr_model)

            current_app.logger.debug(nr_model.json())
            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = nr_svc.current_state_actions
            return jsonify(response_data), 200

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
            nr_model = nr_svc.apply_state_change(nr_model, new_state, self.handle_nr_patch)

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
    """

    def handle_nr_update(self, nr, svc):
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        :param nr: The name request model
        :param svc A reference to the current Resource instance (this controller)
        :return:
        """
        nr = svc.map_request_data(nr, False)
        # Map applicants from request_data to the name request
        nr = svc.map_request_applicants(nr)
        # Map any submitted names from request_data to the name request
        nr = svc.map_request_names(nr)
        # Save
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr

    def handle_nr_patch(self, nr, svc):
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        :param nr: The name request model
        :param svc A reference to the current Resource instance (this controller)
        :return:
        """

        request_data = self.request_data  # Valid request data

        cleared = request_data.get('cleared', [])  # Clear first
        changed = request_data.get('changed', [])  # Then process changes

        # TODO: This needs more work (in progress)
        if cleared:
            nr = svc.map_request_data(nr, False)

        is_changed = len(changed) > 0
        has_applicants = changed.get('applicants', None)
        has_names = changed.get('names', None)

        if is_changed:
            # Map data from request_data to the name request
            nr = svc.map_request_data(nr, False)
        if has_applicants:
            # Map applicants from request_data to the name request
            nr = svc.map_request_applicants(nr)
        if has_names:
            # Map any submitted names from request_data to the name request
            nr = svc.map_request_names(nr)
        # Save
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr

    def handle_nr_approval(self, nr, svc):
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

    def on_nro_save_success(self, nr, svc):
        """
        Just save. Nothing else to do here.
        :param nr:
        :param svc:
        :return:
        """
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr
