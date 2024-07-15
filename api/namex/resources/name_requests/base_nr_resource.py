from flask import current_app, request

from namex.constants import NameRequestPatchActions
from namex.models import Request, State
from namex.services.name_request.exceptions import NameRequestException
from namex.services.name_request.name_request import NameRequestService
from namex.utils.logging import setup_logging

from .abstract_nr_resource import AbstractNameRequestResource
from .constants import contact_editable_states, request_editable_states

setup_logging()  # Important to do this first


class BaseNameRequestResource(AbstractNameRequestResource):
    """
    Just a base class for NameRequest Resource so we have somewhere to put our common logic.
    Inherits from AbstractNROResource and AbstractSolrResource which extend this class with
    functionality to communicate with NRO services and Solr.
    """
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

    """
    The actual methods that map the request data to our domain models and persist the data.
    These are implemented statically so we can call them statically from our tests without having to instantiate a NameRequestResource.
    """

    @staticmethod
    def post_nr(nr: Request, svc: NameRequestService) -> Request:
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
    def put_nr(nr: Request, svc: NameRequestService) -> Request:
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        All request data is mapped.
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
    def patch_nr(nr: Request, svc: NameRequestService, nr_action, request_data: dict) -> Request:
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        Re-map the names and the applicants (just the applicant / contact if applicable).
        :param nr: The name request model
        :param svc A NameRequestService instance
        :param nr_action: The Name Request action
        :param request_data: A request data object
        :return:
        """
        lock_actions = [NameRequestPatchActions.CHECKIN.value, NameRequestPatchActions.CHECKOUT.value]

        if nr_action in lock_actions and nr.stateCd in [State.DRAFT, State.INPROGRESS]:
            # Map the checkout data
            nr.checkedOutBy = request_data.get('checkedOutBy', None)
            nr.checkedOutDt = request_data.get('checkedOutDt', None)

            nr = svc.save_request(nr)
            # Return the updated name request
            return nr

        if nr.stateCd in request_editable_states:
            # Map data from request_data to the name request
            map_draft_attrs = nr.stateCd == State.DRAFT
            nr = svc.map_request_data(nr, map_draft_attrs)

            # Map any submitted names from request_data to the name request
            nr = svc.map_request_names(nr)

        if nr.stateCd in contact_editable_states:
            # Map applicants from request_data to the name request
            nr = svc.map_request_applicants(nr)

        # Save
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr
