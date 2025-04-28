from typing import Callable

from flask import current_app

from namex.models import Request, State
from namex.services.name_request import NameRequestService
from namex.services.name_request.exceptions import NameRequestException
from namex.services.name_request.generate_new_nr_number import NRNumberService
from namex.services.name_request.utils import is_temp_nr_num
from namex.services.virtual_word_condition import VirtualWordConditionService

from .abstract_solr_resource import AbstractSolrResource


class AbstractNameRequestResource(AbstractSolrResource):
    _request_data = None
    _nr_action = None
    _nr_service = None

    @property
    def request_data(self):
        return self._request_data

    @request_data.setter
    def request_data(self, data):
        self._request_data = data

    @property
    def nr_action(self):
        return self._nr_action

    @nr_action.setter
    def nr_action(self, nr_action):
        self._nr_action = nr_action

    @property
    def nr_service(self):
        try:
            if not self._nr_service:
                self._nr_service = NameRequestService()
                self._nr_service.virtual_wc_service = VirtualWordConditionService()
        except Exception as err:
            raise NameRequestException(err, message='Error initializing NameRequestService')

        return self._nr_service

    def update_nr(self, nr_model: Request, new_state, on_state_changed: Callable) -> Request:
        """
        Call this method in inheriting classes to update an NR (Request).
        :param nr_model:
        :param new_state:
        :param on_state_changed: A handler function to be executed after completing the state change
        :return:
        """
        nr_svc = self.nr_service

        # Use apply_state_change to change state, as it enforces the State change pattern
        # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
        if new_state in State.VALID_STATES:
            nr_model = nr_svc.apply_state_change(nr_model, new_state, on_state_changed)

        return nr_model

    """
    These Event callback 'actions' are fired off when Name Request state change is triggered.
    Generally, these just invoke the @static methods post_nr, put_nr, patch_nr, and approve_nr.
    This makes testing those easier as we can call them statically from our tests without having to
    instantiate a NameRequestResource.
    """

    def handle_nr_create(self, nr: Request, svc) -> Request:
        """
        All logic for creating the name request goes inside this handler, which is invoked on successful state change.
        By default just call the inherited post_nr method.
        :param nr: The name request model
        :param svc A NameRequestService instance
        """
        return self.post_nr(nr, svc)

    def handle_nr_update(self, nr: Request, svc) -> Request:
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        By default just call the inherited put_nr method.
        :param nr: The name request model
        :param svc A NameRequestService instance
        :return:
        """
        return self.put_nr(nr, svc)

    def handle_nr_patch(self, nr: Request, svc) -> Request:
        """
        Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
        By default just call the inherited patch_nr method.
        :param nr: The name request model
        :param svc A NameRequestService instance
        :return:
        """
        return self.patch_nr(nr, svc, self.nr_action, self.request_data)

    def handle_nr_approve(self, nr, svc) -> Request:
        """
        This method is for updating certain parts of the name request eg. its STATE when a payment token is present in the request.
        By default just call the inherited approve_nr method.
        :param nr:
        :param svc:
        :return:
        """
        return self.approve_nr(nr, svc)

    @staticmethod
    def post_nr(nr: Request, svc) -> Request:
        """
        Just a default / placeholder, implement the logic in the inheriting class.
        :param nr:
        :param svc:
        :return:
        """
        return nr

    @staticmethod
    def put_nr(nr: Request, svc) -> Request:
        """
        Just a default / placeholder, implement the logic in the inheriting class.
        :param nr:
        :param svc:
        :return:
        """
        return nr

    @staticmethod
    def patch_nr(nr: Request, svc, nr_action, request_data) -> Request:
        """
        Just a default / placeholder, implement the logic in the inheriting class.
        :param nr:
        :param svc:
        :param nr_action:
        :param request_data:
        :return:
        """
        return nr

    @staticmethod
    def approve_nr(nr: Request, svc) -> Request:
        """
        This method is for updating the name request when an active payment exists on the NR.
        Just a default / placeholder, implement the logic in the inheriting class.
        :param nr:
        :param svc:
        :return:
        """
        return nr

    @staticmethod
    def save_nr(nr: Request, svc) -> Request:
        """
        Just save. Nothing else to do here.
        :param nr:
        :param svc:
        :return:
        """
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr

    def add_new_nr_number(self, nr_model: Request, update_solr=False) -> Request:
        is_temp_nr = is_temp_nr_num(nr_model.nrNum)
        temp_nr_num = None

        if (
            nr_model.stateCd
            in [
                State.PENDING_PAYMENT,
                State.DRAFT,
                State.COND_RESERVE,
                State.RESERVED,
                State.CONDITIONAL,
                State.APPROVED,
            ]
            and is_temp_nr
        ):
            temp_nr_num = nr_model.nrNum

            nr_num = NRNumberService.get_new_nr_num()
            nr_model.nrNum = nr_num
            current_app.logger.debug('NR is using the temporary NR Number {num}'.format(num=nr_num))

            # Set the temp NR number if its different
            current_app.logger.debug(
                'Replacing temporary NR Number {temp} -> {new}'.format(temp=temp_nr_num, new=nr_model.nrNum)
            )

            current_app.logger.debug(repr(nr_model))

        # Update SOLR
        if update_solr:
            self.update_solr_service(nr_model, temp_nr_num)

        return nr_model

    def update_solr(self, nr_model: Request) -> Request:
        # List of states that require SOLR update
        states_to_update = [
            State.PENDING_PAYMENT,
            State.DRAFT,
            State.CONDITIONAL,
            State.APPROVED,
            State.CANCELLED,
            State.INPROGRESS,
        ]

        # Check if the current state of the request is in the list of states to update
        if nr_model.stateCd in states_to_update:
            self.update_solr_service(nr_model)

        return nr_model

    @staticmethod
    def log_error(msg, err):
        return msg.format(err)
