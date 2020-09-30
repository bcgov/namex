from namex.utils.logging import setup_logging

from namex.models import State

from .abstract_nro_resource import AbstractNROResource
from .abstract_solr_resource import AbstractSolrResource

setup_logging()  # Important to do this first


class AbstractNameRequestResource(AbstractNROResource, AbstractSolrResource):
    def add_records_to_network_services(self, nr_model, update_solr=False):
        if nr_model.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED]:
            # This updates NRO, it should return the nr_model with the updated nrNum, which we save back to postgres in the on_nro_save_success handler
            print('Adding request to NRO')
            nr_model = self.add_request_to_nro(nr_model, self.on_nro_save_success)
            print('NR is using the temporary NR Number {num}'.format(num=nr_model.nrNum))

            print(repr(nr_model))

        # Update SOLR
        if update_solr:
            self.update_solr_service(nr_model)

        return nr_model

    def update_records_in_network_services(self, nr_model, update_solr=False):
        temp_nr_num = None
        if nr_model.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED, State.CANCELLED]:
            existing_nr_num = nr_model.nrNum
            # This updates NRO, it should return the nr_model with the updated nrNum, which we save back to postgres in the on_nro_save_success handler
            print('Updating request in NRO')
            nr_model = self.update_request_in_nro(nr_model, self.on_nro_save_success)

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
    def on_nro_save_success(nr, svc):
        """
        Just save. Nothing else to do here.
        :param nr:
        :param svc:
        :return:
        """
        return nr

    @staticmethod
    def on_nr_approved(nr, svc):
        """
        This method is for updating certain parts of the name request eg. its STATE when an active payment exists on the NR.
        :param nr:
        :param svc:
        :return:
        """
        return nr

    def handle_nr_approval(self, nr, svc):
        """
        This method is for updating certain parts of the name request eg. its STATE when a payment token is present in the request.
        By default just call the inherited on_nr_approved method.
        :param nr:
        :param svc:
        :return:
        """
        return self.on_nr_approved(nr, svc)

    @staticmethod
    def log_error(msg, err):
        return msg.format(err)
