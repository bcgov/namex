"""Checking
NR back-in by setting state DRAFT After an Edit
"""
from flask import current_app
from .utils import nro_examiner_name
from namex.models import State

def manage_nr_locks(nr, ora_cursor,action,con):
    """Set the Nr State back to DRAFT after Editing
    :raises Exception: what ever error we get, let our caller handle, this is here in case we want to wrap it - future
    """

    eid = _get_event_id(ora_cursor)

    current_app.logger.debug('event ID for NR Details edit:{}'.format(eid))
    _create_nro_transaction(ora_cursor, nr, eid, transaction_type='ADMIN')
    con.commit()

    if action == 'LOCK':
        current_app.logger.debug('got to checkout_nr() for NR:{}'.format(nr.nrNum))
        _update_nro_request_state_to_hold(ora_cursor, nr, eid)
    else:
        current_app.logger.debug('got to checkin_nr() for NR:{}'.format(nr.nrNum))
        _update_nro_request_state_to_draft(ora_cursor, nr, eid)

    con.commit()

    current_app.logger.debug('got to the end of checkinout_nr()')

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
      VALUES (transaction_seq.nextval, :request_id, :transaction_type, :event_id, 'namereq')
    """,
                          request_id=nr.requestId,
                          transaction_type=transaction_type,
                          event_id=event_id
                          )
    current_app.logger.debug('transaction record created')


def _update_nro_request_state_to_draft(oracle_cursor, nr, event_id):
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


def _update_nro_request_state_to_hold(oracle_cursor, nr, event_id):
    new_state = None
    if nr.stateCd == State.INPROGRESS:
        new_state = 'H'
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
