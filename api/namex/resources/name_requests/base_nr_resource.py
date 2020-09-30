from flask import request, current_app

from namex.utils.logging import setup_logging

from namex.models import State

from namex.services.name_request import NameRequestService
from namex.services.name_request.exceptions import NameRequestException

from .abstract_nr_resource import AbstractNameRequestResource

setup_logging()  # Important to do this first


class BaseNameRequestResource(AbstractNameRequestResource):
    """
    Just a base class for NameRequest Resource so we have somewhere to put our common logic.
    Inherits from AbstractNROResource and AbstractSolrResource which extend this class with
    functionality to communicate with NRO services and Solr.
    """
    _nr_service = None
    _request_data = None

    @property
    def nr_service(self):
        try:
            if not self._nr_service:
                self._nr_service = NameRequestService()
        except Exception as err:
            raise NameRequestException(err, message='Error initializing NameRequestService')

        return self._nr_service

    @property
    def request_data(self):
        return self._request_data

    @request_data.setter
    def request_data(self, data):
        self._request_data = data

    def initialize(self):
        self.validate_config(current_app)

        # Store a copy of the request data to our class instance
        request_json = request.get_json()
        self.request_data = request_json if request_json else {}

        # if not self.request_data:
        #    self.log_error('Error getting json input.', None)
        #    raise InvalidInputError()

        # Set the request data to the service
        self.nr_service.request_data = self.request_data

    @classmethod
    def validate_config(cls, app):
        app_config = app.config.get('DB_HOST', None)
        if not app_config:
            cls.log_error('ENV is not set', None)
            raise NameRequestException(message='Internal server error')

        test_env = 'prod'
        if test_env in app_config:
            raise NameRequestException(message='Not Implemented')

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
        # Update the submit count to 1
        nr = svc.update_request_submit_count(nr)
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
        map_draft_attrs = nr.stateCd == State.DRAFT
        nr = svc.map_request_data(nr, map_draft_attrs)
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
        # Map data from request_data to the name request
        map_draft_attrs = nr.stateCd == State.DRAFT
        nr = svc.map_request_data(nr, map_draft_attrs)
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
        This method is for updating certain parts of the name request eg. its STATE when an active payment exists on the NR.
        :param nr:
        :param svc:
        :return:
        """
        # Update the names, we can ignore everything else as this is only
        # invoked when we're completing a payment
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

    @staticmethod
    def log_error(msg, err):
        return msg.format(err)
