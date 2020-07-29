from flask import jsonify, request, current_app
from flask_restplus import cors
from datetime import datetime
from dateutil.relativedelta import relativedelta

from namex.utils.logging import setup_logging
from namex.utils.util import cors_preflight

from namex.constants import NameRequestActions
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


@cors_preflight('GET, PUT')
@api.route('/<string:nr_num>', strict_slashes=False, methods=['GET', 'PUT', 'OPTIONS'])
@api.doc(params={
    'nr_num': 'NR Number - This field is required'
})
class NameRequest(NameRequestResource):
    @cors.crossdomain(origin='*')
    def get(self, nr_num):
        try:
            nr_num = parse_nr_num(nr_num)
            nr_model = Request.find_by_nr(nr_num)

            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = get_nr_state_actions(nr_model.stateCd)
            return jsonify(response_data), 200
        except Exception as err:
            return handle_exception(err, 'Error retrieving the NR.', 500)

    # REST Method Handlers
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def put(self, nr_num):
        """
        Handles general update operations including update when a payment token is present.
        NOT used for updates that only change the Name Request state. Use 'patch' instead.

        State changes handled include state changes to [DRAFT, COND_RESERVE, RESERVED, COND_RESERVE to CONDITIONAL, RESERVED to APPROVED]
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
                if data.get('payment_token') or (data.get('payment_token') is None and data.get('stateCd') in valid_update_states):
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

    def update_nr(self, nr_model):
        nr_svc = self.nr_service

        # Use apply_state_change to change state, as it enforces the State change pattern
        # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
        return nr_svc.apply_state_change(nr_model, nr_model.stateCd, self.handle_nr_update)

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


@cors_preflight('PATCH')
@api.route('/<string:nr_num>/<string:nr_action>', strict_slashes=False, methods=['PATCH', 'OPTIONS'])
@api.doc(params={
    'nr_num': 'NR Number - This field is required',
    'nr_action': 'NR Action - One of [EDIT, UPGRADE, CANCEL, REFUND, REAPPLY, RESEND]'
})
class NameRequestFields(NameRequestResource):
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def patch(self, nr_num, nr_action):
        """
        Update a specific set of fields and/or a provided action. Fields excluded from the payload will not be updated.
        The following data format is expected when providing a data payload:
        { 'stateCd': 'CANCELLED' }  # Fields to update

        We use this to:
        - Edit a subset of NR fields
        - Cancel an NR
        - Change the state of an NR to [CANCELLED, INPROGRESS, HOLD, APPROVED, REJECTED
        - Apply the following actions to an NR [EDIT, UPGRADE, CANCEL, REFUND, REAPPLY, RESEND]
        :param nr_num:
        :param nr_action: One of [EDIT, UPGRADE, CANCEL, REFUND, REAPPLY, RESEND]
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
                self.nr_service.request_data = self.request_data

            initialize(self)

            nr_svc = self.nr_service

            # Find the existing name request
            nr_num = parse_nr_num(nr_num)
            nr_action = str(nr_action).upper()  # Convert to upper-case, just so we can support lower case action strings
            nr_action = NameRequestActions[nr_action].value \
                if NameRequestActions.has_value(nr_action) \
                else NameRequestActions.EDIT.value
            nr_model = Request.find_by_nr(nr_num)
            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            valid_states = State.VALID_STATES

            # This could be moved out, but it's fine here for now
            def validate_patch_request(data):
                # Use the NR model state as the default, as the state change may not be included in the PATCH request
                request_state = data.get('stateCd', nr_model.stateCd)
                is_valid = False
                msg = ''
                # This handles updates if the NR state is 'patchable'
                if request_state in valid_states:
                    # Get the SQL alchemy columns and associations
                    is_valid = True
                else:
                    msg = 'Invalid state change requested - the NR state cannot be changed to [' + data.get('stateCd', '') + ']'

                return is_valid, msg

            is_valid_patch, validation_msg = validate_patch_request(self.request_data)
            validation_msg = validation_msg if not len(validation_msg) > 0 else 'Invalid request for PATCH'

            if not is_valid_patch:
                raise InvalidInputError(message=validation_msg)

            # if nr_model.payment_token is not None:
            #    raise NameRequestException(message='Invalid request state for PATCH - payment token should not be present!')

            def handle_patch_actions(action, model):
                return {
                    NameRequestActions.EDIT: self.handle_patch_edit,
                    NameRequestActions.UPGRADE: self.handle_patch_upgrade,
                    NameRequestActions.CANCEL: self.handle_patch_cancel,
                    NameRequestActions.REFUND: self.handle_patch_refund,
                    # TODO: This is a frontend only action throw an error!
                    # NameRequestActions.RECEIPT: self.patch_receipt,
                    NameRequestActions.REAPPLY: self.patch_reapply,
                    NameRequestActions.RESEND: self.patch_resend
                }.get(action)(model)

            # This handles updates if the NR state is 'patchable'
            nr_model = handle_patch_actions(nr_action, nr_model)

            current_app.logger.debug(nr_model.json())
            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = nr_svc.current_state_actions
            return jsonify(response_data), 200

        except NameRequestException as err:
            return handle_exception(err, err.message, 500)

    def handle_patch_edit(self, nr_model):
        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

        # This handles the updates for NRO and Solr, if necessary
        # TODO: Do we update network services?
        self.update_network_services(nr_model)
        return nr_model

    def handle_patch_upgrade(self, nr_model):
        # TODO: Only works for DRAFT state

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

        # TODO: Update Oracle (change_nr?) and payment related stuff
        # This will generate a new payment Id and then the NR will have two payments.
        # We have not accounted for multiple payments.
        # We will need to add a request_payment model (request_id and payment_id)
        # This handles the updates for NRO and Solr, if necessary
        self.update_network_services(nr_model)
        return nr_model

    def handle_patch_cancel(self, nr_model):
        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, State.CANCELLED)

        # This handles the updates for NRO and Solr, if necessary
        # TODO: Do we update network services?
        self.update_network_services(nr_model)
        return nr_model

    def handle_patch_refund(self, nr_model):
        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

        # This handles the updates for NRO and Solr, if necessary
        # self.update_network_services(nr_model)
        return nr_model

    def handle_patch_reapply(self, nr_model):
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        # TODO: Ensure request action is REH or REST <- Where does this come in?
        # TODO: Ensure submit count is not greater than 3

        if nr_model.submitCount < 3:
            # Update submit count
            nr_model = nr_svc.update_request_submit_count(nr_model)
            # Extend expiry date by (default) 56 days
            nr_model = nr_svc.extend_expiry_date(nr_model)
            # TODO: If request action is REH or REST extend by 1 year (+ 56 default) days
            # TODO: Where does the request action come from in this scenario?
            # nr_model = nr_svc.extend_expiry_date(nr_model, (datetime.utcnow() + relativedelta(years=1)))

            nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

            # This handles the updates for NRO and Solr, if necessary
            # TODO: Do we update network services?
            self.update_network_services(nr_model)

            # TODO: Raise an error if submitCount is greater than 3
        return nr_model

    def handle_patch_resend(self, nr_model):
        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

        # This handles the updates for NRO and Solr, if necessary
        # TODO: Do we update network services?
        self.update_network_services(nr_model)
        return nr_model

    def update_nr_fields(self, nr_model, new_state):
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
        if new_state in State.VALID_STATES:
            nr_model = nr_svc.apply_state_change(nr_model, new_state, self.handle_nr_patch)

        return nr_model
