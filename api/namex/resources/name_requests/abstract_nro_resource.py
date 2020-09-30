from flask import current_app
from flask_restplus import Resource

from namex.utils.logging import setup_logging

from namex.constants import NROChangeFlags
from namex.models import State

from namex.services import MessageServices
from namex.services.name_request import NameRequestService
from namex.services.name_request.exceptions import NameRequestException, NROUpdateError

from namex import nro

setup_logging()  # Important to do this first


class AbstractNROResource(Resource):
    """
    Abstract class. Extended by AbstractNameRequestResource.
    Avoid using this class elsewhere, please use AbstractNameRequestResource instead.
    """
    _nro_service = nro
    _nr_service = None

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

    # TODO: Update this! Add in mocks...
    def add_request_to_nro(self, name_request, on_success=None):
        # Only update Oracle for APPROVED, CONDITIONAL, DRAFT
        if name_request.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED]:
            if current_app.config.get('DISABLE_NAMEREQUEST_NRO_UPDATES', 0) == 1:
                # Ignore update to NRO if NRO updates [DISABLE_NAMEREQUEST_NRO_UPDATES] are explicitly disabled in your .env
                nro_warnings = None
            else:
                nro_warnings = self.nro_service.add_nr(name_request)

            return self.on_nro_update_complete(name_request, on_success, nro_warnings, True)
        else:
            raise NameRequestException(message='Invalid state exception [' + name_request.stateCd + '], cannot add Name Request to NRO when Request state is NOT in DRAFT, CONDITIONAL or APPROVED')

    # TODO: Update this! Add in mocks...
    def update_request_in_nro(self, name_request, on_success=None):
        # Only update Oracle for DRAFT
        # NRO / Oracle records are added when CONDITIONAL or APPROVED (see add_request_to_nro)
        if name_request.stateCd in [State.DRAFT]:
            if current_app.config.get('DISABLE_NAMEREQUEST_NRO_UPDATES', 0) == 1:
                # Ignore update to NRO if NRO updates [DISABLE_NAMEREQUEST_NRO_UPDATES] are explicitly disabled in your .env
                nro_warnings = None
            else:
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
                    NROChangeFlags.CONSENT.value: False,
                    NROChangeFlags.STATE.value: False
                })

            return self.on_nro_update_complete(name_request, on_success, nro_warnings)
        elif name_request.stateCd in [State.CONDITIONAL, State.APPROVED]:
            if current_app.config.get('DISABLE_NAMEREQUEST_NRO_UPDATES', 0) == 1:
                # Ignore update to NRO if NRO updates [DISABLE_NAMEREQUEST_NRO_UPDATES] are explicitly disabled in your .env
                nro_warnings = None
            else:
                nro_warnings = self.nro_service.change_nr(name_request, {
                    NROChangeFlags.REQUEST.value: True,
                    NROChangeFlags.APPLICANT.value: True,
                    NROChangeFlags.ADDRESS.value: True,
                    NROChangeFlags.NAME_1.value: False,
                    NROChangeFlags.NAME_2.value: False,
                    NROChangeFlags.NAME_3.value: False,
                    NROChangeFlags.CONSENT.value: False
                })

            return self.on_nro_update_complete(name_request, on_success, nro_warnings)
        elif name_request.stateCd in [State.CANCELLED]:
            if current_app.config.get('DISABLE_NAMEREQUEST_NRO_UPDATES', 0) == 1:
                # Ignore update to NRO if NRO updates [DISABLE_NAMEREQUEST_NRO_UPDATES] are explicitly disabled in your .env
                nro_warnings = None
            else:
                # TODO: Update this! Add in mocks...
                nro_warnings = self.nro_service.cancel_nr(name_request, 'name_request_service_account')

            return self.on_nro_update_complete(name_request, on_success, nro_warnings)
        else:
            raise NameRequestException(message='Invalid state exception [' + name_request.stateCd + '], cannot update Name Request in NRO when Request state is NOT in DRAFT or CANCELLED')

    def on_nro_update_complete(self, name_request, on_success, warnings, is_new_record=False):
        """
        Used internally. Called by:
         - add_request_to_nro
         - update_request_in_nro
        :param name_request:
        :param on_success:
        :param warnings:
        :param is_new_record:
        :return:
        """
        if warnings:
            code = 'add_request_in_NRO' if is_new_record else 'update_request_in_NRO'
            MessageServices.add_message(MessageServices.ERROR, code, warnings)
            raise NROUpdateError()

        if on_success:
            return on_success(name_request, self.nr_service)

    @staticmethod
    def log_error(msg, err):
        return msg.format(err)
