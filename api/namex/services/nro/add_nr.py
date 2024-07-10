"""add the Name Request Record in NRO from the current record state in NameRequest

   In order to maintain the NRO data patterns, the record adds will follow
   the following pattern:
   -- request header
   create the  NR #
   insert into request
   create new event of type 'SYST'
   create new transaction of type 'NRREQ' using the event_id
   using Name request service account 'name_request_service_account' as STAFF_IDIR
   create the request_instance using the event_id
   create the request_party using the event_id and address insert using the event_id
   create the request_state using the event_id
   -- names
   create the name
   create the name_instance using the event_id for each name
   create the name_state using the event_id for each name



   Each main segment has its own function call to facilitate testing,
   but the main function call is new_nr

"""

from flask import current_app, jsonify, make_response
from .utils import generate_compressed_name
from namex.services.nro.change_nr import _get_event_id, _create_nro_transaction
from namex.services.name_request.generate_new_nr_number import NRNumberService
from namex.models import State
import cx_Oracle


def new_nr(nr, ora_cursor, con):
    """Add the Name Request in NRO
    :raises Exception: what ever error we get, let our caller handle, this is here in case we want to wrap it - future
    """

    nr_num = NRNumberService.get_new_nr_num()
    # Set postgres to real NR #
    nr.nrNum = nr_num

    #set the oracle version of the priority code
    priority = None
    if nr.priorityCd == 'Y':
        priority = 'PQ'
    else:
        priority = 'RQ'

    request_id = _create_request(ora_cursor, nr_num)
    nr.requestId = request_id
    current_app.logger.debug('got to new_nr() for NR:{}'.format(nr_num))

    eid = _get_event_id(ora_cursor)
    current_app.logger.debug('event ID for NR:{1}. event id:{0}'.format(eid, nr_num))

    nr.requestId = request_id
    _create_nro_transaction(ora_cursor, nr, eid, transaction_type='NRREQ')
    con.commit()
    current_app.logger.debug('Created the transaction for new_nr() for NR:{}'.format(nr_num))

    _create_request_instance(ora_cursor, nr, eid, priority)
    con.commit()
    if not (applicant_info := nr.applicants):
        current_app.logger.error("Error on getting applicant info.")
        return make_response(jsonify({"Message": "No applicant info"}), 404)

    _create_request_party(ora_cursor, applicant_info[0], eid, request_id)  # includes address
    con.commit()
    current_app.logger.debug('Created Request Party and Address in new_nr() for NR:{}'.format(nr_num))

    _create_request_state(ora_cursor, 'D', eid, request_id)
    con.commit()

    _create_names(ora_cursor, nr, eid) #name, name_instace and name state
    con.commit()
    current_app.logger.debug('Created Names in new_nr() for NR:{}'.format(nr_num))

    # for completed NRs waiting for the updater set the state to H so no one can change it in NRO
    # for Name request Rserved and conditionally Reersved NRs.
    if nr.stateCd in [State.RESERVED, State.COND_RESERVE]:
        eid = _get_event_id(ora_cursor)
        set_request_on_hold(ora_cursor, request_id, eid)
        con.commit()
        current_app.logger.debug('Set State to ONHOLD for Updater to Run in new_nr() for NR:{}'.format(nr_num))

    current_app.logger.debug('got to the end of new_nr() for NR:{}'.format(nr_num))

def _create_request(oracle_cursor, nr_num):
    l_output=None
    l_output = oracle_cursor.var(cx_Oracle.NUMBER)
    l_request_id = 0
    try:
        # create new request record
        oracle_cursor.execute("""
            INSERT INTO request(request_id, nr_num, submit_count)
            VALUES (request_seq.nextval, :nr_num, :submit_count)
            RETURNING request_id INTO :out
            """,
                nr_num=nr_num,
                submit_count=1,
                out=l_output
            )
        current_app.logger.debug('request record created')
        l_request_id = l_output.values[0][0]
        return int(l_request_id)

    except Exception as error:
        current_app.logger.error("Error on adding request record for NR:{0}'. Error:{1}".format(nr_num, error))
        return make_response(jsonify({"Message": "Error on adding request record in oracle"}), 404)

def  _create_request_instance(oracle_cursor, nr, eid,priority):
    try:
        oracle_cursor.execute("""
                    INSERT INTO request_instance(request_instance_id, request_id,priority_cd, request_type_cd,
                    expiration_date, start_event_id, xpro_jurisdiction,additional_info, nature_business_info, home_juris_num)
                VALUES (request_instance_seq.nextval, :request_id, :priority_cd, :request_type_cd, 
                      :expiration_date, :start_event_id, upper(:xpro_jurisdiction), :additional_info, :nature_business_info, :home_juris_num)
                """,
                          request_id=nr.requestId,
                          priority_cd=priority,
                          request_type_cd=nr.requestTypeCd,
                          expiration_date=nr.expirationDate,
                          start_event_id=eid,
                          xpro_jurisdiction=nr.xproJurisdiction,
                          additional_info=nr.additionalInfo,
                          nature_business_info=nr.natureBusinessInfo,
                          home_juris_num=nr.homeJurisNum
                          )
        current_app.logger.debug('request instance record created')
    except Exception as error:
        current_app.logger.error("Error on adding request record for NR:{0}'. Error:{1}".format(nr.nrNum, error))
        return make_response(jsonify({"Message": "Error on adding request instance record in oracle"}), 404)

def   _create_request_party(oracle_cursor, applicantInfo, eid, request_id):
    # get next address ID
    oracle_cursor.execute("""select address_seq.NEXTVAL@global_address from dual""")
    row = oracle_cursor.fetchone()
    address_id = int(row[0])

    # create new address record
    oracle_cursor.execute("""
    INSERT INTO address@global_address(addr_id, application_cd, state_province_cd, postal_cd, addr_line_1, addr_line_2, addr_line_3, city, country_type_cd)
    VALUES (:addr_id, :application_cd, :state_province_cd, :postal_cd, :addr_line_1, :addr_line_2, :addr_line_3, :city, :country_type_cd)
    """,
                          addr_id=address_id,
                          application_cd='AB',
                          state_province_cd=applicantInfo.stateProvinceCd,
                          postal_cd=applicantInfo.postalCd,
                          addr_line_1=applicantInfo.addrLine1,
                          addr_line_2=applicantInfo.addrLine2,
                          addr_line_3=applicantInfo.addrLine3,
                          city=applicantInfo.city,
                          country_type_cd=applicantInfo.countryTypeCd
                          )

    #create request_party
    # create new record for request party instance
    oracle_cursor.execute("""
            INSERT INTO request_party (party_id, request_id, party_type_cd, last_name, first_name, middle_name, 
                        phone_number, fax_number, email_address, address_id, start_event_id, contact, 
                        client_first_name, client_last_name) 
            VALUES (request_party_seq.nextval, :request_id, 'APP', :last_name, :first_name, :middle_name, 
                    :phone_number, :fax_number, :email_address, :address_id, :start_event_id, :contact, 
                    :client_first_name, :client_last_name)
            """,
                          request_id=request_id,
                          last_name=applicantInfo.lastName,
                          first_name=applicantInfo.firstName,
                          middle_name=applicantInfo.middleName,
                          phone_number=applicantInfo.phoneNumber,
                          fax_number=applicantInfo.faxNumber,
                          email_address=applicantInfo.emailAddress,
                          address_id=address_id,
                          start_event_id=eid,
                          contact=applicantInfo.contact,
                          client_first_name=applicantInfo.clientFirstName,
                        client_last_name=applicantInfo.clientLastName
                          )

def  _create_request_state(oracle_cursor, new_state,eid,request_id):

    # create new request_state record
    oracle_cursor.execute("""
            INSERT INTO request_state (request_state_id, request_id, state_type_cd, start_event_id, state_comment)
            VALUES (request_state_seq.nextval, :request_id, :state_type_cd, :start_event_id, NULL)
            """,
                          request_id=request_id,
                          state_type_cd=new_state,
                          start_event_id=eid,

                          )


def  _create_names(oracle_cursor, nr, eid):
    name_count = len(nr.names)
    if name_count == 0:
        current_app.logger.error("Error on getting names for NR:{0}".format(nr.nrNum))
        return make_response(jsonify({"Message": "Error getting names"}), 404)

    for name in nr.names:
        oracle_cursor.execute("""select name_seq.NEXTVAL from dual""")
        row = oracle_cursor.fetchone()
        n_id = int(row[0])

        oracle_cursor.execute("""
                       INSERT INTO name (NAME_ID, REQUEST_ID)
                       VALUES (:name_id, :request_id)
                       """,
                              name_id=n_id,
                              request_id=nr.requestId)

        oracle_cursor.execute("""
                      INSERT INTO name_state (name_state_id, name_id, start_event_id, name_state_type_cd)
                      VALUES (name_state_seq.NEXTVAL, :name_id, :start_event_ID, 'NE')
                      """,
                              name_id=n_id,
                              start_event_id=eid)
        if name.name:
            oracle_cursor.execute("""
                   INSERT INTO name_instance (name_instance_id, name_id, choice_number, name, start_event_id, search_name, designation)
                   VALUES (name_instance_seq.nextval, :name_id, :choice, :name, :start_event_id, :search_name, :designation)
                   """,
                              name_id=n_id,
                              choice=name.choice,
                              name=name.name,
                              start_event_id=eid,
                              search_name=generate_compressed_name(name.name),
                              designation = name.designation)

def set_request_on_hold(oracle_cursor, request_id,eid):
    # set the end event for the existing record
    oracle_cursor.execute("""
            UPDATE request_state
            SET end_event_id = :event_id
            WHERE request_id = :request_id
            AND end_event_id IS NULL
            """,
                          event_id=eid,
                          request_id=request_id)

    # create new request_state record
    oracle_cursor.execute("""
           INSERT INTO request_state (request_state_id, request_id, state_type_cd, 
               start_event_id,end_event_id)
           VALUES (request_state_seq.nextval, :request_id, 'H', :start_event_id,NULL)
           """,
                          request_id=request_id,
                          start_event_id=eid
                          )
