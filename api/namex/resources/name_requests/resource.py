import pysolr

from flask import request, current_app
from flask_restplus import Resource

from namex.utils.logging import setup_logging

from namex.constants import NROChangeFlags
from namex.models import Event, State

from namex.services import EventRecorder, MessageServices
from namex.services.virtual_word_condition import VirtualWordConditionService
from namex.services.name_request import NameRequestService
from namex.services.name_request.exceptions import \
    NameRequestException, InvalidInputError, VirtualWordConditionServiceError, NROUpdateError, SolrUpdateError

from namex import nro

from .configuration import SOLR_CORE, SOLR_API_URL

setup_logging()  # Important to do this first


class NameRequestResource(Resource):
    """
    Just a base class for NameRequest Resource so we have somewhere to put our common logic.
    """
    _nro_service = nro
    _nr_service = None
    _virtual_wc_service = None
    _request_data = None

    @property
    def nro_service(self):
        try:
            if not self._nro_service:
                self._nro_service = nro
        except Exception as err:
            raise NameRequestException(err, message='Error initializing NROService')

        return self._nro_service

    @property
    def nr_service(self):
        try:
            if not self._nr_service:
                self._nr_service = NameRequestService()
        except Exception as err:
            raise NameRequestException(err, message='Error initializing NameRequestService')

        return self._nr_service

    @property
    def virtual_wc_service(self):
        try:
            if not self._virtual_wc_service:
                self._virtual_wc_service = VirtualWordConditionService()
        except Exception as err:
            raise VirtualWordConditionServiceError()

        return self._virtual_wc_service

    @property
    def request_data(self):
        return self._request_data

    @request_data.setter
    def request_data(self, data):
        self._request_data = data

    def initialize(self):
        self.validate_config(current_app)

        # Store a copy of the request data to our class instance
        self.request_data = request.get_json()

        if not self.request_data:
            self.log_error('Error getting json input.', None)
            raise InvalidInputError()

        # Set the request data to the service
        self.nr_service.request_data = self.request_data

    @classmethod
    def validate_config(cls, app):
        app_config = app.config.get('SOLR_SYNONYMS_API_URL', None)
        if not app_config:
            cls.log_error('ENV is not set', None)
            raise NameRequestException(message='Internal server error')

        test_env = 'prod'
        if test_env in app_config:
            return NotImplementedError()

    """
    These Event callback 'actions' are fired off when Name Request state change is triggered.
    Generally, these just invoke the @static methods post_nr, put_nr, patch_nr, and on_nr_approved.
    This makes testing those easier as we can call them statically from our tests without having to 
    instantiate a NameRequestResource.
    """

    def handle_nr_creation(self, nr, svc):
        """
        All logic for creating the name request goes inside this handler, which is invoked on successful state change.
        By default just call the inherited post_nr method.
        :param nr: The name request model
        :param svc A NameRequestService instance
        """
        return self.post_nr(nr, svc)

    def handle_nr_update(self, nr, svc):
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        By default just call the inherited put_nr method.
        :param nr: The name request model
        :param svc A NameRequestService instance
        :return:
        """
        return self.put_nr(nr, svc)

    def handle_nr_patch(self, nr, svc):
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        By default just call the inherited patch_nr method.
        :param nr: The name request model
        :param svc A NameRequestService instance
        :return:
        """
        request_data = self.request_data  # Valid request data

        return self.patch_nr(nr, request_data, svc)

    def handle_nr_approval(self, nr, svc):
        """
        This method is for updating certain parts of the name request eg. its STATE when a payment token is present in the request.
        By default just call the inherited on_nr_approved method.
        :param nr:
        :param svc:
        :return:
        """
        return self.on_nr_approved(nr, svc)

    """
    The actual methods that map the request data to our domain models and persist the data.
    These are implemented statically so we can call them statically from our tests without having to 
    instantiate a NameRequestResource.
    """

    @staticmethod
    def post_nr(nr, svc):
        """
        All logic for creating the name request goes inside this handler, which is invoked on successful state change.
        By default just call the inherited post_nr method.
        :param nr: The name request model
        :param svc A NameRequestService instance
        """
        # Map the request data and save so we have a name request ID to use for collection ops
        nr = svc.map_request_data(nr, True)  # Set map_draft_attrs to True
        nr = svc.save_request(nr)
        # Map applicants from the request data to the name request
        nr = svc.map_request_applicants(nr)
        # Map any submitted names from the request data to the name request
        nr = svc.map_request_names(nr)
        # Save
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr

    @staticmethod
    def put_nr(nr, svc):
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        :param nr: The name request model
        :param svc A NameRequestService instance
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

    @staticmethod
    def patch_nr(nr, request_data, svc):
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        :param request_data: A request data object
        :param nr: The name request model
        :param svc A NameRequestService instance
        :return:
        """

        # cleared = request_data.get('cleared', [])  # Clear first
        # changed = request_data.get('changed', [])  # Then process changes

        # TODO: This needs more work (in progress)
        # if cleared:
        # nr = svc.map_request_data(nr, False)

        # is_changed = len(changed) > 0
        # has_applicants = changed.get('applicants', None)
        # has_names = changed.get('names', None)

        # if is_changed:
        # Map data from request_data to the name request
        nr = svc.map_request_data(nr, False)
        # if has_applicants:
        # Map applicants from request_data to the name request
        nr = svc.map_request_applicants(nr)
        # if has_names:
        # Map any submitted names from request_data to the name request
        nr = svc.map_request_names(nr)
        # Save
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr

    @staticmethod
    def on_nr_approved(nr, svc):
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

    def on_nro_update_complete(self, name_request, on_success, warnings, is_new_record=False):
        if warnings:
            code = 'add_request_in_NRO' if is_new_record else 'update_request_in_NRO'
            MessageServices.add_message(MessageServices.ERROR, code, warnings)
            raise NROUpdateError()
        else:
            return self.on_nro_update_success(name_request, on_success)

    def on_nro_update_success(self, name_request, on_success):
        if on_success:
            return on_success(name_request, self.nr_service)

    def add_request_to_nro(self, name_request, on_success=None):
        # Only update Oracle for APPROVED, CONDITIONAL, DRAFT
        if name_request.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED]:
            # TODO: It might be a good idea to set an env var for this...
            # nro_warnings = None
            nro_warnings = self.nro_service.add_nr(name_request)
            return self.on_nro_update_complete(name_request, on_success, nro_warnings, True)
        else:
            raise NameRequestException(message='Invalid state exception')

    def update_request_in_nro(self, name_request, on_success=None):
        # Only update Oracle for DRAFT
        # NRO / Oracle records are added when CONDITIONAL or APPROVED (see add_request_to_nro)
        if name_request.stateCd in [State.DRAFT]:
            # TODO: It might be a good idea to set an env var for this...
            # nro_warnings = None
            nro_warnings = self.nro_service.change_nr(name_request, {
                NROChangeFlags.REQUEST.value: True,
                NROChangeFlags.PREV_REQ.value: False,
                NROChangeFlags.APPLICANT.value: True,
                NROChangeFlags.ADDRESS.value: True,
                NROChangeFlags.NAME_1.value: True,
                NROChangeFlags.NAME_2.value: True,
                NROChangeFlags.NAME_3.value: True,
                # NROChangeFlags.NWPTA_AB.value: False,
                # NROChangeFlags.NWPTA_SK.value: False,
                # NROChangeFlags.CONSENT.value: False,
                NROChangeFlags.STATE.value: False
            })

            return self.on_nro_update_complete(name_request, on_success, nro_warnings)
        # Handle any changes where ONLY state is changed
        elif name_request.stateCd in [State.CANCELLED]:
            # TODO: It might be a good idea to set an env var for this...
            nro_warnings = self.nro_service.change_nr(name_request, {
                NROChangeFlags.STATE.value: True
            })

            return self.on_nro_update_complete(name_request, on_success, nro_warnings)
        else:
            raise NameRequestException(message='Invalid state exception')

    def create_solr_nr_doc(self, solr_core, name_request):
        try:
            # Create a new solr doc
            solr_name = name_request.names[0].name
            solr_docs = []
            nr_doc = {
                'id': name_request.nrNum,
                'name': solr_name,
                'source': 'NR',
                'start_date': name_request.submittedDate.strftime('%Y-%m-%dT%H:%M:00Z')
            }

            solr_docs.append(nr_doc)
            self.add_solr_doc(solr_core, solr_docs)

        except Exception as err:
            raise SolrUpdateError(err)

    @classmethod
    def add_solr_doc(cls, solr_core, solr_docs):
        try:
            solr = pysolr.Solr(SOLR_API_URL + solr_core + '/', timeout=10)
            result = solr.add(solr_docs, commit=True)
        except Exception as err:
            raise SolrUpdateError(err)

        return result

    @classmethod
    def delete_solr_doc(cls, solr_core, doc_id):
        try:
            solr = pysolr.Solr(SOLR_API_URL + solr_core + '/', timeout=10)
            result = solr.delete(id=doc_id, commit=True)

        except Exception as err:
            raise SolrUpdateError(err)

        return result

    def add_records_to_network_services(self, nr_model):
        nr_svc = self.nr_service

        temp_nr_num = None
        # Save the request to NRO and back to postgres ONLY if the state is DRAFT, CONDITIONAL, or APPROVED
        # this is after fees are accepted
        if nr_model.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED]:
            existing_nr_num = nr_model.nrNum
            # This updates NRO, it should return the nr_model with the updated nrNum, which we save back to postgres in the on_nro_save_success handler
            nr_model = self.add_request_to_nro(nr_model, self.on_nro_save_success)
            # Set the temp NR number if its different
            if nr_model.nrNum != existing_nr_num:
                temp_nr_num = existing_nr_num

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PUT, nr_model, nr_svc.request_data)

        # Update SOLR
        self.update_solr_service(nr_model, temp_nr_num)

    def update_records_in_network_services(self, nr_model):
        nr_svc = self.nr_service

        temp_nr_num = None
        # Save the request to NRO and back to postgres ONLY if the state is DRAFT, CONDITIONAL, or APPROVED
        # this is after fees are accepted
        if nr_model.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED, State.CANCELLED]:
            existing_nr_num = nr_model.nrNum
            # This updates NRO, it should return the nr_model with the updated nrNum, which we save back to postgres in the on_nro_save_success handler
            nr_model = self.update_request_in_nro(nr_model, self.on_nro_save_success)
            # Set the temp NR number if its different
            if nr_model.nrNum != existing_nr_num:
                temp_nr_num = existing_nr_num

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH, nr_model, nr_svc.request_data)

        # Update SOLR
        self.update_solr_service(nr_model, temp_nr_num)

    def update_solr_service(self, nr_model, temp_nr_num):
        if nr_model.stateCd in [State.COND_RESERVE, State.RESERVED, State.CONDITIONAL, State.APPROVED]:
            self.create_solr_nr_doc(SOLR_CORE, nr_model)
            if temp_nr_num:
                # This performs a safe delete, we check to see if the temp ID exists before deleting
                self.delete_solr_doc(SOLR_CORE, temp_nr_num)

    @staticmethod
    def log_error(msg, err):
        return msg.format(err)
