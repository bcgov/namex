"""update the Name Request Record in NRO from the current record state in NameX

   In order to maintain the NRO data patterns, the record updates will follow
   the following pattern:

   create new event of type 'SYST'
   create new transaction of type 'ADMIN'
   using STAFF_IDIR of 'namex'

   Each main segment has its own function call to facilitate testing,
   but the main function call is update_nr

"""

from flask import current_app
from .utils import generate_compressed_name

def update_nr (nr, ora_cursor, change_flags):
    """Update the Name Request in NRO
    :raises Exception: what ever error we get, let our caller handle, this is here in case we want to wrap it - future
    """

    eid = _get_event_id(ora_cursor)
    current_app.logger.debug('got to update_nr() for NR:{}'.format(nr.nrNum))
    current_app.logger.debug('event ID for NR Details edit:{}'.format(eid))
    _create_nro_transaction(ora_cursor, nr, eid)
    _update_request(ora_cursor, nr, eid, change_flags)
    _update_nro_names(ora_cursor, nr, eid, change_flags)
    _update_nro_address(ora_cursor, nr, eid, change_flags)
    _update_nro_partner_name_system(ora_cursor, nr, eid, change_flags)

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


def _create_nro_transaction(oracle_cursor, nr, event_id):

    oracle_cursor.execute("""
    INSERT INTO transaction (transaction_id, request_id, transaction_type_cd, event_id, staff_idir)
      VALUES (transaction_seq.nextval, :request_id, 'ADMIN', :event_id, 'namex')
    """,
                          request_id=nr.requestId,
                          event_id=event_id
                          )


def _update_request(oracle_cursor, nr, event_id, change_flags):
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

        # create new request_instance record
        oracle_cursor.execute("""
        INSERT INTO request_instance
        VALUES (request_instance_seq.nextval, :request_id, :priority_cd, :request_type_cd, 
                  :expiration_date, :event_id, null, :tilma_ind, :xpro_jurisdiction, 
                  :nuans_expiration_date, :queue_position, :additional_info, :nature_business_info,
                  :user_note, :nuans_num, :tilma_transaction_id, :assumed_nuans_num, 
                  :assumed_nuans_name, :assumed_nuans_expiration_date, :last_nuans_updated_role, 
                  :admin_comment)
        """,
                              request_id=nr.requestId,
                              priority_cd=row[2],
                              request_type_cd=nr.requestTypeCd,
                              expiration_date=nr.expirationDate,
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
                              admin_comment=row[20]
                              )


def _update_nro_names(oracle_cursor, nr, event_id, change_flags):
    """find the current name instance, set it's end_event_id to event_id
       create a new name_instance and set it start_event_id to event_id
    """

    for name in nr.names.all():

        if  (name.choice == 1 and change_flags['is_changed__name1']) or \
            (name.choice == 2 and change_flags['is_changed__name2']) or \
            (name.choice == 3 and change_flags['is_changed__name3']):

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
                                  choice=name.choice)
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

    applicantInfo = nr.applicants.one_or_none()
    if not applicantInfo:
        return

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
                                  state_province_cd=applicantInfo.stateProvinceCd,
                                  postal_cd=applicantInfo.postalCd,
                                  addr_line_1=applicantInfo.addrLine1,
                                  addr_line_2=applicantInfo.addrLine2,
                                  addr_line_3=applicantInfo.addrLine3,
                                  city=applicantInfo.city,
                                  country_type_cd=applicantInfo.countryTypeCd
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
                              last_name=applicantInfo.lastName,
                              first_name=applicantInfo.firstName,
                              middle_name=applicantInfo.middleName,
                              phone_number=applicantInfo.phoneNumber,
                              fax_number=applicantInfo.faxNumber,
                              email_address=applicantInfo.emailAddress,
                              address_id=address_id,
                              event_id=event_id,
                              contact=applicantInfo.contact,
                              client_first_name=applicantInfo.clientFirstName,
                              client_last_name=applicantInfo.clientLastName,
                              decline_notification_ind=applicantInfo.declineNotificationInd
                              )

def _update_nro_partner_name_system(oracle_cursor, nr, event_id, change_flags):
    """find the current NWPTA record(s) (a.k.a. Partner Name System), set end_event_id to event_id
       create new partner_name_system record(s) and set start_event_id to event_id
    """

    for nwpta in nr.partnerNS.all():

        if  (nwpta.partnerJurisdictionTypeCd == 'AB' and change_flags['is_changed__nwpta_ab']) or \
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
                          partner_name_type_cd, partner_name_number, partner_jurisdiction_type_cd, 
                          partner_name_date, last_update_id)
            VALUES (partner_name_system_seq.nextval, :request_id, :event_id, :partner_name_type_cd, 
                          :partner_name_number, :partner_jurisdiction_type_cd, :partner_name_date, 
                          'namex')
            """,
                                  request_id=nr.requestId,
                                  event_id=event_id,
                                  partner_name_type_cd=nwpta.partnerNameTypeCd,
                                  partner_name_number=nwpta.partnerNameNumber,
                                  partner_jurisdiction_type_cd=nwpta.partnerJurisdictionTypeCd,
                                  partner_name_date=nwpta.partnerNameDate
                                  )
