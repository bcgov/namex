from pytz import timezone
import os, pysolr
from datetime import datetime

from flask import request
from flask_restplus import Namespace, Resource, fields
from flask import current_app

from namex import nro

from namex.utils.logging import setup_logging

from namex.constants import NameState

from namex.models import Request, Name, State, User, Event, Comment, Applicant

from namex.services import MessageServices
from namex.services.virtual_word_condition.virtual_word_condition import VirtualWordConditionService
from namex.services.name_request import convert_to_ascii

from .abstract_name_request import AbstractNameRequestMixin
from .utils import log_error

from .exceptions import *

setup_logging()  # Important to do this first

# Register a local namespace for the NR reserve
api = Namespace('nameRequests', description='Public facing Name Requests')

applicant_model = api.model('applicant_model', {
    'lastName': fields.String(attribute='lastName'),
    'firstName': fields.String(attribute='firstName'),
    'middleName': fields.String('Applicant middle name or initial'),
    'contact': fields.String('Applicant contact person last and first name'),
    'clientFirstName': fields.String('Client first name'),
    'clientLastName': fields.String('Client last name'),
    'phoneNumber': fields.String('Contact phone number'),
    'faxNumber': fields.String('Contact fax number'),
    'emailAddress': fields.String('Contact email'),
    'addrLine1': fields.String('First address line'),
    'addrLine2': fields.String('Second address line'),
    'city': fields.String('City'),
    'stateProvinceCd': fields.String('Province or state code'),
    'postalCd': fields.String('Postal code or zip code'),
    'countryTypeCd': fields.String('Country code')
})

consent_model = api.model('consent_model', {
    'consent_word': fields.String('A word that requires consent')
})

name_model = api.model('name_model', {
    'choice': fields.Integer('Name choice'),
    'name': fields.String('Name'),
    'name_type_cd': fields.String('For company or assumed name', enum=['CO', 'AS']),
    'state': fields.String('The state of the Name'),
    'designation': fields.String('Name designation based on entity type'),
    'conflict1_num': fields.String('The corp_num of the matching name'),
    'conflict1': fields.String('The matching corp name'),
    'consent_words': fields.Nested(consent_model)
})

nr_request = api.model('name_request', {
    'entity_type': fields.String('The entity type'),
    'request_action': fields.String('The action requested by the user'),
    'stateCd': fields.String('The state of the NR'),
    'english': fields.Boolean('Set when the name is English only'),
    'nameFlag': fields.Boolean('Set when the name is a person'),
    'additionalInfo': fields.String('Additional NR Info'),
    'natureBusinessInfo': fields.String('The nature of business'),
    'tradeMark': fields.String('Registered Trademark'),
    'previousRequestId': fields.Integer('Internal Id for Re-Applys'),
    'priorityCd': fields.String('Set to Yes if it is  priority going to examination'),
    'submit_count': fields.Integer('Used to enforce the 3 times only rule for Re-Applys'),
    'xproJurisdiction': fields.String('The province or country code for XPRO requests'),
    'homeJurisNum': fields.String('For MRAS participants, their home jurisdiction corp_num'),
    'corpNum': fields.String('For companies already registered in BC, their BC corp_num'),
    'applicants': fields.Nested(applicant_model),
    'names': fields.Nested(name_model)
})

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
    party_id = party_id
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


class BaseNameRequest(Resource, AbstractNameRequestMixin):
    @property
    def restricted_word_service(self):
        try:
            if not self._restricted_word_service:
                self._restricted_word_service = VirtualWordConditionService()
        except Exception as err:
            log_error('Error initializing VirtualWordCondition Service. Error: {0}', err)
            raise VirtualWordContidionServiceError()

        return self._restricted_word_service

    @property
    def user_id(self):
        try:
            user = User.find_by_username('name_request_service_account')
        except Exception as err:
            raise GetUserIdError(err)

        return user.id

    @property
    def user(self):
        try:
            user = User.find_by_username('name_request_service_account')
        except Exception as err:
            raise GetUserIdError(err)

        return user

    # Initialization methods
    @classmethod
    def _validate_config(cls):
        app_config = current_app.config.get('SOLR_SYNONYMS_API_URL', None)
        if not app_config:
            log_error('ENV is not set', None)
            raise Exception('Internal server error')

        test_env = 'prod'
        if test_env in app_config:
            return NotImplementedError()

    def _before_create_or_update(self):
        self._validate_config()

        self.request_data = request.get_json()
        if not self.request_data:
            log_error('Error getting json input.', None)
            raise InvalidInputError()

    def create_name_request(self):
        try:
            name_request = Request()
            self.generate_nr_keys()
        except Exception as err:
            raise CreateNameRequestError(err)

        return name_request

    def update_request_submit_count(self, name_request):
        if self.request_data['submit_count'] is None:
            name_request.submitCount = 1
        else:
            name_request.submitCount = + 1

        return name_request

    # Methods used to map request data
    def map_request_attrs(self, name_request):
        request_entity = self.request_entity
        request_action = self.request_action
        nr_id = self.nr_id
        nr_num = self.nr_num

        name_request.id = nr_id
        name_request.submittedDate = datetime.utcnow()
        name_request.requestTypeCd = self.set_request_type(request_entity, request_action)
        name_request.nrNum = nr_num
        name_request._source = NAME_REQUEST_SOURCE

        return name_request

    def map_request_language_comments(self, name_request):
        request_data = self.request_data
        user_id = self.user_id
        nr_id = self.nr_id

        lang_comment = build_language_comment(request_data['english'], user_id, nr_id)
        name_request.comments.append(lang_comment)

        return name_request

    def map_request_person_name_comments(self, name_request):
        request_data = self.request_data
        user_id = self.user_id
        nr_id = self.nr_id

        if request_data['nameFlag'] is True:
            name_comment = build_name_comment(user_id, nr_id)
            name_request.comments.append(name_comment)

        return name_request

    def map_request_attributes(self, name_request, request_data, user_id):
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

        return name_request

    def map_request_data(self, name_request):
        user_id = self.user_id
        next_state = self.next_state_code
        request_data = self.request_data
        request_entity = self.request_entity
        request_action = self.request_action

        # Set the request attributes
        try:
            name_request = self.map_request_attrs(name_request)
        except Exception as err:
            raise MapRequestAttributesError(err)

        try:
            if next_state == State.COND_RESERVE:
                name_request.consentFlag = 'Y'

            if next_state in [State.RESERVED, State.COND_RESERVE]:
                name_request.expirationDate = self.create_expiry_date(start=name_request.submittedDate, expires_in_days=56, tz=timezone('UTC'))

            name_request.stateCd = next_state
            name_request.entity_type_cd = request_entity
            name_request.request_action_cd = request_action
        except Exception as err:
            raise RequestStateChangeError(err)

        # Set this to name_request_service_account
        name_request.userId = user_id

        try:
            name_request = self.map_request_language_comments(name_request)
        except Exception as err:
            raise MapLanguageCommentError(err)

        try:
            self.map_request_person_name_comments(name_request)
        except Exception as err:
            raise MapPersonCommentError(err)

        try:
            name_request = self.update_request_submit_count(name_request)
        except Exception as err:
            raise UpdateSubmitCountError(err)

        if next_state == State.DRAFT:
            try:
                # Set name request header attributes
                name_request = self.map_request_attributes(name_request, request_data, user_id)
            except Exception as err:
                raise RequestStateChangeError(err)

        return name_request

    def map_request_applicants(self, name_request):
        request_data = self.request_data
        nr_id = self.nr_id

        applicants = []
        for request_applicant in request_data.get('applicants', []):
            applicant = build_request_applicant(nr_id, self.get_applicant_sequence(), request_applicant)
            applicants.append(applicant)

        name_request.applicants = applicants

        return name_request

    def map_request_names(self, name_request):
        if not self.request_names:
            raise MapRequestNamesError()

        try:
            for name in self.request_names:
                submitted_name = self.map_submitted_name(name)
                name_request.names.append(submitted_name)
        except Exception as err:
            raise MapRequestNamesError(err)

        return name_request

    def map_submitted_name(self, name):
        next_state = self.next_state_code

        try:
            submitted_name = Name()
            name_id = self.get_name_sequence()
            submitted_name.id = name_id
        except Exception as err:
            raise MapRequestNamesError(err, 'Error setting submitted_name and / or sequence.')

        # Common name attributes
        try:
            submitted_name = self.map_submitted_name_attrs(submitted_name, name)
        except Exception as err:
            raise MapRequestNamesError(err, 'Error setting common name attributes.')

        decision_text = None

        if next_state in [State.RESERVED, State.COND_RESERVE]:
            try:
                # Only capturing one conflict
                if name['conflict1_num']:
                    submitted_name.conflict1_num = name['conflict1_num']
                if name['conflict1']:
                    submitted_name.conflict1 = name['conflict1']
                # Conflict text same as Namex
                decision_text = 'Consent is required from ' + name['conflict1'] + '\n' + '\n'
            except Exception as err:
                raise MapRequestNamesError(err, 'Error on reserved conflict info.')
        else:
            try:
                submitted_name.conflict1_num = None
                submitted_name.conflict1 = None
            except Exception as err:
                raise MapRequestNamesError(err, 'Error on draft empty conflict info.')

        consent_list = name['consent_words']
        if len(consent_list) > 0:
            for consent in consent_list:
                try:
                    cnd_instructions = None
                    if consent != '' or len(consent) > 0:
                        cnd_instructions = self.restricted_word_service.get_word_condition_instructions(consent)
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

    def map_submitted_name_attrs(self, submitted_name, name):
        next_state = self.next_state_code

        submitted_name.choice = name['choice']
        submitted_name.name = name['name']

        if name['name_type_cd']:
            submitted_name.name_type_cd = name['name_type_cd']
        else:
            submitted_name.name_type_cd = 'CO'

        if next_state == State.DRAFT:
            submitted_name.state = NameState.NOT_EXAMINED.value
        else:
            submitted_name.state = next_state

        if name['designation']:
            submitted_name.designation = name['designation']

        submitted_name.nrId = self.nr_id

        return submitted_name

    # CRUD methods
    def save_request(self, name_request, on_success=None):
        try:
            name_request.save_to_db()
            if on_success:
                on_success()

            return Request.find_by_nr(name_request.nrNum)

        except Exception as err:
            raise SaveNameRequestError(err)

    def save_request_to_nro(self, name_request, next_state_code):
        next_state = next_state_code if next_state_code else self.next_state_code

        # Only update Oracle for APPROVED, CONDITIONAL, DRAFT
        if next_state in [State.DRAFT, State.APPROVED, State.CONDITIONAL]:
            # Note: Comment out this block to run locally, or you will get Oracle errors
            warnings = nro.add_nr(name_request)
            if warnings:
                MessageServices.add_message(MessageServices.ERROR, 'add_request_in_NRO', warnings)
                raise NROUpdateError()
            else:
                # added the oracle request_id in new_nr, need to save it postgres
                # set the furnished_flag='Y' for approved and conditionally approved
                if self.request_data['stateCd'] in [State.APPROVED, State.CONDITIONAL]:
                    name_request.furnished = 'Y'

        return name_request

    def update_solr(self, core, solr_docs):
        SOLR_URL = os.getenv('SOLR_BASE_URL')
        solr = pysolr.Solr(SOLR_URL + '/solr/' + core + '/', timeout=10)
        solr.add(solr_docs, commit=True)

    def update_solr_doc(self, updated_nr, name_request):
        next_state = self.next_state_code
        # TODO: Need to add verification that the save was successful.
        # Update solr for reservation
        try:
            if next_state in [State.RESERVED, State.COND_RESERVE]:
                solr_name = updated_nr.names[0].name
                solr_docs = []
                nr_doc = {'id': name_request.nrNum, 'name': solr_name, 'source': 'NR',
                          'start_date': name_request.submittedDate.strftime('%Y-%m-%dT%H:%M:00Z')}

                solr_docs.append(nr_doc)
                self.update_solr('possible.conflicts', solr_docs)
        except Exception as err:
            raise SolrUpdateError(err)
