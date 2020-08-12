import os

from datetime import datetime
from pytz import timezone

from namex.utils.logging import setup_logging

from namex.constants import NameState

from namex.models import Request, Name, State, Comment, Applicant

from .abstract_name_request import AbstractNameRequestMixin
from .name_request_state import apply_nr_state_change, get_nr_state_actions

from .exceptions import \
    CreateNameRequestError, SaveNameRequestError, MapRequestDataError, MapRequestHeaderAttributesError, MapRequestAttributesError, \
    MapRequestNamesError, MapPersonCommentError, MapLanguageCommentError, UpdateSubmitCountError, ExtendExpiryDateError

from .utils import log_error, convert_to_ascii

setup_logging()  # Important to do this first

NAME_REQUEST_SOURCE = 'NAMEREQUEST'


def build_language_comment(english_bol, user_id, nr_id):
    lang_comment = Comment()
    lang_comment.examinerId = user_id
    lang_comment.nrId = nr_id
    if english_bol is True:
        # Add a comment for the examiner that says this is not an english name
        lang_comment.comment = 'The applicant has indicated the submitted name or names are in English.'
    else:
        lang_comment.comment = 'The applicant has indicated the submitted name or names are not English.'
    return lang_comment


def build_name_comment(user_id, nr_id):
    name_comment = Comment()
    name_comment.examinerId = user_id
    name_comment.nrId = nr_id
    name_comment.comment = 'The submitted name or names is a person name, coined phrase or trademark'
    return name_comment


def build_request_applicant(nr_id, party_id, request_applicant):
    # Applicant, contact and address info
    applicant = Applicant()
    applicant.nrId = nr_id
    applicant.partyId = party_id
    applicant.lastName = convert_to_ascii(request_applicant['lastName'])
    applicant.firstName = convert_to_ascii(request_applicant['firstName'])
    if request_applicant['middleName']:
        applicant.middleName = convert_to_ascii(request_applicant['middleName'])
    applicant.contact = convert_to_ascii(request_applicant['contact'])
    if request_applicant['middleName']:
        applicant.middleName = convert_to_ascii(request_applicant['middleName'])
    if request_applicant['clientFirstName']:
        applicant.clientFirstName = convert_to_ascii(request_applicant['clientFirstName'])
    if request_applicant['clientLastName']:
        applicant.clientLastName = convert_to_ascii(request_applicant['clientLastName'])
    if request_applicant['phoneNumber']:
        applicant.phoneNumber = convert_to_ascii(request_applicant['phoneNumber'])
    if request_applicant['faxNumber']:
        applicant.faxNumber = convert_to_ascii(request_applicant['faxNumber'])
    applicant.emailAddress = convert_to_ascii(request_applicant['emailAddress'])
    applicant.addrLine1 = convert_to_ascii(request_applicant['addrLine1'])
    if request_applicant['addrLine2']:
        applicant.addrLine2 = convert_to_ascii(request_applicant['addrLine2'])
    applicant.city = convert_to_ascii(request_applicant['city'])
    applicant.stateProvinceCd = request_applicant['stateProvinceCd']
    applicant.postalCd = convert_to_ascii(request_applicant['postalCd'])
    applicant.countryTypeCd = request_applicant['countryTypeCd']

    return applicant


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

    def create_name(self):
        try:
            name = Name()
            name_id = self.get_name_sequence()
            name.id = name_id
            name.state = NameState.NOT_EXAMINED.value
        except Exception as err:
            raise MapRequestNamesError(err, 'Error setting submitted_name and / or sequence.')

        return name

    @classmethod
    def get_name_from_list(cls, names, name_id):
        matches = [n for n in names if n.id == name_id]
        if len(matches) == 0:
            return None
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise Exception('More than one match for a name!')

    @classmethod
    def update_request_submit_count(cls, name_request):
        try:
            name_request.submitCount = name_request.submitCount + 1 if isinstance(name_request.submitCount, int) else 1
        except Exception as err:
            raise UpdateSubmitCountError(err)

        return name_request

    def extend_expiry_date(self, name_request, start_date=None):
        start_datetime = start_date if start_date else datetime.utcnow()
        """
        Extends the expiry date by 56 days from today's date
        :param name_request:
        :return:
        """
        try:
            name_request.expirationDate = self.create_expiry_date(
                start=start_datetime,
                expires_in_days=56,
                tz=timezone('UTC')
            )
        except Exception as err:
            raise ExtendExpiryDateError(err)

        return name_request

    # Methods used to map request data
    def map_request_data(self, name_request, map_draft_attrs=False):
        """
        This method maps data from the HTTP request data over to the name request.
        We use this to set draft attributes, header attributes, and comments...
        :param name_request:
        :param map_draft_attrs:
        :return:
        """
        new_state_code = self.next_state_code if self.next_state_code else self.request_state_code

        # Set the request attributes
        name_request = self.map_request_attrs(name_request)

        # If this is a draft, set name request header attributes
        if map_draft_attrs:
            name_request = self.map_draft_attrs(name_request)

        name_request = self.map_request_header_attrs(name_request)
        name_request = self.map_request_comments(name_request)

        try:
            if new_state_code == State.COND_RESERVE:
                name_request.consentFlag = 'Y'

            if new_state_code in [State.RESERVED, State.COND_RESERVE]:
                name_request.expirationDate = self.create_expiry_date(
                    start=name_request.submittedDate,
                    expires_in_days=56,
                    tz=timezone('UTC')
                )
        except Exception as err:
            raise MapRequestDataError(err)

        return name_request

    def map_draft_attrs(self, name_request):
        """
        Used internally by map_request_data.
        :param name_request:
        :return:
        """
        try:
            user_id = self.user_id
            request_entity = self.request_entity
            request_action = self.request_action

            # Set this to name_request_service_account
            name_request.userId = user_id
            name_request.submittedDate = datetime.utcnow()
            name_request.entity_type_cd = request_entity

            if request_action:
                name_request.request_action_cd = request_action
                name_request.requestTypeCd = self.set_request_type(name_request.entity_type_cd, request_action)
        except Exception as err:
            raise MapRequestDataError(err)

        return name_request

    def map_request_attrs(self, name_request):
        """
        Used internally by map_request_data.
        :param name_request:
        :return:
        """
        try:
            nr_id = self.nr_id
            nr_num = self.nr_num

            name_request.id = nr_id
            name_request.nrNum = nr_num
            name_request._source = NAME_REQUEST_SOURCE
        except Exception as err:
            raise MapRequestAttributesError(err)

        return name_request

    def map_request_header_attrs(self, name_request):
        """
        Used internally by map_request_data.
        :param name_request:
        :return:
        """
        user_id = self.user_id
        request_data = self.request_data

        try:
            # TODO: Review additional info stuff from NRO/namex (prev NR for re-applies,no NWPTA?
            if isinstance(request_data.get('natureBusinessInfo'), str):
                name_request.natureBusinessInfo = convert_to_ascii(request_data.get('natureBusinessInfo'))
            if isinstance(request_data.get('additionalInfo'), str):
                name_request.additionalInfo = convert_to_ascii(request_data.get('additionalInfo'))
            if isinstance(request_data.get('tradeMark'), str):
                name_request.tradeMark = request_data.get('tradeMark')
            if isinstance(request_data.get('previousRequestId'), int):
                name_request.previousRequestId = request_data.get('previousRequestId')
            if isinstance(request_data.get('priorityCd'), str):
                name_request.priorityCd = request_data.get('priorityCd')
            if request_data.get('priorityCd') == 'Y':
                name_request.priorityDate = datetime.utcnow().date()

            name_request.submitter_userid = user_id

            # XPRO
            if isinstance(request_data.get('xproJurisdiction'), str):
                name_request.xproJurisdiction = request_data.get('xproJurisdiction')
            # For MRAS participants
            if isinstance(request_data.get('homeJurisNum'), str):
                name_request.homeJurisNum = convert_to_ascii(request_data.get('homeJurisNum'))
            # For existing businesses
            if isinstance(request_data.get('corpNum'), str):
                name_request.corpNum = convert_to_ascii(request_data.get('corpNum'))
        except Exception as err:
            raise MapRequestHeaderAttributesError(err)

        return name_request

    def map_request_comments(self, name_request):
        """
        Used internally by map_request_data. Execute any logic required to map comments here.
        :param name_request:
        :return:
        """
        name_request = self.map_request_language_comments(name_request)
        name_request = self.map_request_person_name_comments(name_request)

        return name_request

    def map_request_language_comments(self, name_request):
        """
        Used internally by map_request_comments.
        :param name_request:
        :return:
        """
        try:
            request_data = self.request_data
            user_id = self.user_id
            nr_id = self.nr_id

            # If the language comment exists, we don't need to add it again
            lang_comment = build_language_comment(request_data.get('english'), user_id, nr_id)
            matching_comments = list(filter(lambda x: x.comment == lang_comment.comment, list(name_request.comments)))
            if len(matching_comments) == 0:
                name_request.comments.append(lang_comment)
        except Exception as err:
            raise MapLanguageCommentError(err)

        return name_request

    def map_request_person_name_comments(self, name_request):
        """
        Used internally by map_request_comments.
        :param name_request:
        :return:
        """
        try:
            request_data = self.request_data
            user_id = self.user_id
            nr_id = self.nr_id

            if request_data.get('nameFlag') is True:
                # If the person name comment exists, we don't need to add it again
                name_comment = build_name_comment(user_id, nr_id)
                matching_comments = list(filter(lambda x: x.comment == name_comment.comment, list(name_request.comments)))
                if len(matching_comments) == 0:
                    name_request.comments.append(name_comment)
        except Exception as err:
            raise MapPersonCommentError(err)

        return name_request

    def map_request_applicants(self, name_request):
        """
        This method maps applicants from the HTTP request data over to the name request.
        :param name_request:
        :return:
        """
        request_data = self.request_data
        nr_id = self.nr_id

        request_applicants = request_data.get('applicants')
        applicants = []

        if isinstance(request_applicants, list):
            for request_applicant in request_data.get('applicants', []):
                applicant = build_request_applicant(nr_id, self.get_applicant_sequence(), request_applicant)
                applicants.append(applicant)

        elif isinstance(request_applicants, dict):
            applicant = build_request_applicant(nr_id, self.get_applicant_sequence(), request_applicants)
            applicants.append(applicant)

        name_request.applicants = applicants

        return name_request

    def map_request_names(self, name_request):
        """
        This method maps names from the HTTP request data over to the name request.
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
                    match = self.get_name_from_list(existing_names, request_name_id)
                    if match:
                        # Update the name
                        updated_name = self.map_submitted_name(match, request_name)
                        name_request.names.append(updated_name)
                else:
                    submitted_name = self.create_name()
                    submitted_name = self.map_submitted_name(submitted_name, request_name)
                    name_request.names.append(submitted_name)

        except Exception as err:
            raise MapRequestNamesError(err)

        return name_request

    def map_submitted_name(self, submitted_name, name):
        """
        Used internally by map_request_names.
        :param submitted_name:
        :param name:
        :return:
        """
        new_state_code = self.next_state_code if self.next_state_code else self.request_state_code

        # Common name attributes
        submitted_name = self.map_submitted_name_attrs(submitted_name, name)
        test_conflict = name.get('conflict1')
        if len(test_conflict) > 0:
            conflict_flag = 'Y'
        else:
            conflict_flag = 'N'

        if new_state_code in [State.COND_RESERVE] and conflict_flag == 'Y':
            submitted_name = self.map_submitted_name_conflicts(submitted_name, name)

        consent_words_list = name.get('consent_words', None)
        if consent_words_list and len(consent_words_list) > 0:
            submitted_name = self.map_submitted_name_consent_words(submitted_name, consent_words_list)

        return submitted_name

    def map_submitted_name_attrs(self, submitted_name, name):
        """
        Used internally by map_submitted_name.
        :param submitted_name:
        :param name:
        :return:
        """
        new_state_code = self.next_state_code if self.next_state_code else self.request_state_code

        try:
            submitted_name.nrId = self.nr_id
            submitted_name.choice = name.get('choice', 1)
            submitted_name.name_type_cd = name.get('name_type_cd', 'CO')
            submitted_name.name = convert_to_ascii(name.get('name', ''))
            submitted_name.designation = name.get('designation', '')

            if new_state_code == State.DRAFT:
                submitted_name.state = NameState.NOT_EXAMINED.value

            elif new_state_code == State.COND_RESERVE:
                submitted_name.state = NameState.COND_RESERVE.value

            elif new_state_code == State.RESERVED:
                submitted_name.state = NameState.RESERVED.value

            elif new_state_code == State.CONDITIONAL:
                submitted_name.state = NameState.CONDITION.value

            elif new_state_code == State.APPROVED:
                submitted_name.state = NameState.APPROVED.value

        except Exception as err:
            raise MapRequestNamesError(err, 'Error setting common name attributes.')

        return submitted_name

    def map_submitted_name_conflicts(self, submitted_name, name):
        """
        Used internally by map_submitted_name.
        :param submitted_name:
        :param name:
        :return:
        """
        try:
            # Only capturing one conflict
            if name.get('conflict1_num'):
                submitted_name.conflict1_num = name.get('conflict1_num')
            if name.get('conflict1'):
                submitted_name.conflict1 = name.get('conflict1')
            # Conflict text same as Namex
            submitted_name.decision_text = 'Consent is required from ' + name.get('conflict1') + '\n' + '\n'
        except Exception as err:
            raise MapRequestNamesError(err, 'Error on reserved conflict info.')

        return submitted_name

    def clear_submitted_name_conflicts(self, submitted_name):
        """
        Used internally by map_submitted_name.
        :param submitted_name:
        :param name:
        :return:
        """
        try:
            submitted_name.conflict1_num = None
            submitted_name.conflict1 = None
        except Exception as err:
            raise MapRequestNamesError(err, 'Error on draft empty conflict info.')

        return submitted_name

    def map_submitted_name_consent_words(self, submitted_name, consent_list):
        """
        Used internally by map_submitted_name.
        :param submitted_name:
        :param consent_list:
        :return:
        """
        decision_text = submitted_name.decision_text
        for consent in consent_list:
            try:
                cnd_instructions = None
                if consent != '' or len(consent) > 0:
                    cnd_instructions = self.virtual_wc_service.get_word_condition_instructions(consent)
            except Exception as err:
                log_error('Error on get consent word. Consent Word[0]'.format(consent), err)
                raise MapRequestNamesError('Error mapping consent words.')

            try:
                if decision_text is None:
                    decision_text = cnd_instructions + '\n'
                else:
                    decision_text += consent + '- ' + cnd_instructions + '\n'

                submitted_name.decision_text = decision_text
            except Exception as err:
                raise MapRequestNamesError(err, 'Error adding consent words to decision.')

        return submitted_name

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
            self.current_state_actions = get_nr_state_actions(new_state)
            return nr

        return apply_nr_state_change(self, name_request, next_state, on_success_cb)

    # CRUD methods
    def save_request(self, name_request, on_success=None):
        try:
            name_request.save_to_db()
            if on_success:
                on_success()

            return Request.find_by_nr(name_request.nrNum)

        except Exception as err:
            raise SaveNameRequestError(err)
