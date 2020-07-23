import os

from datetime import datetime
from pytz import timezone

from namex.utils.logging import setup_logging

from namex.constants import NameState

from namex.models import Request, Name, State, Comment, Applicant

from .abstract_name_request import AbstractNameRequestMixin
from .name_request_state import apply_nr_state_change

from .exceptions import \
    CreateNameRequestError, SaveNameRequestError, MapRequestDataError, MapRequestHeaderAttributesError, MapRequestAttributesError, \
    MapRequestNamesError, MapPersonCommentError, MapLanguageCommentError, UpdateSubmitCountError

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
    _virtual_wc_service = None
    _nr_id = None
    _nr_num = None
    _next_state_code = None

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

    def update_request_submit_count(self, name_request):
        try:
            if self.request_data['submit_count'] is None:
                name_request.submitCount = 1
            else:
                name_request.submitCount = + 1
        except Exception as err:
            raise UpdateSubmitCountError(err)

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

        name_request = self.update_request_submit_count(name_request)

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
            name_request.entity_type_cd = request_entity
            name_request.request_action_cd = request_action
            name_request.submittedDate = datetime.utcnow()
            name_request.requestTypeCd = self.set_request_type(request_entity, request_action)
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
            name_request.natureBusinessInfo = request_data['natureBusinessInfo']
            if request_data['natureBusinessInfo']:
                name_request.natureBusinessInfo = request_data['natureBusinessInfo']

            if request_data['additionalInfo']:
                name_request.additionalInfo = request_data['additionalInfo']
            if request_data['tradeMark']:
                name_request.tradeMark = request_data['tradeMark']
            if request_data['previousRequestId']:
                name_request.previousRequestId = request_data['previousRequestId']
            name_request.priorityCd = request_data['priorityCd']
            if request_data['priorityCd'] == 'Y':
                name_request.priorityDate = datetime.utcnow().date()

            name_request.submitter_userid = user_id

            # XPRO
            if request_data['xproJurisdiction']:
                name_request.xproJurisdiction = request_data['xproJurisdiction']
            # For MRAS participants
            if request_data['homeJurisNum']:
                name_request.homeJurisNum = request_data['homeJurisNum']
            # For existing businesses
            if request_data['corpNum']:
                name_request.corpNum = request_data['corpNum']
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
            lang_comment = build_language_comment(request_data['english'], user_id, nr_id)
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

            if request_data['nameFlag'] is True:
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

        applicants = []
        for request_applicant in request_data.get('applicants', []):
            applicant = build_request_applicant(nr_id, self.get_applicant_sequence(), request_applicant)
            applicants.append(applicant)

        name_request.applicants = applicants

        return name_request

    def map_request_names(self, name_request):
        """
        This method maps names from the HTTP request data over to the name request.
        :param name_request:
        :return:
        """
        if not self.request_names:
            raise MapRequestNamesError()

        try:
            for name in self.request_names:
                name_id = name.get('id')
                if name_id:
                    existing_names = []
                    for idx, existing_name in enumerate(name_request.names):
                        existing_names.append(self.map_submitted_name(existing_name, name))
                    name_request.names = existing_names
                else:
                    submitted_name = self.create_name()
                    submitted_name = self.map_submitted_name(submitted_name, name)
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
        if len(test_conflict) > 0 :
            conflict_flag = 'Y'
        else:
            conflict_flag='N'

        if new_state_code in [State.COND_RESERVE] and conflict_flag=='Y':
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
            submitted_name.name = name.get('name', '')
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
        :param name:
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
        return apply_nr_state_change(self, name_request, next_state, on_success)

    # CRUD methods
    def save_request(self, name_request, on_success=None):
        try:
            name_request.save_to_db()
            if on_success:
                on_success()

            return Request.find_by_nr(name_request.nrNum)

        except Exception as err:
            raise SaveNameRequestError(err)
