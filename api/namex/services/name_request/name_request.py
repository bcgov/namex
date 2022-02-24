from datetime import datetime
from pytz import timezone

from namex.utils.logging import setup_logging

from namex.constants import NameState, RequestAction, ExpiryDays

from namex.models import Request, Name, State, Applicant

from .abstract_name_request import AbstractNameRequestMixin
from .name_request_state import apply_nr_state_change, get_nr_state_actions

# Mapping utils used to map HTTP request data to a Request model
from .mappers.request_header_attrs import map_request_header_attrs
from .mappers.request_draft_attrs import map_draft_attrs
from .mappers.request_attrs import map_request_attrs
from .mappers.request_applicants import map_request_applicant
from .mappers.request_comments import map_request_comments
from .mappers.request_names import map_submitted_name

from .utils import get_item_from_list
from .exceptions import CreateNameRequestError, SaveNameRequestError, MapRequestDataError, \
    MapRequestApplicantError, MapRequestNamesError, UpdateSubmitCountError, ExtendExpiryDateError

setup_logging()  # Important to do this first


class NameRequestService(AbstractNameRequestMixin):
    """
    Basic usage:

    # 1. Create or retrieve an NR
    nr_model = Request()

    # Sample method to generate a new NR number
    def generate_nr():
        db.session.query(NRNumber).first()
        if r is None:
            # Set starting nr number
            last_nr = 'NR L000000'
        else:
            last_nr = r.nrNum
        return nr_num

        nr_num = NRNumber.get_next_nr_num(last_nr)
        r.nrNum = nr_num
        r.save_to_db()

    # 2. Set the initial state of the NR
    nr_model.stateCd = State.DRAFT

    # 3. Create an instance of this service
    nr_svc = NameRequestService()

    # 3a. Important! Set the nr_num property on the service
    nr_svc.nr_num = generate_nr()

    # 3b. Important! Set the nr_id
    nr_svc.nr_id = nr_model.id

    # 3c. Important! Set the request_data
    nr_svc.request_data = request.get_json()

    # 4. Do your update logic in here
    def on_update(nr, svc):
        # Do stuff here
        nr = svc.map_request_data(nr, False)
        # Save the request
        nr = svc.save_request(nr)
        # Return the updated name request
        # The result of on_update is returned as the result of apply_state_change
        return nr

    # 5. Run apply_state_change to execute the update
    nr_model = nr_svc.apply_state_change(nr_model, new_state, on_update)
    """
    _virtual_wc_service = None

    @property
    def virtual_wc_service(self):
        return self._virtual_wc_service

    @virtual_wc_service.setter
    def virtual_wc_service(self, service):
        self._virtual_wc_service = service

    @property
    def new_state_code(self):
        return self.next_state_code if self.next_state_code else self.request_state_code

    def create_name_request(self):
        """
        # !Important! All new name requests should be initially set to the DRAFT state.
        # Use apply_state_change on the name_request to transition to any other state.
        :return:
        """
        try:
            name_request = Request()
            self.generate_nr_keys()

            name_request.stateCd = State.DRAFT
        except Exception as err:
            raise CreateNameRequestError(err)

        return name_request

    @classmethod
    def create_name(cls):
        try:
            name = Name()
            name_id = cls.get_name_sequence()
            name.id = name_id
            name.state = NameState.NOT_EXAMINED.value
        except Exception as err:
            raise MapRequestNamesError(err, 'Error setting submitted_name and / or sequence.')

        return name

    @classmethod
    def create_applicant(cls):
        try:
            applicant = Applicant()
            applicant.partyId = cls.get_applicant_sequence()
        except Exception as err:
            raise MapRequestApplicantError(err, 'Error setting applicant and / or sequence.')

        return applicant

    @classmethod
    def get_item_from_list(cls, items, item_id, item_prop='id'):
        return get_item_from_list(items, item_id, item_prop=item_prop)

    @classmethod
    def update_request_submit_count(cls, name_request):
        try:
            name_request.submitCount = name_request.submitCount + 1 if isinstance(name_request.submitCount, int) else 1
        except Exception as err:
            raise UpdateSubmitCountError(err)

        return name_request

    @classmethod
    def get_expiry_days(cls, name_request):
        """
        returns expiry days of an NR.
        """
        if name_request.request_action_cd in [RequestAction.REH.value, RequestAction.REN.value, RequestAction.REST.value]:
            expires_days = ExpiryDays.NAME_REQUEST_REH_REN_LIFESPAN_DAYS.value
        else:
            if name_request.request_type_cd in ['RCR', 'RUL', 'BERE', 'RCC', 'RCP', 'RFI', 'XRCR', 'RLC', 'XRCP','RSO','XRSO']:
                expires_days = ExpiryDays.NAME_REQUEST_REH_REN_LIFESPAN_DAYS.value
            else:
                expires_days = ExpiryDays.NAME_REQUEST_LIFESPAN_DAYS.value

        return expires_days

    @classmethod
    def extend_expiry_date(cls, name_request, start_date=None):
        """
        Extends/sets the expiry date of an NR.

        Default: extends the expiry date to 56 days date at 11:59pm.
        """
        start_datetime = start_date if start_date else datetime.utcnow()
        try:
            expiry_days = int(cls.get_expiry_days(name_request))
           
            name_request.expirationDate = cls.create_expiry_date(
                start=start_datetime,
                expires_in_days=expiry_days
            )
        except Exception as err:
            raise ExtendExpiryDateError(err)

        return name_request

    def map_request_data(self, name_request, map_attrs=False):
        """
        This method maps data from the HTTP request data over to the name request.
        We use this to set draft attributes, header attributes, and comments...
        You must explicitly call this method when using an instance of the service to map data to properties on the Request model.
        :param name_request:
        :param map_attrs:
        :return:
        """
        # Set the request attributes
        name_request = map_request_attrs(
            name_request,
            nr_id=self.nr_id,
            nr_num=self.nr_num,
            request_entity=self.request_entity,
            request_action=self.request_action,
            request_type=self.request_type
        )

        # If this is a DRAFT, set draft attributes
        if map_attrs:
            name_request = map_draft_attrs(name_request, user_id=self.user_id)

        # Map request header attributes
        name_request = map_request_header_attrs(
            name_request,
            request_data=self.request_data,
            user_id=self.user_id
        )

        # Map request comments
        name_request = map_request_comments(
            name_request,
            request_data=self.request_data,
            user_id=self.user_id,
            nr_id=self.nr_id
        )

        try:
            if self.new_state_code == State.COND_RESERVE:
                name_request.consentFlag = 'Y'

            if self.new_state_code in [State.RESERVED, State.COND_RESERVE]:
                expiry_days = int(self.get_expiry_days(name_request))
                name_request.expirationDate = self.create_expiry_date(
                    start=name_request.submittedDate,
                    expires_in_days=expiry_days
                )
        except Exception as err:
            raise MapRequestDataError(err)

        return name_request

    def map_request_applicants(self, name_request):
        """
        This method maps applicants from the HTTP request data over to the name request.
        You must explicitly call this method when using an instance of the service to map applicants to the Request model.
        :param name_request:
        :return:
        """
        try:
            request_data = self.request_data
            nr_id = self.nr_id

            request_applicants = request_data.get('applicants')
            applicants = []

            def create_or_update_applicant(mapped_applicants, applicant_data):
                if request_applicant_id:
                    existing_applicants = name_request.applicants.all()
                    match = get_item_from_list(existing_applicants, request_applicant_id, 'partyId')
                    if match:
                        applicant = map_request_applicant(match, applicant_data)
                        mapped_applicants.append(applicant)
                else:
                    applicant = self.create_applicant()
                    applicant.nrId = nr_id

                    applicant = map_request_applicant(applicant, applicant_data)
                    mapped_applicants.append(applicant)

                return applicants

            if isinstance(request_applicants, list):
                for request_applicant in request_applicants:
                    request_applicant_id = request_applicant.get('partyId')
                    applicants = create_or_update_applicant(applicants, request_applicant)

                name_request.applicants = applicants

            elif isinstance(request_applicants, dict):
                request_applicant_id = request_applicants.get('partyId')
                applicants = create_or_update_applicant(applicants, request_applicants)

                name_request.applicants = applicants

        except Exception as err:
            raise MapRequestApplicantError(err)

        return name_request

    def map_request_names(self, name_request):
        """
        This method maps names from the HTTP request data over to the name request.
        You must explicitly call this method when using an instance of the service to map names to the Request model.
        :param name_request:
        :return:
        """
        if not isinstance(self.request_names, list):
            raise MapRequestNamesError()

        try:
            for request_name in self.request_names:
                request_name_id = request_name.get('id')
                if request_name_id:
                    existing_names = name_request.names.all()
                    match = self.get_item_from_list(existing_names, request_name_id)
                    if match:
                        # Update the name
                        updated_name = map_submitted_name(
                            match,
                            request_name,
                            nr_id=self.nr_id,
                            new_state_code=self.new_state_code,
                            request_entity=self.request_entity,
                            request_action=self.request_action
                        )

                        name_request.names.append(updated_name)
                else:
                    submitted_name = self.create_name()
                    submitted_name = map_submitted_name(
                        submitted_name,
                        request_name,
                        nr_id=self.nr_id,
                        new_state_code=self.new_state_code,
                        request_entity=self.request_entity,
                        request_action=self.request_action
                    )

                    name_request.names.append(submitted_name)

        except Exception as err:
            raise MapRequestNamesError(err)

        return name_request

    def apply_state_change(self, name_request, next_state, on_success=None):
        """
        This is where we handle entity state changes.
        This just wraps .state.apply_nr_state_change located in this module.
        :param name_request:
        :param next_state:
        :param on_success:
        :return:
        """
        def on_success_cb(nr, resource):
            new_state = next_state

            # TODO: Try / except here?
            if on_success:
                nr = on_success(nr, resource)

            # Set the actions corresponding to the new Name Request state
            self.current_state_actions = get_nr_state_actions(new_state, nr)
            return nr

        return apply_nr_state_change(self, name_request, next_state, on_success_cb)

    # CRUD methods
    @classmethod
    def save_request(cls, name_request, on_success=None):
        try:
            name_request.save_to_db()
            if on_success:
                on_success()

            return Request.find_by_nr(name_request.nrNum)

        except Exception as err:
            raise SaveNameRequestError(err)
