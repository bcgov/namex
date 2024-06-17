"""update the Name Request Record in NRO from the current record state in NameX

   In order to maintain the NRO data patterns, the record updates will follow
   the following pattern:

   create new event of type 'SYST'
   create new transaction of type 'ADMIN' or 'CORRT'
   using STAFF_IDIR of 'namex'

   Each main segment has its own function call to facilitate testing,
   but the main function call is update_nr

"""

from datetime import datetime
from flask import current_app
from .utils import generate_compressed_name, nro_examiner_name
from namex.models import State
import pytz

def update_nr(nr, ora_cursor, change_flags, con):
    """Update the Name Request in NRO
    :raises Exception: what ever error we get, let our caller handle, this is here in case we want to wrap it - future
    """

    priority = None
    if nr.priorityCd == 'Y':
        priority = 'PQ'
    else:
        priority = 'RQ'

    eid = _get_event_id(ora_cursor)
    current_app.logger.debug('got to update_nr() for NR:{}'.format(nr.nrNum))
    current_app.logger.debug('event ID for NR Details edit:{}'.format(eid))
    _create_nro_transaction(ora_cursor, nr, eid, transaction_type='CORRT')
    con.commit()

    _update_nro_request_state(ora_cursor, nr, eid, change_flags)
    con.commit()

    _update_request(ora_cursor, nr, eid, change_flags, priority)
    con.commit()

    _update_nro_names(ora_cursor, nr, eid, change_flags)
    con.commit()

    _update_nro_address(ora_cursor, nr, eid, change_flags)
    _update_nro_partner_name_system(ora_cursor, nr, eid, change_flags)
    _update_consent(ora_cursor, nr, eid, change_flags)
    con.commit()

    current_app.logger.debug('got to the end of update_nr()')


def _get_event_id(oracle_cursor):  # -> (int)
    """gets the event_id to be used for updating the NR history
    :oracle_conn : a Cx_Oracle connection to the NRO database
    :returns (int): a valid NRO event_id to be used for updating NRO records
    """

    oracle_cursor.execute("""select event_seq.NEXTVAL from dual""")
    row = oracle_cursor.fetchone()

    event_id = int(row[0])

    oracle_cursor.execute("""
    INSERT INTO event (event_id, event_type_cd, event_timestamp)
      VALUES (:event_id, 'SYST', sysdate)
    """,
                          event_id=event_id
    )

    return event_id


def _create_nro_transaction(oracle_cursor, nr, event_id, transaction_type='ADMIN'):

    oracle_cursor.execute("""
    INSERT INTO transaction (transaction_id, request_id, transaction_type_cd, event_id, staff_idir)
      VALUES (transaction_seq.nextval, :request_id, :transaction_type, :event_id, 'namex')
    """,
                          request_id=nr.requestId,
                          transaction_type=transaction_type,
                          event_id=event_id
                          )
    current_app.logger.debug('transaction record created')


def _update_nro_request_state(oracle_cursor, nr, event_id, change_flags):
    """ Update the current request state. Can be used to set to any state except H. Mainly used to
        set to Draft after edits pre-examination.

        Only handles setting NR to following states in NRO:
            D (Draft)
    """

    if 'is_changed__request_state' in change_flags.keys() and change_flags['is_changed__request_state']:

        new_state = None
        if nr.stateCd == State.DRAFT:
            new_state = 'D'
        else:
            return

        # set the end event for the existing record
        oracle_cursor.execute("""
        UPDATE request_state
        SET end_event_id = :event_id
        WHERE request_id = :request_id
        AND end_event_id IS NULL
        """,
                       event_id=event_id,
                       request_id=nr.requestId)

        # create new request_state record
        oracle_cursor.execute("""
        INSERT INTO request_state (request_state_id, request_id, state_type_cd, 
            start_event_id, end_event_id, examiner_idir, examiner_comment, state_comment, 
            batch_id)
        VALUES (request_state_seq.nextval, :request_id, :state, :event_id, NULL, 
                  :examiner_id, NULL, NULL, NULL)
        """,
                       request_id=nr.requestId,
                       state=new_state,
                       event_id=event_id,
                       examiner_id=nro_examiner_name(nr.activeUser.username)
                       )


def format_datetime(timestamp_datetime):
    """format datetime from python to oracle format
    """
    # Parse the string to a datetime object
    if timestamp_datetime is not None:
        timestamp_datetime_pacific = timestamp_datetime.astimezone(pytz.timezone('US/Pacific'))
        # Format the datetime object as per the Oracle date format
        formatted_timestamp = timestamp_datetime_pacific.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_timestamp
    else:
        print("Error: timestamp_datetime is None.")
        return None


def _update_request(oracle_cursor, nr, event_id, change_flags, priority):
    """ Update the current request instance.
    """

    if change_flags['is_changed__request']:
        # get request_instance record, with all fields
        oracle_cursor.execute("""
        SELECT *
        FROM request_instance
        WHERE request_id = :request_id
        AND end_event_id IS NULL
        FOR UPDATE
        """,
                              request_id=nr.requestId)
        row = oracle_cursor.fetchone()
        req_inst_id = int(row[0])

        # set the end event for the existing record
        oracle_cursor.execute("""
        UPDATE request_instance
        SET end_event_id = :event_id
        WHERE request_instance_id = :req_inst_id
        """,
                              event_id=event_id,
                              req_inst_id=req_inst_id)

        formated_expiration_date = format_datetime(nr.expirationDate)
        # create cursor for env
        # create new request_instance record
        oracle_cursor.execute("""
            INSERT INTO request_instance(request_instance_id, request_id,priority_cd, request_type_cd,
            expiration_date, start_event_id, tilma_ind, xpro_jurisdiction,
            nuans_expiration_date, queue_position, additional_info, nature_business_info,
            user_note, nuans_num, tilma_transaction_id, assumed_nuans_num, assumed_nuans_name,
            assumed_nuans_expiration_date, last_nuans_update_role, admin_comment, home_juris_num)
            VALUES (request_instance_seq.nextval, :request_id, :priority_cd, :request_type_cd,
                  to_date(:expiration_date, 'YYYY-MM-DD HH24:MI:SS'), :event_id, :tilma_ind, :xpro_jurisdiction,
                  :nuans_expiration_date, :queue_position, :additional_info, :nature_business_info,
                  :user_note, :nuans_num, :tilma_transaction_id, :assumed_nuans_num,
                  :assumed_nuans_name, :assumed_nuans_expiration_date, :last_nuans_updated_role,
                  :admin_comment, :home_juris_num)
            """,
                              request_id=nr.requestId,
                              priority_cd=priority,
                              request_type_cd=nr.requestTypeCd,
                              expiration_date=formated_expiration_date,
                              event_id=event_id,
                              tilma_ind=row[7],
                              xpro_jurisdiction=nr.xproJurisdiction,
                              nuans_expiration_date=row[9],
                              queue_position=row[10],
                              additional_info=nr.additionalInfo,
                              nature_business_info=nr.natureBusinessInfo,
                              user_note=row[13],
                              nuans_num=row[14],
                              tilma_transaction_id=row[15],
                              assumed_nuans_num=row[16],
                              assumed_nuans_name=row[17],
                              assumed_nuans_expiration_date=row[18],
                              last_nuans_updated_role=row[19],
                              admin_comment=row[20],
                              home_juris_num=nr.homeJurisNum
                              )


def _update_nro_names(oracle_cursor, nr, event_id, change_flags):
    """find the current name instance, set it's end_event_id to event_id
       if the name was deleted, nothing more needs to be done.
       otherwise, create a new name_instance and set its start_event_id to event_id
    """

    name_map = {1: None, 2: None, 3: None}
    for name in nr.names:
        name_map[name.choice] = name

    for choice in range(1, 4):
        name = name_map[choice]

        if (choice == 1 and change_flags['is_changed__name1']) or \
           (choice == 2 and change_flags['is_changed__name2']) or \
           (choice == 3 and change_flags['is_changed__name3']):

            oracle_cursor.execute("""
            SELECT ni.name_instance_id, ni.name_id
            FROM name_instance ni
            LEFT OUTER JOIN name nm ON nm.name_id = ni.name_id
            WHERE nm.request_id = :request_id
            AND ni.choice_number = :choice
            AND ni.end_event_id IS NULL
            FOR UPDATE
            """,
                                  request_id=nr.requestId,
                                  choice=choice)
            row = oracle_cursor.fetchone()

            # if there was a result, this is an existing name record
            if row:

                ni_id = int(row[0])
                n_id = int(row[1])

                oracle_cursor.execute("""
                UPDATE name_instance
                SET end_event_id = :event_id
                WHERE name_instance_id = :instance_id
                """,
                                      event_id=event_id,
                                      instance_id=ni_id)

                # If the name is deleted or missing, do not insert new name_instance record
                if name is None or name.name is None:
                    continue

            else:
                # this is a new name, so create a new NAME and NAME_STATE record

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
                VALUES (name_state_seq.NEXTVAL, :name_id, :start_event, 'NE')
                """,
                                      name_id=n_id,
                                      start_event=event_id)

            # If the new name is not blank, do this:
            if name and name.name:
                oracle_cursor.execute("""
                INSERT INTO name_instance (name_instance_id, name_id, choice_number, name, start_event_id, search_name)
                VALUES (name_instance_seq.nextval, :name_id, :choice, :name, :event_id, :search_name)
                """,
                                      name_id=n_id,
                                      choice=name.choice,
                                      name=name.name,
                                      event_id=event_id,
                                      search_name=generate_compressed_name(name.name))


def _update_nro_address(oracle_cursor, nr, event_id, change_flags):
    """find the current address (request_party), set it's end_event_id to event_id
       create a new request_party and set it start_event_id to event_id
       Also add record to address table in global db.
    """
    if not nr.applicants:
        return
    applicant_info = nr.applicants[0]

    if change_flags['is_changed__applicant'] or change_flags['is_changed__address']:

        # find request_party ID
        oracle_cursor.execute("""
        SELECT party_id, address_id
        FROM request_party
        WHERE request_id = :request_id
        AND end_event_id IS NULL
        AND party_type_cd='APP'
        FOR UPDATE
        """,
                              request_id=nr.requestId
        )
        row = oracle_cursor.fetchone()
        rp_id = int(row[0])
        address_id = int(row[1])

        # set end event for old request_party instance
        oracle_cursor.execute("""
        UPDATE request_party
        SET end_event_id = :event_id
        WHERE party_id = :party_id
        """,
                              event_id=event_id,
                              party_id=rp_id)

        if change_flags['is_changed__address']:
            # get next address ID
            oracle_cursor.execute("""select address_seq.NEXTVAL@global_address from dual""")
            row = oracle_cursor.fetchone()
            address_id = int(row[0])

            # create new address record
            oracle_cursor.execute("""
            INSERT INTO address@global_address(addr_id, application_cd, state_province_cd, postal_cd, addr_line_1, addr_line_2, addr_line_3, city, country_type_cd)
            VALUES (:address_id, :application_cd, :state_province_cd, :postal_cd, :addr_line_1, :addr_line_2, :addr_line_3, :city, :country_type_cd)
            """,
                                  address_id=address_id,
                                  application_cd='AB',
                                  state_province_cd=applicant_info.stateProvinceCd,
                                  postal_cd=applicant_info.postalCd,
                                  addr_line_1=applicant_info.addrLine1,
                                  addr_line_2=applicant_info.addrLine2,
                                  addr_line_3=applicant_info.addrLine3,
                                  city=applicant_info.city,
                                  country_type_cd=applicant_info.countryTypeCd
                                  )

        # create new record for request party instance
        oracle_cursor.execute("""
        INSERT INTO request_party (party_id, request_id, party_type_cd, last_name, first_name, middle_name, 
                    phone_number, fax_number, email_address, address_id, start_event_id, contact, 
                    client_first_name, client_last_name, decline_notification_ind) 
        VALUES (request_party_seq.nextval, :request_id, 'APP', :last_name, :first_name, :middle_name, 
                :phone_number, :fax_number, :email_address, :address_id, :event_id, :contact, 
                :client_first_name, :client_last_name, :decline_notification_ind)
        """,
                              request_id=nr.requestId,
                              last_name=applicant_info.lastName,
                              first_name=applicant_info.firstName,
                              middle_name=applicant_info.middleName,
                              phone_number=applicant_info.phoneNumber,
                              fax_number=applicant_info.faxNumber,
                              email_address=applicant_info.emailAddress,
                              address_id=address_id,
                              event_id=event_id,
                              contact=applicant_info.contact,
                              client_first_name=applicant_info.clientFirstName,
                              client_last_name=applicant_info.clientLastName,
                              decline_notification_ind=applicant_info.declineNotificationInd
                              )


def _update_nro_partner_name_system(oracle_cursor, nr, event_id, change_flags):
    """find the current NWPTA record(s) (a.k.a. Partner Name System), set end_event_id to event_id
       create new partner_name_system record(s) and set start_event_id to event_id
    """

    for nwpta in nr.partnerNS.all():

        if (nwpta.partnerJurisdictionTypeCd == 'AB' and change_flags['is_changed__nwpta_ab']) or \
           (nwpta.partnerJurisdictionTypeCd == 'SK' and change_flags['is_changed__nwpta_sk']):

            # confirm that there is a record for this partner jurisdiction, and get record ID
            # - failure of this triggers error in logs, and needs to be addressed due to mismatch
            #   between Postgres and Oracle data
            oracle_cursor.execute("""
            SELECT partner_name_system_id
            FROM partner_name_system
            WHERE request_id = :request_id
            AND partner_jurisdiction_type_cd = :partner_jurisdiction_type_cd
            AND end_event_id IS NULL
            FOR UPDATE
            """,
                                  request_id=nr.requestId,
                                  partner_jurisdiction_type_cd=nwpta.partnerJurisdictionTypeCd)
            row = oracle_cursor.fetchone()
            ps_id = int(row[0])

            # set the end event for the existing record
            oracle_cursor.execute("""
            UPDATE partner_name_system
            SET end_event_id = :event_id
            WHERE partner_name_system_id = :ps_id
            """,
                                  event_id=event_id,
                                  ps_id=ps_id)

            # create new partner_name_system record
            oracle_cursor.execute("""
            INSERT INTO partner_name_system(partner_name_system_id, request_id, start_event_id, 
                          partner_name_type_cd, partner_name_number, partner_name, partner_jurisdiction_type_cd, 
                          partner_name_date, last_update_id)
            VALUES (partner_name_system_seq.nextval, :request_id, :event_id, :partner_name_type_cd, 
                          :partner_name_number, :partner_name, :partner_jurisdiction_type_cd, :partner_name_date, 
                          'namex')
            """,
                                  request_id=nr.requestId,
                                  event_id=event_id,
                                  partner_name_type_cd=nwpta.partnerNameTypeCd,
                                  partner_name_number=nwpta.partnerNameNumber,
                                  partner_name=nwpta.partnerName,
                                  partner_jurisdiction_type_cd=nwpta.partnerJurisdictionTypeCd,
                                  partner_name_date=nwpta.partnerNameDate
                                  )

def  _update_consent(oracle_cursor, nr,eid, change_flags):
    if change_flags['is_changed_consent']:
        # set the end event for the existing record
        oracle_cursor.execute("""
               UPDATE consent
               SET end_event_id = :event_id
               WHERE request_id = :request_id 
               and end_event_id IS NULL
               """,
                request_id=nr.requestId,
                event_id = eid)

        #if it was a reset, no need to insert a new record
        if nr.consentFlag is not None:
            # create new consent received/wiaved record record
            oracle_cursor.execute("""
                   INSERT INTO consent (consent_id, request_id, consent_type_cd, received_flag, start_event_id) 
                    VALUES (consent_seq.nextval, :request_id, 'NAME', :consent_flag, :event_id)
                    """,
                              request_id=nr.requestId,
                              consent_flag=nr.consentFlag,
                              event_id=eid
                              )

