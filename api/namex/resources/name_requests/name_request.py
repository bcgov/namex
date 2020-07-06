from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from flask import current_app
from pytz import timezone

from namex.utils.logging import setup_logging

from datetime import datetime

from namex.constants import NameState

from namex.models import Request, Name, State, User

# from namex.services import EventRecorder, MessageServices
from namex.services.virtual_word_condition.virtual_word_condition import VirtualWordConditionService

from .abstract import AbstractNameRequestMixin, \
    log_error, handle_exception, \
    set_request_type, create_expiry_date, update_solr, \
    get_name_sequence, \
    build_language_comment, build_name_comment, \
    map_request_attributes

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


class BaseNameRequest(Resource, AbstractNameRequestMixin):
    # TODO: Fix this!
    # def __init__(self, *args, **kwargs):
    #    super(Resource, self).__init__()
    #    self._restricted_word_service = None
    #    self._request_data = None
    #    self._next_state_code = None
    #    self._nr_num = None
    #    self._nr_id = None

    @property
    def restricted_word_service(self):
        try:
            if not self._restricted_word_service:
                self._restricted_word_service = VirtualWordConditionService()
        except Exception as err:
            log_error('Error initializing VirtualWordCondition Service: Error:{0}', err)
            # TODO: Make sure these exceptions are being handled properly
            # return jsonify({'message': 'Virtual Word Condition Service error'}), 404
            raise

        return self._restricted_word_service

    @property
    def user_id(self):
        # Get the user
        try:
            user = User.find_by_username('name_request_service_account')
        except Exception as err:
            return handle_exception(err, 'Error getting user id.', 500)

        return user.id

    # Initialization methods
    @classmethod
    def _validate_config(cls):
        app_config = current_app.config.get('SOLR_SYNONYMS_API_URL', None)
        if not app_config:
            log_error('ENV is not set', None)
            return None, 'Internal server error', 500

        test_env = 'prod'
        if test_env in app_config:
            log_error('Someone is trying to post a new request. Not available.', None)
            return jsonify({'message': 'Not Implemented in the current environment'}), 501

    def _before_create_or_update(self):
        self._validate_config()

        self.request_data = request.get_json()
        if not self.request_data:
            log_error('Error when getting json input', None)
            return jsonify({'message': 'No input data provided'}), 400

    def create_name_request(self):
        try:
            name_request = Request()
        except Exception as err:
            return handle_exception(err, 'Error initializing name_request object.', 500)

        self.generate_nr_keys()

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
        name_request.requestTypeCd = set_request_type(request_entity, request_action)
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
            return handle_exception(err, 'Error setting request header attributes.', 500)

        try:
            if next_state == State.COND_RESERVE:
                name_request.consentFlag = 'Y'

            if next_state in [State.RESERVED, State.COND_RESERVE]:
                name_request.expirationDate = create_expiry_date(start=name_request.submittedDate, expires_in_days=56, tz=timezone('UTC'))

            name_request.stateCd = next_state
            name_request.entity_type_cd = request_entity
            name_request.request_action_cd = request_action
        except Exception as err:
            return handle_exception(err, 'Error setting reserve state and expiration date.', 500)

        # Set this to name_request_service_account
        name_request.userId = user_id

        try:
            name_request = self.map_request_language_comments(name_request)
        except Exception as err:
            return handle_exception(err, 'Error setting language comment.', 500)

        try:
            self.map_request_person_name_comments(name_request)
        except Exception as err:
            return handle_exception(err, 'Error setting person name comment.', 500)

        try:
            name_request = self.update_request_submit_count(name_request)
        except Exception as err:
            return handle_exception(err, 'Error setting submit count.', 500)

        if next_state == State.DRAFT:
            try:
                # Set name request header attributes
                name_request = map_request_attributes(name_request, request_data, user_id)
            except Exception as err:
                return handle_exception(err, 'Error setting request DRAFT attributes.', 500)

        return name_request

    # CRUD methods
    def save_request(self, name_request, on_success):
        next_state = self.next_state_code

        try:
            name_request.save_to_db()
            on_success()
        except Exception as err:
            return handle_exception(err, 'Error saving request [' + next_state + '].', 500)

        # try:
        #     if next_state in [State.RESERVED, State.COND_RESERVE, State.DRAFT]:
        #         name_request.save_to_db()
        # except Exception as err:
        #     return handle_exception(err, 'Error saving reservation to db.', 500)

    def create_or_update_names(self, name_request):
        next_state = self.next_state_code

        if not self.request_names:
            # TODO: Raise error here!
            return

        try:
            for name in self.request_names:
                submitted_name = self._create_or_update_name(name)

                try:
                    name_request.names.append(submitted_name)
                except Exception as err:
                    return handle_exception(err, 'Error appending names.', 500)
            try:
                # Save names to postgres
                name_request.save_to_db()

                # Only update Oracle for APPROVED, CONDITIONAL, DRAFT
                if next_state in [State.DRAFT, State.APPROVED, State.CONDITIONAL]:
                    # TODO: Uncomment this block
                    # warnings = nro.add_nr(nrd)
                    # if warnings:
                    #     MessageServices.add_message(MessageServices.ERROR, 'add_request_in_NRO', warnings)
                    #     return jsonify({'message': 'Error updating oracle. You must re-try'}), 500
                    # else:
                    # added the oracle request_id in new_nr, need to save it postgres
                    # set the furnished_flag='Y' for approved and conditionally approved
                    #     if request_data['stateCd'] in [State.APPROVED, State.CONDITIONAL]:
                    #         name_request.furnished='Y'

                    #     name_request.save_to_db()
                    #     EventRecorder.record(user, Event.POST, nrd, request_data)
                    pass

            except Exception as err:
                return handle_exception(err, 'Error saving nr and names.', 500)

        except Exception as err:
            return handle_exception(err, 'Error setting name.', 500)

    def _create_or_update_name(self, name):
        next_state = self.next_state_code

        try:
            submitted_name = Name()
            name_id = get_name_sequence()
            submitted_name.id = name_id
        except Exception as err:
            return handle_exception(err, 'Error on submitted_name and / or sequence.', 500)

        # Common name attributes
        try:
            submitted_name = self._map_submitted_name_attrs(submitted_name, name)
        except Exception as err:
            return handle_exception(err, 'Error on common name attributes.', 500)

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
                return handle_exception(err, 'Error on reserved conflict info.', 500)
        else:
            try:
                submitted_name.conflict1_num = None
                submitted_name.conflict1 = None
            except Exception as err:
                return handle_exception(err, 'Error on draft empty conflict info.', 500)

        consent_list = name['consent_words']
        if len(consent_list) > 0:
            for consent in consent_list:
                try:
                    cnd_instructions = None
                    if consent != '' or len(consent) > 0:
                        cnd_instructions = self.restricted_word_service.get_word_condition_instructions(consent)
                except Exception as err:
                    # TODO: Acceot a lambda as param for handle_exception
                    log_error('Error on get consent word. Consent Word[0], Error:{1}'.format(consent, err), err)
                    return jsonify({'message': 'Error on get consent words.'}), 500

                try:
                    if decision_text is None:
                        decision_text = cnd_instructions + '\n'
                    else:
                        decision_text += consent + '- ' + cnd_instructions + '\n'

                    submitted_name.decision_text = decision_text
                except Exception as err:
                    return handle_exception(err, 'Error adding consent words to decision.', 500)

        return submitted_name

    def _map_submitted_name_attrs(self, submitted_name, name):
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
                update_solr('possible.conflicts', solr_docs)
        except Exception as err:
            return handle_exception(err, 'Error updating solr for reservation.', 500)
