from flask_restplus import Namespace, Resource, fields
from flask import request, jsonify, current_app, g
from sqlalchemy import text
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from api import db
from namex.models import Request, User, State, Applicant, Comment, PartnerNameSystem, Name, Event
from namex.services import EventRecorder

import sys

api = Namespace('nroRequests', description='Name Request System - extracts legacy NRs and puts them into the new system')


@api.route('/nro-requests', methods=['POST', 'PUT', 'OPTIONS'])
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
        """this creates a new Request in NameX from data in the NRO system
        calls: transfer_NRO_records_to_NameX with UPDATE=FALSE
        :returns: (json): the NR of the request if 200
        :returns: 200, 403, 409, 500
        """
        return self.transfer_nro_records_to_namex(update=False, *args, **kwargs)

    @api.expect(a_request)
    def put(self, *args, **kwargs):
        """this updates an existing Request in NameX from data in the NRO system
        calls: transfer_NRO_records_to_NameX with UPDATE=TRUE
        :returns: (json): the NR of the request if 200
        :returns: 200, 403, 409, 500
        """
        return self.transfer_nro_records_to_namex(update=True, *args, **kwargs)

    def transfer_nro_records_to_namex(self, update=False, *args, **kwargs):
        """

        :param update: (bool)
        :param args: __future__
        :param kwargs:  __future__
        :returns: (json): the NR of the request if 200
        :returns: 200, 403, 409, 500
        """
        json_input = request.get_json()
        if not json_input:
            return {"message": "No input data provided"}, 400

        nr_num = json_input['nameRequest']
        current_app.logger.debug('attempting to load: {}, update:{}'.format(nr_num, update))
        if not validNRFormat(nr_num):
            return {"message": "Valid NR format required - 'NR 9999999'"}, 400

        # open a connection to the NRO bind
        nro_session = db.get_engine(bind='nro').connect()
        g.db_nro_session = nro_session

        try:
            existing_nr = Request.find_by_nr(nr_num)
            if existing_nr and not update:
                return {"message": "{nr} already exists in namex, unable to create a duplicate".format(nr=nr_num)}, 409

            if update and not existing_nr:
                return {"message": "{nr} doesn't exist in namex, unable to update it.".format(nr=nr_num)}, 409

            # get the header from NRO, if it's not there, bail
            nr_header = get_nr_header(nro_session, nr_num)
            if not nr_header:
                return {"message": "{nr} not found in NRO, unable to complete extraction to new system".format(nr=nr_num)}, 404
            current_app.logger.debug('nr_header: {}'.format(nr_header))

            # get the service account user to save BRO Requests
            user = User.find_by_username(current_app.config['NRO_SERVICE_ACCOUNT'])

            # process a POST (aka create)
            if not update:
                nrd = self._copy_nr(user, nro_session, nr_header, existing_nr, update)
                EventRecorder.record(user, Event.POST, nrd, json_input)
                return {"message": "{nr_num} has been successfully copied".format(nr_num=nr_num)}, 200

            # cancel the NR
            if update and nr_header['state_type_cd'] == 'C':
                existing_nr.stateCd = State.CANCELLED
                db.session.add(existing_nr)
                db.session.commit()
                EventRecorder.record(user, Event.PUT, existing_nr, json_input)
                return {"message": "{nr} is cancelled".format(nr=nr_num)}, 200

            # update the NR if NameX allows
            if update and (
                    (existing_nr.stateCd == State.DRAFT)
                    or (nr_header['state_type_cd'] == 'H' and existing_nr.stateCd == State.NRO_UPDATING)
            ):
                self._copy_nr(user, nro_session, nr_header, existing_nr, update)
                EventRecorder.record(user, Event.PUT, existing_nr, json_input)
                return {"message": "{nr_num} has been successfully updated".format(nr_num=nr_num)}, 200

            else:
                return {"message": "Unable to update {nr}".format(nr=nr_num)}, 404

        except Exception as err:
            current_app.logger.error(err.with_traceback(err.__traceback__))
            db.session.rollback()
            return {"message": "Internal server error"}, 500

        finally:
            if nro_session:
                nro_session.close()

    def _copy_nr(self, user, nro_session, nr_header, existing_nr, update):
        """Utility function to gather up and copy across the Name Request data segments
        """
        # get all the request segments from NRO
        nr_submitter = get_nr_submitter(nro_session, nr_header['request_id'])
        nr_applicant = get_nr_requester(nro_session, nr_header['request_id'])
        nr_ex_comments = get_exam_comments(nro_session, nr_header['request_id'])
        nr_nwpat = get_nwpta(nro_session, nr_header['request_id'])
        nr_names = get_names(nro_session, nr_header['request_id'])

        current_app.logger.debug('completed all gets')

        # Create or Update the NR
        if existing_nr and update:
            nr = existing_nr
        else:
            nr = Request()

        add_nr_header(nr, nr_header, nr_submitter, user, update)
        if nr_applicant:
            add_applicant(nr, nr_applicant, update)
            current_app.logger.debug('completed applicants for {}'.format(nr.nrNum))
        if nr_ex_comments:
            add_comments(nr, nr_ex_comments, update)
            current_app.logger.debug('completed comments for {}'.format(nr.nrNum))
        if nr_nwpat:
            add_nwpta(nr, nr_nwpat, update)
            current_app.logger.debug('completed nwpta for {}'.format(nr.nrNum))
        if nr_names:
            add_names(nr, nr_names, update)
            current_app.logger.debug('completed names for {}'.format(nr.nrNum))

        current_app.logger.debug('saving the {} graph to the database, updating?:{}'.format(nr.nrNum, update))
        db.session.add(nr)
        db.session.commit()
        return nr

# ### UTILITY FUNCTIONS #########################################

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


# ######## save stuff
def add_nr_header(nr, nr_header, nr_submitter, user, update=False):

    NR_STATE={
        'HISTORICAL': 'HISTORICAL',
        'H': 'HOLD',
        'COMPLETED': 'COMPLETED',
        'D': 'DRAFT',
        'C': 'CANCELLED',
        'E': 'EXPIRED'
    }

    if nr_submitter:
        submitter = User.find_by_username(nr_submitter['submitter'])

    nr.userId = user.id
    nr.stateCd = State.DRAFT if nr_header['state_type_cd'] is None else NR_STATE[nr_header['state_type_cd']]
    nr.nrNum = nr_header['nr_num']
    nr.requestId = nr_header['request_id']
    nr.previousRequestId = nr_header['previous_request_id']
    nr.submitCount = nr_header['submit_count']
    nr.requestTypeCd = nr_header['request_type_cd']
    nr.expirationDate = nr_header['expiration_date']
    nr.additionalInfo = nr_header['additional_info']
    nr.natureBusinessInfo = nr_header['nature_business_info']
    nr.xproJurisdiction = nr_header['xpro_jurisdiction']
    nr.submittedDate = nr_submitter['submitted_date']
    nr.submitter_userid = None if (submitter is None) else submitter.id
    nr.nroLastUpdate = nr_header['last_update']
    nr.lastUpdate = nr.nroLastUpdate # this needs to be set to the same Point In Time as NRO until NameX owns it

    if nr_header['priority_cd'] is 'PQ':
        nr.priorityCd = 'Y'
    else:
        nr.priorityCd = 'N'


def add_comments(nr, comments, update=False):
    # TODO: link to examiner IDs somehow - examiner_IDIR
    # TODO: append new comments, rather than flushing out all the old ones first
    if update:
        for com in nr.comments.all():
            nr.comments.remove(com)

    if comments:
        for c in comments:
            comm = Comment()
            comm.comment = c['examiner_comment']
            comm.timestamp = c['event_timestamp']

            nr.comments.append(comm)


def add_nwpta(nr, nr_nwpat, update=False):

    # naive approach, if updating remove all the old PNS'es
    # TODO change to an update / delete / insert flow
    if update:
        for pn in nr.partnerNS.all():
            nr.partnerNS.remove(pn)

    if nr_nwpat:
        for p in nr_nwpat:
            pns = PartnerNameSystem()
            pns.partnerNameTypeCd = p['partner_name_type_cd']
            pns.partnerNameNumber = p['partner_name_number']
            pns.partnerJurisdictionTypeCd = p['partner_jurisdiction_type_cd']
            pns.partnerNameDate = p['partner_name_date']
            pns.partnerName = p['partner_name']

            nr.partnerNS.append(pns)


def add_names(nr, nr_names, update=False):
    NAME_STATE={
        'NE': Name.NOT_EXAMINED,
        'A': Name.APPROVED,
        'R': Name.REJECTED,
        'C': Name.CONDITION
    }
    # naive approach
    # TODO change to an update / delete / insert flow
    if update:
        # remove all names
        for ne in nr.names.all():
            nr.names.remove(ne)

    # add in the names from this request
    for n in nr_names:
        name = Name()
        name.state = Name.NOT_EXAMINED if n['name_state_type_cd'] is None else NAME_STATE[n['name_state_type_cd']]
        name.choice = n['choice_number']
        name.name = n['name']
        name.designation = n['designation']

        nr.names.append(name)


def add_applicant(nr, nr_applicant, update=False):

    if update:
        applicant = nr.applicants
        # TODO: can an existing NR ever not have applicants?
    else:
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

    if not update:
        nr.applicants.append(applicant)


# ######## Fetch Current NRO Information ##########################################

def get_nr_header(session, nr_num):
    # get the NR Header
    #############################
    sql_nr = text(
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
        ' from request_vw'
        ' where nr_num = :nr'
    )
    sql_lu = text(
        'set search_path to bc_registries_names;'
        'select last_update'
        ' from req_instance_max_event'
        ' where request_id = :id'
    )
    sql_state = text(
        'set search_path to bc_registries_names;'
        'select rs.state_type_cd'
        ' from request_state_vw rs'
        ' where rs.request_id = :req_id'
        ' and rs.end_event_id IS NULL'
    )
    result = session.execute(sql_nr.params(nr=nr_num), multi=True)
    row = result.fetchone()
    result.close()

    #get main row
    if row:
        nr = row_to_dict(row)

        # get last_updated
        result = session.execute(sql_lu.params(id=nr['request_id']), multi=True)
        row = result.fetchone()
        if row:
            nr = {**nr, **(row_to_dict(row))}

        # get state
        result = session.execute(sql_state.params(req_id=nr['request_id']), multi=True)
        row = result.fetchone()
        if row:
            nr = {**nr, **(row_to_dict(row))}

        return nr

    return None

def get_nr_submitter(session, request_id):

    # get the NR Submitter
    #############################
    sql = text(
        'set search_path to bc_registries_names;'
        'select submitted_date,'
        ' submitter'
        ' from submitter_vw'
        ' where request_id = :req_id'
    )
    result = session.execute(sql.params(req_id=request_id), multi=True)
    row = result.fetchone()
    if row:
        current_app.logger.debug(row_to_dict(row))
        return row_to_dict(row)
    return None

def get_nr_requester(session, request_id):

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
        ' from request_party_vw'
        ' where request_id = :req_id'
    )
    result = session.execute(sql.params(req_id=request_id), multi=True)
    row = result.fetchone()
    if row:
        current_app.logger.debug(row_to_dict(row))
        return row_to_dict(row)
    return None

def get_exam_comments(session, request_id):
    # get the NR Requester
    #############################
    sql = text(
        'set search_path to bc_registries_names;'
        'select examiner_IDIR,'
        ' examiner_comment,'
        ' state_comment,'
        ' event_timestamp'
        ' from examiner_comments_vw'
        ' where request_id= :req_id'
    )
    result = session.execute(sql.params(req_id=request_id), multi=True)
    ex_comments = []
    for row in result:
        if row['examiner_comment'] or row['state_comment']:
            current_app.logger.debug(row_to_dict(row))
            ex_comments.append(row_to_dict(row))
    if len(ex_comments) < 1:
        return None
    return ex_comments

def get_nwpta(session, request_id):
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
        ' from partner_name_system_vw pns'
        ' where end_event_id IS NULL'
        ' and pns.request_id= :req_id'
    )
    result = session.execute(sql.params(req_id=request_id), multi=True)
    nwpta = []
    for row in result:
        current_app.logger.debug(row_to_dict(row))
        nwpta.append(row_to_dict(row))
    if len(nwpta) < 1:
        return None
    return nwpta

def get_names(session, request_id):
    # get the NR Names
    #############################
    sql = text(
        'set search_path to bc_registries_names;'
        'select choice_number,'
        ' name,'
        ' designation,'
        ' name_state_type_cd'
        ' from names_vw'
        ' where request_id = :req_id'
    )
    result = session.execute(sql.params(req_id=request_id), multi=True)
    names = []
    for row in result:
        current_app.logger.debug(row_to_dict(row))
        names.append(row_to_dict(row))
    if len(names) < 1:
        return None
    return names

