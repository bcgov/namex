from flask import current_app, jsonify
from flask_restplus import cors
from datetime import datetime
from dateutil.relativedelta import relativedelta

from namex.utils.logging import setup_logging
from namex.utils.auth import cors_preflight
from namex.utils.api_resource import handle_exception

from namex.constants import NameRequestActions, NameRequestRollbackActions, RequestAction
from namex.models import Request, State, Event

from namex.services import EventRecorder
from namex.services.name_request.name_request_state import get_nr_state_actions
from namex.services.name_request.exceptions import \
    NameRequestException, InvalidInputError

from .api_namespace import api
from .api_models import nr_request
from .base_nr_resource import BaseNameRequestResource


setup_logging()  # Important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'
MSG_ERROR_CREATING_RESOURCE = 'Could not create / update resource'


@cors_preflight('GET, PUT')
@api.route('/<int:nr_id>', strict_slashes=False, methods=['GET', 'PUT', 'OPTIONS'])
@api.doc(params={
    'nr_id': 'NR ID - This field is required'
})
class NameRequestResource(BaseNameRequestResource):
    @cors.crossdomain(origin='*')
    def get(self, nr_id):
        try:
            nr_model = Request.query.get(nr_id)

            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = get_nr_state_actions(nr_model.stateCd, nr_model)
            return jsonify(response_data), 200
        except Exception as err:
            return handle_exception(err, 'Error retrieving the NR.', 500)

    # REST Method Handlers
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def put(self, nr_id):
        """
        NOT used for Existing Name Request updates that only change the Name Request. Use 'patch' instead.
        State changes handled include state changes to [DRAFT, COND_RESERVE, RESERVED, COND_RESERVE to CONDITIONAL, RESERVED to APPROVED]
        :param nr_id:
        :return:
        """
        try:
            # Find the existing name request
            nr_model = Request.query.get(nr_id)

            # Creates a new NameRequestService, validates the app config, and sets request_data to the NameRequestService instance
            self.initialize()
            nr_svc = self.nr_service

            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            valid_update_states = [State.DRAFT, State.COND_RESERVE, State.RESERVED]

            # This could be moved out, but it's fine here for now
            def validate_put_request(data):
                is_valid = False
                msg = ''
                if data.get('stateCd') in valid_update_states:
                    is_valid = True

                return is_valid, msg

            is_valid_put, validation_msg = validate_put_request(self.request_data)
            validation_msg = validation_msg if not len(validation_msg) > 0 else 'Invalid request for PUT'

            if not is_valid_put:
                raise InvalidInputError(message=validation_msg)

            if nr_model.stateCd in valid_update_states:
                nr_model = self.update_nr(nr_model)

            current_app.logger.debug(nr_model.json())
            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = nr_svc.current_state_actions
            return jsonify(response_data), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, repr(err), 500)

    def update_nr(self, nr_model):
        nr_svc = self.nr_service

        # Use apply_state_change to change state, as it enforces the State change pattern
        # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
        nr_model = nr_svc.apply_state_change(nr_model, nr_model.stateCd, self.handle_nr_update)

        # This handles the updates for NRO and Solr, if necessary
        update_solr = True
        self.add_records_to_network_services(nr_model, update_solr)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PUT, nr_model, nr_svc.request_data)

        return nr_model


@cors_preflight('PATCH')
@api.route('/<int:nr_id>/<string:nr_action>', strict_slashes=False, methods=['PATCH', 'OPTIONS'])
@api.doc(params={
    'nr_id': 'NR ID - This field is required',
    'nr_action': 'NR Action - One of [EDIT, UPGRADE, CANCEL, REFUND, REAPPLY, RESEND]'
})
class NameRequestFields(NameRequestResource):
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def patch(self, nr_id, nr_action):
        """
        Update a specific set of fields and/or a provided action. Fields excluded from the payload will not be updated.
        The following data format is expected when providing a data payload:
        { 'stateCd': 'CANCELLED' }  # Fields to update

        We use this to:
        - Edit a subset of NR fields
        - Cancel an NR
        - Change the state of an NR to [CANCELLED, INPROGRESS, HOLD, APPROVED, REJECTED
        - Apply the following actions to an NR [EDIT, UPGRADE, CANCEL, REFUND, REAPPLY, RESEND]
        :param nr_id:
        :param nr_action: One of [EDIT, UPGRADE, CANCEL, REFUND, REAPPLY, RESEND]
        :return:
        """
        try:
            # Find the existing name request
            nr_model = Request.query.get(nr_id)

            # Creates a new NameRequestService, validates the app config, and sets request_data to the NameRequestService instance
            self.initialize()
            nr_svc = self.nr_service

            nr_action = str(nr_action).upper()  # Convert to upper-case, just so we can support lower case action strings
            nr_action = NameRequestActions[nr_action].value \
                if NameRequestActions.has_value(nr_action) \
                else NameRequestActions.EDIT.value

            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            # Only allow editing if the request is in certain valid states
            request_editable_states = [
                State.DRAFT,
                State.RESERVED,
                State.COND_RESERVE
            ]

            contact_editable_states = [
                State.APPROVED,
                State.REJECTED,
                State.CONDITIONAL
            ]

            # This could be moved out, but it's fine here for now
            def validate_patch_request(data):
                # Use the NR model state as the default, as the state change may not be included in the PATCH request
                request_state = data.get('stateCd', nr_model.stateCd)
                is_valid = False
                msg = ''

                # Handles updates if the NR state is 'patchable'
                if request_state in request_editable_states:
                    is_valid = True
                elif request_state in contact_editable_states:
                    # Check expiry
                    if not nr_model.is_expired:
                        is_valid = True
                    else:
                        msg = 'Name Request PATCH is invalid - the Name Request is expired'
                else:
                    msg = 'Invalid state change requested - the Name Request state cannot be changed to [' + data.get('stateCd', '') + ']'

                return is_valid, msg

            is_valid_patch, validation_msg = validate_patch_request(self.request_data)
            validation_msg = validation_msg if not len(validation_msg) > 0 else 'Invalid request for PATCH'

            if not is_valid_patch:
                raise InvalidInputError(message=validation_msg)

            def handle_patch_actions(action, model):
                return {
                    NameRequestActions.EDIT.value: self.handle_patch_edit,
                    NameRequestActions.UPGRADE.value: self.handle_patch_upgrade,
                    NameRequestActions.CANCEL.value: self.handle_patch_cancel,
                    NameRequestActions.REFUND.value: self.handle_patch_refund,
                    # TODO: This is a frontend only action throw an error!
                    # NameRequestActions.RECEIPT.value: self.patch_receipt,
                    NameRequestActions.REAPPLY.value: self.handle_patch_reapply,
                    NameRequestActions.RESEND.value: self.handle_patch_resend
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
        except Exception as err:
            return handle_exception(err, repr(err), 500)

    def handle_patch_edit(self, nr_model):
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

        # This handles the updates for NRO and Solr, if necessary
        update_solr = True
        nr_model = self.update_records_in_network_services(nr_model, update_solr)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [edit]', nr_model, nr_svc.request_data)

        return nr_model

    def handle_patch_upgrade(self, nr_model):
        """
        Upgrade the Name Request to priority, create the payment and save the record.
        :param nr_model:
        :param payment_id:
        :return:
        """
        nr_svc = self.nr_service

        if not nr_model.stateCd == State.DRAFT:
            raise NameRequestException(message='Error upgrading Name Request, request is in an invalid state!')

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

        nr_model.priorityCd = 'Y'
        nr_model.priorityDate = datetime.utcnow()

        # Save the name request
        nr_model.save_to_db()

        # Update the actions, as things change once the payment is successful
        self.nr_service.current_state_actions = get_nr_state_actions(nr_model.stateCd, nr_model)
        # We have not accounted for multiple payments.
        # We will need to add a request_payment model (request_id and payment_id)
        # This handles the updates for NRO and Solr, if necessary
        update_solr = True
        nr_model = self.update_records_in_network_services(nr_model, update_solr)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [upgrade]', nr_model, nr_svc.request_data)

        return nr_model

    def handle_patch_reapply(self, nr_model):
        """
        Extend the Name Request's expiration date by 56 days. If the request action is set to REH or REST,
        extend the expiration by an additional year (plus the default 56 days).
        :param nr_model:
        :return:
        """
        nr_svc = self.nr_service

        if nr_model.submitCount < 3:
            if nr_model.request_action_cd in [RequestAction.REH.value, RequestAction.REN.value]:
                # If request action is REH or REST extend by 1 year (+ 56 default) days
                nr_model = nr_svc.extend_expiry_date(nr_model, (datetime.utcnow() + relativedelta(years=1,days=56)))
                nr_model = nr_svc.update_request_submit_count(nr_model)
            else:
                # Extend expiry date by (default) 56 days
                nr_model = nr_svc.extend_expiry_date(nr_model, datetime.utcnow())
                nr_model = nr_svc.update_request_submit_count(nr_model)

            # This handles updates if the NR state is 'patchable'
            nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

            # This handles the updates for NRO and Solr, if necessary
            update_solr = True
            nr_model = self.update_records_in_network_services(nr_model, update_solr)

            # Record the event
            EventRecorder.record(nr_svc.user, Event.PATCH + ' [re-apply]', nr_model, nr_svc.request_data)
        else:
            # TODO: Make a custom exception for this?
            raise NameRequestException(message='Submit count maximum of 3 retries has been reached!')

        return nr_model

    def handle_patch_resend(self, nr_model):
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

        # This handles the updates for NRO and Solr, if necessary
        update_solr = True
        nr_model = self.update_records_in_network_services(nr_model, update_solr)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [re-send]', nr_model, nr_svc.request_data)

        return nr_model

    def handle_patch_refund(self, nr_model):
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

        # This handles the updates for NRO and Solr, if necessary
        update_solr = True
        nr_model = self.update_records_in_network_services(nr_model, update_solr)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH, nr_model, nr_svc.request_data)

        return nr_model

    def handle_patch_cancel(self, nr_model):
        """
        Cancel the Name Request.
        :param nr_model:
        :return:
        """
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, State.CANCELLED)

        # This handles the updates for NRO and Solr, if necessary
        update_solr = True
        nr_model = self.update_records_in_network_services(nr_model, update_solr)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [cancel]', nr_model, nr_svc.request_data)

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


@cors_preflight('PATCH')
@api.route('/<int:nr_id>/rollback/<string:action>', strict_slashes=False, methods=['PATCH', 'OPTIONS'])
@api.doc(params={
    'nr_id': 'NR Number - This field is required',
})
class NameRequestRollback(NameRequestResource):
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def patch(self, nr_id, action):
        """
        Roll back a Name Request to a usable state in case of a frontend error.
        :param nr_id:
        :param action:
        :return:
        """
        try:
            # Find the existing name request
            nr_model = Request.query.get(nr_id)

            # Creates a new NameRequestService, validates the app config, and sets request_data to the NameRequestService instance
            self.initialize()
            nr_svc = self.nr_service

            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            # This could be moved out, but it's fine here for now
            def validate_patch_request(data):
                # TODO: Validate the data payload
                # Use the NR model state as the default, as the state change may not be included in the PATCH request
                is_valid = False
                msg = ''
                # This handles updates if the NR state is 'patchable'
                if NameRequestRollbackActions.has_value(action):
                    is_valid = True
                else:
                    msg = 'Invalid rollback action'

                return is_valid, msg

            is_valid_patch, validation_msg = validate_patch_request(self.request_data)
            validation_msg = validation_msg if not len(validation_msg) > 0 else 'Invalid request for PATCH'

            if not is_valid_patch:
                raise InvalidInputError(message=validation_msg)

            # This handles updates if the NR state is 'patchable'
            nr_model = self.handle_patch_rollback(nr_model, action)

            current_app.logger.debug(nr_model.json())
            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = nr_svc.current_state_actions
            return jsonify(response_data), 200

        except NameRequestException as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, repr(err), 500)

    def handle_patch_rollback(self, nr_model, action):
        """
        Roll back the Name Request.
        :param nr_model:
        :param action:
        :return:
        """
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, State.CANCELLED)

        # This handles the updates for NRO and Solr, if necessary
        self.update_records_in_network_services(nr_model)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH, nr_model, nr_svc.request_data)

        return nr_model

    def update_nr_fields(self, nr_model, new_state):
        """
        State changes handled:
        - to CANCELLED
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
