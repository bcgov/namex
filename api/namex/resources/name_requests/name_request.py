from uuid import uuid4
from datetime import datetime
from flask import current_app, request, jsonify
from flask_restx import cors

from namex.utils.logging import setup_logging
from namex.utils.auth import cors_preflight, full_access_to_name_request
from namex.utils.api_resource import handle_exception

from namex.constants import NameRequestPatchActions, NameRequestRollbackActions, PaymentState
from namex.models import Request, State, Event, User

from namex.services import EventRecorder
from namex.services.name_request.name_request_state import get_nr_state_actions
from namex.services.name_request.utils import get_mapped_entity_and_action_code, is_temp_nr_num
from namex.services.name_request.exceptions import \
    NameRequestException, InvalidInputError, NameRequestIsInProgressError
from namex.services.payment.payments import refund_payment
from namex.services.statistics.wait_time_statistics import WaitTimeStatsService

from .api_namespace import api
from .api_models import nr_request
from .base_nr_resource import BaseNameRequestResource
from .constants import request_editable_states, contact_editable_states

setup_logging()  # Important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'


@cors_preflight('GET, PUT')
@api.route('/<int:nr_id>', strict_slashes=False, methods=['GET', 'PUT', 'OPTIONS'])
@api.doc(params={
    'nr_id': 'NR ID - This field is required'
})
class NameRequestResource(BaseNameRequestResource):
    @cors.crossdomain(origin='*')
    def get(self, nr_id):

        return {"message": "Not Implemented"}, 503
        try:
            nr_model = Request.query.get(nr_id)

            if nr_model.requestTypeCd and (not nr_model.entity_type_cd or not nr_model.request_action_cd):
                # If requestTypeCd is set, but a request_entity (entity_type_cd) and a request_action (request_action_cd)
                # are not, use get_mapped_entity_and_action_code to map the values from the requestTypeCd
                entity_type, request_action = get_mapped_entity_and_action_code(nr_model.requestTypeCd)
                nr_model.entity_type_cd = entity_type
                nr_model.request_action_cd = request_action

            response_data = nr_model.json()

            # If draft, get the wait time and oldest queued request
            if nr_model.stateCd == 'DRAFT':

                service = WaitTimeStatsService()
                wait_time_response = service.get_waiting_time_dict()
                response_data.update(wait_time_response)

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
            if not full_access_to_name_request(request):
                return {"message": "You do not have access to this NameRequest."}, 403
            # Find the existing name request
            nr_model = Request.query.get(nr_id)

            # Creates a new NameRequestService, validates the app config, and sets request_data to the NameRequestService instance
            self.initialize()
            nr_svc = self.nr_service

            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            valid_update_states = [State.DRAFT, State.COND_RESERVE, State.RESERVED, State.PENDING_PAYMENT]

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
                nr_model = self.update_nr(nr_model, nr_model.stateCd, self.handle_nr_update)

                # Record the event
                EventRecorder.record(nr_svc.user, Event.PUT, nr_model, nr_svc.request_data)

            current_app.logger.debug(nr_model.json())
            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = nr_svc.current_state_actions
            return jsonify(response_data), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, repr(err), 500)


@cors_preflight('PATCH')
@api.route('/<int:nr_id>/<string:nr_action>', strict_slashes=False, methods=['PATCH', 'OPTIONS'])
@api.doc(params={
    'nr_id': 'NR ID - This field is required',
    'nr_action': 'NR Action - One of [CHECKOUT, CHECKIN, EDIT, CANCEL, RESEND, REQUEST_REFUND]'
})
class NameRequestFields(BaseNameRequestResource):
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def patch(self, nr_id, nr_action: str):
        """
        Update a specific set of fields and/or a provided action. Fields excluded from the payload will not be updated.
        The following data format is expected when providing a data payload:
        { 'stateCd': 'CANCELLED' }  # Fields to update

        We use this to:
        - Edit a subset of NR fields
        - Cancel an NR
        - Change the state of an NR
        :param nr_id:
        :param nr_action: One of [CHECKOUT, CHECKIN, EDIT, CANCEL, RESEND]
        :return:
        """
        try:
            if not full_access_to_name_request(request):
                return {"message": "You do not have access to this NameRequest."}, 403

            nr_action = str(nr_action).upper()  # Convert to upper-case, just so we can support lower case action strings
            nr_action = NameRequestPatchActions[nr_action].value \
                if NameRequestPatchActions.has_value(nr_action) \
                else NameRequestPatchActions.EDIT.value

            # Find the existing name request
            nr_model = Request.query.get(nr_id)

            def initialize(_self):
                _self.validate_config(current_app)
                request_json = request.get_json()

                if nr_action:
                    _self.nr_action = nr_action

                if nr_action is NameRequestPatchActions.CHECKOUT.value:
                    # Make sure the NR isn't already checked out
                    checked_out_by_different_user = nr_model.checkedOutBy is not None and nr_model.checkedOutBy != request_json.get('checkedOutBy', None)
                    if checked_out_by_different_user:
                        raise NameRequestIsInProgressError()

                    # set the user id of the request to name_request_service_account
                    service_account_user = User.find_by_username('name_request_service_account')
                    nr_model.userId = service_account_user.id

                    # The request payload will be empty when making this call, add them to the request
                    _self.request_data = {
                        # Doesn't have to be a UUID but this is easy and works for a pretty unique token
                        'checkedOutBy': str(uuid4()),
                        'checkedOutDt': datetime.now()
                    }
                    # Set the request data to the service
                    _self.nr_service.request_data = self.request_data
                elif nr_action is NameRequestPatchActions.CHECKIN.value:
                    # The request payload will be empty when making this call, add them to the request
                    _self.request_data = {
                        'checkedOutBy': None,
                        'checkedOutDt': None
                    }
                    # Set the request data to the service
                    _self.nr_service.request_data = self.request_data
                else:
                    super().initialize()

            initialize(self)

            nr_svc = self.nr_service
            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

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
                    is_valid = True
                else:
                    msg = 'Invalid state change requested - the Name Request state cannot be changed to [' + data.get('stateCd', '') + ']'

                # Check the action, make sure it's valid
                if not NameRequestPatchActions.has_value(nr_action):
                    is_valid = False
                    msg = 'Invalid Name Request PATCH action, please use one of [' + ', '.join([action.value for action in NameRequestPatchActions]) + ']'
                return is_valid, msg

            is_valid_patch, validation_msg = validate_patch_request(self.request_data)
            validation_msg = validation_msg if not len(validation_msg) > 0 else 'Invalid request for PATCH'

            if not is_valid_patch:
                raise InvalidInputError(message=validation_msg)

            def handle_patch_actions(action, model):
                return {
                    NameRequestPatchActions.CHECKOUT.value: self.handle_patch_checkout,
                    NameRequestPatchActions.CHECKIN.value: self.handle_patch_checkin,
                    NameRequestPatchActions.EDIT.value: self.handle_patch_edit,
                    NameRequestPatchActions.CANCEL.value: self.handle_patch_cancel,
                    NameRequestPatchActions.RESEND.value: self.handle_patch_resend,
                    NameRequestPatchActions.REQUEST_REFUND.value: self.handle_patch_request_refund
                }.get(action)(model)

            # This handles updates if the NR state is 'patchable'
            nr_model = handle_patch_actions(nr_action, nr_model)

            current_app.logger.debug(nr_model.json())
            response_data = nr_model.json()

            # Don't return the whole response object if we're checking in or checking out
            if nr_action == NameRequestPatchActions.CHECKOUT.value:
                response_data = {
                    'id': nr_id,
                    'checkedOutBy': response_data.get('checkedOutBy'),
                    'checkedOutDt': response_data.get('checkedOutDt'),
                    'state': response_data.get('state', ''),
                    'stateCd': response_data.get('stateCd', ''),
                    'actions': nr_svc.current_state_actions
                }
                return jsonify(response_data), 200

            if nr_action == NameRequestPatchActions.CHECKIN.value:
                response_data = {
                    'id': nr_id,
                    'state': response_data.get('state', ''),
                    'stateCd': response_data.get('stateCd', ''),
                    'actions': nr_svc.current_state_actions
                }
                return jsonify(response_data), 200

            # Add the list of valid Name Request actions for the given state to the response
            if (nr_action == NameRequestPatchActions.REQUEST_REFUND.value):
                response_data['actions'] = []
            else:
                response_data['actions'] = nr_svc.current_state_actions
            return jsonify(response_data), 200

        except NameRequestIsInProgressError as err:
            # Might as well use the Mozilla WebDAV HTTP Locked status, it's pretty close
            return handle_exception(err, err.message, 423)
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, repr(err), 500)

    def handle_patch_checkout(self, nr_model: Request):
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr(nr_model, State.INPROGRESS, self.handle_nr_patch)

        # Lock nro Request row (set status=H)
        nro_warnings = self.lock_request_in_nro(nr_model)
        if nro_warnings:
            on_success = False
            return self.on_nro_update_complete(nr_model, on_success, nro_warnings)

        EventRecorder.record(nr_svc.user, Event.PATCH + ' [checkout]', nr_model, {})
        return nr_model

    def handle_patch_checkin(self, nr_model: Request):
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr(nr_model, State.DRAFT, self.handle_nr_patch)

        # Set status back to D after edit is complete
        nro_warnings = self.unlock_request_in_nro(nr_model)
        if nro_warnings:
            on_success = False
            return self.on_nro_update_complete(nr_model, on_success, nro_warnings)
        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [checkin]', nr_model, {})

        return nr_model

    def handle_patch_edit(self, nr_model: Request):
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr(nr_model, nr_model.stateCd, self.handle_nr_patch)

        # This handles the updates for NRO and Solr, if necessary
        nr_model = self.update_records_in_network_services(nr_model, update_solr=False)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [edit]', nr_model, nr_svc.request_data)

        return nr_model

    def handle_patch_resend(self, nr_model: Request):
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr(nr_model, nr_model.stateCd, self.handle_nr_patch)

        # This handles the updates for NRO and Solr, if necessary
        nr_model = self.update_records_in_network_services(nr_model, update_solr=False)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [re-send]', nr_model, nr_svc.request_data)

        return nr_model

    def handle_patch_cancel(self, nr_model: Request):
        """
        Cancel the Name Request.
        :param nr_model:
        :return:
        """
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr(nr_model, State.CANCELLED, self.handle_nr_patch)

        # This handles the updates for NRO and Solr, if necessary
        nr_model = self.update_records_in_network_services(nr_model, update_solr=True)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [cancel]', nr_model, nr_svc.request_data)

        return nr_model

    def handle_patch_request_refund(self, nr_model: Request):
        """
        Can the NR and request a refund for ALL associated Name Request payments.
        :param nr_model:
        :return:
        """
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr(nr_model, State.REFUND_REQUESTED, self.handle_nr_patch)

        # Handle the payments
        valid_states = [
            PaymentState.COMPLETED.value,
            PaymentState.PARTIAL.value
        ]
        # Cancel any payments associated with the NR
        for payment in nr_model.payments.all():
            if payment.payment_status_code in valid_states:
                # refund_payment(payment.payment_token, {'reason': 'Name Request user requested refund'})
                refund_payment(payment.payment_token, {})
                payment.payment_status_code = PaymentState.REFUND_REQUESTED.value
                payment.save_to_db()

        # This handles the updates for NRO and Solr, if necessary
        nr_model = self.update_records_in_network_services(nr_model, update_solr=True)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [request-refund]', nr_model, nr_svc.request_data)

        return nr_model


@cors_preflight('PATCH')
@api.route('/<int:nr_id>/rollback/<string:action>', strict_slashes=False, methods=['PATCH', 'OPTIONS'])
@api.doc(params={
    'nr_id': 'NR Number - This field is required',
})
class NameRequestRollback(BaseNameRequestResource):
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
            if not full_access_to_name_request(request):
                return {"message": "You do not have access to this NameRequest."}, 403
                
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

    def handle_patch_rollback(self, nr_model: Request, action: str):
        """
        Roll back the Name Request.
        :param nr_model:
        :param action:
        :return:
        """
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr(nr_model, State.CANCELLED, self.handle_nr_patch)
        # Only update the record in NRO if it's a real NR, otherwise the record won't exist
        if not is_temp_nr_num(nr_model.nrNum):
            # This handles the updates for NRO and Solr, if necessary
            # self.update_records_in_network_services(nr_model, update_solr=True)
            nr_model = self.update_request_in_nro(nr_model, self.save_nr)

        # Delete in solr for temp or real NR because it is cancelled
        if nr_model.entity_type_cd in ['CR', 'UL', 'BC', 'CP', 'PA', 'XCR', 'XUL', 'XCP', 'CC', 'FI', 'XCR', 'XUL', 'XCP']:
            SOLR_CORE = 'possible.conflicts'
            self.delete_solr_doc(SOLR_CORE, nr_model.nrNum)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH, nr_model, nr_svc.request_data)

        return nr_model
