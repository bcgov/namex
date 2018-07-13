from flask_restplus import Namespace, Resource, fields
from flask import request, jsonify, current_app
from sqlalchemy import text
from api import db
from api.models import Request, User, State, Applicant, Comment, PartnerNameSystem, Name
import logging

api = Namespace('nroRequests', description='Name Request System - extracts legacy NRs and puts them into the new system')

log = logging.getLogger(__name__)


@api.route('/nro-requests', methods=['POST', 'OPTIONS'])
@api.response(404, 'NR not found')
class NRORequest(Resource):
    '''Expects a JSON:{"nameRequest": "NR 1234567"}
    fetches all the bits from the legacy NRO system and copies them into the new system
    Currently we copy directly into the NAMEX tables, but this is BAD. We shold be using the NAMEX-API
    but that requires some more complex setup on the KeyCloak side and skills/time prevents that at the moment.

    TODO: switch this to posting against the NAMEX service - this requires some KeyCloak setup that is not viable now
    '''

    a_request = api.model('Request', {'nameRequest': fields.String('A valid NR that exists in NRO')})

    @api.expect(a_request)
    def post(self, *args, **kwargs):
        json_input = request.get_json()
        if not json_input:
            return {"message": "No input data provided"}, 400

        nr_num = json_input['nameRequest']
        current_app.logger.debug('attempting to load: {}'.format(nr_num))
        if not validNRFormat(nr_num):
            return {"message": "Valid NR format required - 'NR 9999999'"}, 400


        if Request.find_by_nr(nr_num):
            return {"message": "{nr} already exists in namex, unable to create a duplicate".format(nr=nr_num)}, 409


        conn = db.get_engine(bind='nro')

        nr_header = get_nr_header(conn, nr_num)
        log.log(logging.DEBUG, 'nr_header: {}'.format(nr_header))
        if not nr_header:
            return {"message": "{nr} not found, unable to complete extraction to new system".format(nr=nr_num)}, 404


        nr_submitter = get_nr_submitter(conn, nr_header['request_id'])
        nr_applicant = get_nr_requester(conn, nr_header['request_id'])
        nr_ex_comments = get_exam_comments(conn, nr_header['request_id'])
        nr_nwpat = get_nwpta(conn, nr_header['request_id'])
        nr_names = get_names(conn, nr_header['request_id'])

        user = User.find_by_username(current_app.config['NRO_SERVICE_ACCOUNT'])

        #Create NR
        new_nr = Request()
        add_nr_header(new_nr, nr_header, nr_submitter, user)
        add_applicant(new_nr, nr_applicant)
        add_comments(new_nr, nr_ex_comments)
        add_nwpta(new_nr, nr_nwpat)
        add_names(new_nr, nr_names)

        new_nr.save_to_db()

        return {"message": "{nr} has been successfully copied".format(nr=nr_num)}, 200

def row_to_dict(row):
    return {key: value for (key, value) in row.items()}


def validNRFormat(nr):
    '''NR should be of the format "NR 1234567"
    '''

    if len(nr) != 10 or nr[:2] != 'NR' or nr[2:3] != ' ':
        return False

    try:
        num = int(nr[3:])
    except:
        return False

    return True

######### save stuff
def add_nr_header(new_nr, nr_header, nr_submitter, user):

    submitter = User.find_by_username(nr_submitter['submitter'])

    new_nr.userId = user.id
    new_nr.stateCd = State.DRAFT
    new_nr.nrNum = nr_header['nr_num']
    new_nr.requestId = nr_header['request_id']
    new_nr.previousRequestId = nr_header['previous_request_id']
    new_nr.submitCount = nr_header['submit_count']
    new_nr.requestTypeCd = nr_header['request_type_cd']
    new_nr.expirationDate = nr_header['expiration_date']
    new_nr.additionalInfo = nr_header['additional_info']
    new_nr.natureBusinessInfo = nr_header['nature_business_info']
    new_nr.xproJurisdiction = nr_header['xpro_jurisdiction']
    new_nr.submittedDate = nr_submitter['submitted_date']
    new_nr.submitter_userid = None if (submitter is None) else submitter.id
    if nr_header['priority_cd'] is 'PQ':
        new_nr.priorityCd = 'Y'
    else:
        new_nr.priorityCd = 'N'

def add_comments(new_nr, comments):
    # TODO: link to examiner IDs somehow - examiner_IDIR
    if comments:
        for c in comments:
            comm = Comment()
            comm.comment = c['examiner_comment']
            comm.timestamp = c['event_timestamp']

            new_nr.comments.append(comm)

def add_nwpta(new_nr, nr_nwpat):
    if nr_nwpat:
        for p in nr_nwpat:
            pns = PartnerNameSystem()
            pns.partnerNameTypeCd = p['partner_name_type_cd']
            pns.partnerNameNumber = p['partner_name_number']
            pns.partnerJurisdictionTypeCd = p['partner_jurisdiction_type_cd']
            pns.partnerNameDate = p['partner_name_date']
            pns.partnerName = p['partner_name']

            new_nr.partnerNS.append(pns)

def add_names(new_nr, nr_names):
    for n in nr_names:
        name = Name()
        name.state = Name.NOT_EXAMINED
        name.choice = n['choice_number']
        name.name = n['name']
        name.designation = n['designation']

        new_nr.names.append(name)

def add_applicant(new_nr, nr_applicant):
    applicant = Applicant()
    applicant.lastName = nr_applicant['last_name']
    applicant.firstName = nr_applicant['first_name']
    applicant.middleName = nr_applicant['middle_name']
    applicant.phoneNumber = nr_applicant['phone_number']
    applicant.faxNumber = nr_applicant['fax_number']
    applicant.emailAddress = nr_applicant['email_address']
    applicant.contact = nr_applicant['contact']
    applicant.clientFirstName = nr_applicant['client_first_name']
    applicant.clientLastName = nr_applicant['client_last_name']
    applicant.declineNotificationInd = nr_applicant['decline_notification_ind']
    applicant.addrLine1 = nr_applicant['addr_line_1']
    applicant.addrLine2 = nr_applicant['addr_line_2']
    applicant.addrLine3 = nr_applicant['addr_line_3']
    applicant.city = nr_applicant['city']
    applicant.postalCd = nr_applicant['postal_cd']
    applicant.stateProvinceCd = nr_applicant['state_province_cd']
    applicant.countryTypeCd = nr_applicant['country_type_cd']

    new_nr.applicants.append(applicant)


######### get stuff

def get_nr_header(conn, nr_num):
    # get the NR Header
    #############################
    sql = text(
        'set search_path to bc_registries_names;'
        'select  request_id,'
        'nr_num,'
        'previous_request_id,'
        'submit_count,'
        'priority_cd,'
        'request_type_cd,'
        'expiration_date,'
        'additional_info,'
        'nature_business_info,'
        'xpro_jurisdiction'
        ' from namex_request_vw'
        ' where nr_num = :nr'
    )
    result = conn.execute(sql.params(nr=nr_num), multi=True)
    row = result.fetchone()
    if row:
        return row_to_dict(row)
    return None

def get_nr_submitter(conn, request_id):

    # get the NR Submitter
    #############################
    sql = text(
        'set search_path to bc_registries_names;'
        'select submitted_date,'
        ' submitter'
        ' from namex_submitter_vw'
        ' where request_id = :req_id'
    )
    result = conn.execute(sql.params(req_id=request_id), multi=True)
    row = result.fetchone()
    log.log(logging.DEBUG, row_to_dict(row))
    if row:
        return row_to_dict(row)
    return None

def get_nr_requester(conn, request_id):

    # get the NR Requester
    #############################
    sql = text(
        'set search_path to bc_registries_names;'
        'select  request_id,'
        ' last_name,'
        ' first_name,'
        ' middle_name,'
        ' phone_number,'
        ' fax_number,'
        ' email_address,'
        ' contact,'
        ' client_first_name,'
        ' client_last_name,'
        ' decline_notification_ind,'
        ' addr_line_1,'
        ' addr_line_2,'
        ' addr_line_3,'
        ' city,'
        ' postal_cd,'
        ' state_province_cd,'
        ' country_type_cd'
        ' from namex_request_party_vw'
        ' where request_id = :req_id'
    )
    result = conn.execute(sql.params(req_id=request_id), multi=True)
    row = result.fetchone()
    log.log(logging.DEBUG, row_to_dict(row))
    if row:
        return row_to_dict(row)
    return None

def get_exam_comments(conn, request_id):
    # get the NR Requester
    #############################
    sql = text(
        'set search_path to bc_registries_names;'
        'select examiner_IDIR,'
        ' examiner_comment,'
        ' state_comment,'
        ' event_timestamp'
        ' from namex_examiner_comments_vw'
        ' where request_id= :req_id'
    )
    result = conn.execute(sql.params(req_id=request_id), multi=True)
    ex_comments = []
    for row in result:
        if row['examiner_comment'] or row['state_comment']:
            log.log(logging.DEBUG, row_to_dict(row))
            ex_comments.append(row_to_dict(row))
    if len(ex_comments) < 1:
        return None
    return ex_comments

def get_nwpta(conn, request_id):
    # get the NR NWPTA Partner information
    #############################
    sql = text(
        'set search_path to bc_registries_names;'
        'select partner_name_type_cd,'
        ' partner_name_number,'
        ' partner_jurisdiction_type_cd,'
        ' partner_name_date,'
        ' partner_name,'
        ' last_update_id'
        ' from partner_name_system pns'
        ' where end_event_id IS NULL'
        ' and pns.request_id= :req_id'
    )
    result = conn.execute(sql.params(req_id=request_id), multi=True)
    nwpta = []
    for row in result:
        log.log(logging.DEBUG, row_to_dict(row))
        nwpta.append(row_to_dict(row))
    if len(nwpta) < 1:
        return None
    return nwpta

def get_names(conn, request_id):
    # get the NR Names
    #############################
    sql = text(
        'set search_path to bc_registries_names;'
        'select choice_number,'
        ' name,'
        ' designation'
        ' from namex_names_vw'
        ' where request_id = :req_id'
    )
    result = conn.execute(sql.params(req_id=request_id), multi=True)
    names = []
    for row in result:
        log.log(logging.DEBUG, row_to_dict(row))
        names.append(row_to_dict(row))
    if len(names) < 1:
        return None
    return names

