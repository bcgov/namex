from flask import jsonify
from namex.models import db
from datetime import timedelta
from pytz import timezone
import os, pysolr

from namex.utils.logging import setup_logging

from datetime import datetime

from namex.models import NRNumber, Comment, Applicant

from namex.services.name_request import convert_to_ascii

from namex.constants import request_type_mapping

setup_logging()  # Important to do this first


def log_error(msg, err):
    return msg.format(err)


def handle_exception(err, msg, err_code):
    log_error(msg + ' Error:{0}', err)
    return jsonify(message=msg), err_code


def set_request_type(entity_type, request_action):
    for item in request_type_mapping:
        if item[1] == entity_type and item[2] == request_action:
            output = item
            break
    request_type = list(output)
    return request_type[0]


def create_expiry_date(start: datetime, expires_in_days: int, expiry_hour: int = 23, expiry_min: int = 59,
                       tz: timezone = timezone('US/Pacific')) -> datetime:

    date = (start.astimezone(tz) + timedelta(days=expires_in_days)) \
        .replace(hour=expiry_hour, minute=expiry_min, second=0, microsecond=0)

    return date


def update_solr(core, solr_docs):
    SOLR_URL = os.getenv('SOLR_BASE_URL')
    solr = pysolr.Solr(SOLR_URL+'/solr/' + core + '/', timeout=10)
    solr.add(solr_docs, commit=True)


def get_request_sequence():
    seq = db.Sequence('requests_id_seq')
    nr_id = db.engine.execute(seq)
    return nr_id


def get_applicant_sequence():
    seq = db.Sequence('applicants_party_id_seq')
    party_id = db.engine.execute(seq)
    return party_id


def get_name_sequence():
    seq = db.Sequence('names_id_seq')
    name_id = db.engine.execute(seq)
    return name_id


def generate_nr():
    r = db.session.query(NRNumber).first()
    if r is None:
        # Set starting nr number
        last_nr = 'NR L000000'
    else:
        last_nr = r.nrNum
        # TODO: Add a check wheN the number has reached 999999
        # and you need to roll over to the next letter in the alphabet and reset the number to 000000

    nr_num = NRNumber.get_next_nr_num(last_nr)
    r.nrNum = nr_num
    r.save_to_db()
    # TODO: Add a check that it updated
    return nr_num


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


def map_request_attributes(name_request, request_data, user_id):
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


def map_request_applicants(request_data, nr_id):
    # Applicant, contact and address info
    applicants = []
    for request_applicant in request_data.get('applicants', []):
        applicant = Applicant()
        party_id = get_applicant_sequence()
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

        applicants.append(applicant)

    return applicants


class AbstractNameRequestMixin(object):
    @property
    def request_data(self):
        return self._request_data

    @request_data.setter
    def request_data(self, data):
        self._request_data = data

    @property
    def next_state_code(self):
        return self.request_data.get('stateCd', None)

    @property
    def request_action(self):
        return self.request_data.get('request_action', None)

    @property
    def request_entity(self):
        return self.request_data.get('entity_type', None)

    @property
    def request_names(self):
        return self.request_data.get('names', None)

    @property
    def nr_num(self):
        return self._nr_num

    @nr_num.setter
    def nr_num(self, val):
        self._nr_num = val

    @property
    def nr_id(self):
        return self._nr_id

    @nr_id.setter
    def nr_id(self, val):
        self._nr_id = val

    def generate_nr_keys(self):
        try:
            # temp Nr # until one is generated in oracle
            self.nr_num = generate_nr()
            self.nr_id = get_request_sequence()
        except Exception as err:
            return handle_exception(err, 'Error getting nr number.', 500)

        return self.nr_num, self.nr_id
