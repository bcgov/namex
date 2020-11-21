from namex.utils.logging import setup_logging

from namex.models import State

from .abstract_nro_resource import AbstractNROResource
from .abstract_solr_resource import AbstractSolrResource

setup_logging()  # Important to do this first


class AbstractNameRequestResource(AbstractNROResource, AbstractSolrResource):
    _request_data = None
    _nr_action = None

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

    """
    These Event callback 'actions' are fired off when Name Request state change is triggered.
    Generally, these just invoke the @static methods post_nr, put_nr, patch_nr, and approve_nr.
    This makes testing those easier as we can call them statically from our tests without having to 
    instantiate a NameRequestResource.
    """

    def handle_nr_create(self, nr, svc):
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
        return self.patch_nr(nr, svc, self.nr_action, self.request_data)

    def handle_nr_approve(self, nr, svc):
        """
        This method is for updating certain parts of the name request eg. its STATE when a payment token is present in the request.
        By default just call the inherited approve_nr method.
        :param nr:
        :param svc:
        :return:
        """
        return self.approve_nr(nr, svc)

    @staticmethod
    def post_nr(nr, svc):
        """
        Just a placeholder, implement the logic in the inheriting class.
        :param nr:
        :param svc:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def put_nr(nr, svc):
        """
        Just a placeholder, implement the logic in the inheriting class.
        :param nr:
        :param svc:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def patch_nr(nr, svc, nr_action, request_data):
        """
        Just a placeholder, implement the logic in the inheriting class.
        :param nr:
        :param svc:
        :param nr_action:
        :param request_data:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def approve_nr(nr, svc):
        """
        This method is for updating the name request when an active payment exists on the NR.
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
    def save_nr(nr, svc):
        """
        Just save. Nothing else to do here.
        :param nr:
        :param svc:
        :return:
        """
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr

    def add_records_to_network_services(self, nr_model, update_solr=False):
        temp_nr_num = None
        if nr_model.stateCd in [State.DRAFT, State.COND_RESERVE, State.RESERVED, State.CONDITIONAL, State.APPROVED]:
            existing_nr_num = nr_model.nrNum
            # This updates NRO, it should return the nr_model with the updated nrNum, which we save back to postgres in the save_nr handler
            print('Adding request to NRO')
            nr_model = self.add_request_to_nro(nr_model, self.save_nr)
            print('NR is using the temporary NR Number {num}'.format(num=nr_model.nrNum))

            # Set the temp NR number if its different
            if nr_model.nrNum != existing_nr_num:
                temp_nr_num = existing_nr_num
                print('Replacing temporary NR Number {temp} -> {new}'.format(temp=temp_nr_num, new=nr_model.nrNum))

            print(repr(nr_model))

        # Update SOLR
        if update_solr:
            self.update_solr_service(nr_model, temp_nr_num)

        return nr_model

    def update_records_in_network_services(self, nr_model, update_solr=False):
        temp_nr_num = None
        if nr_model.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED, State.CANCELLED]:
            existing_nr_num = nr_model.nrNum
            # This updates NRO, it should return the nr_model with the updated nrNum, which we save back to postgres in the save_nr handler
            print('Updating request in NRO')
            nr_model = self.update_request_in_nro(nr_model, self.save_nr)

            # Set the temp NR number if its different
            if nr_model.nrNum != existing_nr_num:
                temp_nr_num = existing_nr_num
                print('Replacing temporary NR Number {temp} -> {new}'.format(temp=temp_nr_num, new=nr_model.nrNum))

            print(repr(nr_model))

            # Update SOLR
            if update_solr:
                self.update_solr_service(nr_model, temp_nr_num)

        return nr_model

    @staticmethod
    def log_error(msg, err):
        return msg.format(err)
