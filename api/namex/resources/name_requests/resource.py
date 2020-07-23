import pysolr

from flask import request, current_app
from flask_restplus import Resource

from namex.utils.logging import setup_logging

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
        self._validate_config(current_app)

        # Store a copy of the request data to our class instance
        self.request_data = request.get_json()

        if not self.request_data:
            self.log_error('Error getting json input.', None)
            raise InvalidInputError()

        # Set the request data to the service
        self.nr_service.request_data = self.request_data

    @classmethod
    def _validate_config(cls, app):
        app_config = app.config.get('SOLR_SYNONYMS_API_URL', None)
        if not app_config:
            cls.log_error('ENV is not set', None)
            raise NameRequestException(message='Internal server error')

        test_env = 'prod'
        if test_env in app_config:
            return NotImplementedError()

    def save_request_to_nro(self, name_request, on_success=None):
        # Only update Oracle for APPROVED, CONDITIONAL, DRAFT
        if name_request.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED]:
            # TODO: Re-enable NRO update, might be a good idea to set an env var for this...
            warnings = self.nro_service.add_nr(name_request)
            if warnings:
                MessageServices.add_message(MessageServices.ERROR, 'add_request_in_NRO', warnings)
                raise NROUpdateError()
            else:
                # Execute the callback handler
                if on_success:
                    return on_success(name_request, self.nr_service)
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

    def update_network_services(self, nr_model):
        nr_svc = self.nr_service

        temp_nr_num = None
        # Save the request to NRO and back to postgres ONLY if the state is DRAFT, CONDITIONAL, or APPROVED
        # this is after fees are accepted
        if nr_model.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED]:
            existing_nr_num = nr_model.nrNum
            # This updates NRO, it should return the nr_model with the updated nrNum, which we save back to postgres in the on_nro_save_success handler
            nr_model = self.save_request_to_nro(nr_model, self.on_nro_save_success)
            # Set the temp NR number if its different
            if nr_model.nrNum != existing_nr_num:
                temp_nr_num = existing_nr_num

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PUT, nr_model, nr_svc.request_data)

        # Update SOLR
        if nr_model.stateCd in [State.COND_RESERVE, State.RESERVED, State.CONDITIONAL, State.APPROVED]:
            self.create_solr_nr_doc(SOLR_CORE, nr_model)
            if temp_nr_num:
                # This performs a safe delete, we check to see if the temp ID exists before deleting
                self.delete_solr_doc(SOLR_CORE, temp_nr_num)

    @staticmethod
    def log_error(msg, err):
        return msg.format(err)
