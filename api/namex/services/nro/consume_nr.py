"""

1. Get the next event id
SELECT event_seq.NEXTVAL INTO l_event_id FROM dual;

2. save the event
insert into event (EVENT_ID, EVENT_TYPE_CD, EVENT_TIMESTAMP);
           values (l_event_id, 'CONSUME', sysdate);

3. save the transaction
INSERT INTO transaction(transaction_id, transaction_type_cd, request_id, event_id, staff_idir)
          VALUES(transaction_seq.nextval, 'CONSUME', ***request_id***, l_event_id,'THOR');

4. get and update the name_instance
UPDATE name_instance SET end_event_id = l_event_id
where name_id=***name_id*** and end_event_id is null;

5. create a new name_instance record
INSERT INTO name_instance (name_instance_id, name_id, choice_number, name, designation,
                           consumption_date, search_name, start_event_id, end_event_id, corp_num)
SELECT name_instance_seq.nextval,name_id,choice_number,name,designation,
       ***consumption_date***,search_name,l_event_id,NULL,***corp_num***
FROM name_instance 
WHERE name_id=***name_id*** 
and end_event_id=l_event_id -- the row we just closed off

"""

from flask import current_app
from .utils import generate_compressed_name
from namex.constants import NameState
from namex.models import State

def consume_nr(nr, username, corp_num, ora_cursor):
    transaction_type='CONSUME'
    current_app.logger.debug('got to consume_nr() for NR:{}'.format(nr.nrNum))

    event_id = _get_next_event_id(ora_cursor, transaction_type=transaction_type)
    current_app.logger.debug('event ID for event_type==CONSUME:{}'.format(event_id))

    _create_nro_transaction(ora_cursor, nr, event_id, username=username, transaction_type=transaction_type)
    _consume_nro_names(ora_cursor, nr, event_id, corp_num)

    current_app.logger.debug('got to the end of consume_nr({})'.format(nr.nrNum))

def _get_next_event_id(oracle_cursor, transaction_type):  # -> (int)
    """gets the event_id to be used for updating the NR history
    :oracle_conn : a Cx_Oracle connection to the NRO database
    :returns (int): a valid NRO event_id to be used for updating NRO records
    """

    oracle_cursor.execute("""select event_seq.NEXTVAL from dual""")
    row = oracle_cursor.fetchone()

    event_id = int(row[0])

    oracle_cursor.execute("""
    INSERT INTO event (event_id, event_type_cd, event_timestamp)
      VALUES (:event_id, :transaction_type, sysdate)
    """,
        event_id=event_id,
        transaction_type=transaction_type
    )

    return event_id


def _create_nro_transaction(oracle_cursor, nr, event_id, username, transaction_type='CONSUME'):

    oracle_cursor.execute("""
    INSERT INTO transaction (transaction_id, request_id, transaction_type_cd, event_id, staff_idir)
      VALUES (transaction_seq.nextval, :request_id, :transaction_type, :event_id, :username)
    """,
        request_id=nr.requestId,
        transaction_type=transaction_type,
        event_id=event_id,
        username=username
        )
    current_app.logger.debug('transaction record created')


def _consume_nro_names(oracle_cursor, nr, event_id, corp_num):
    """find the current name instance, set it's end_event_id to event_id
       if the name was deleted, nothing more needs to be done.
       otherwise, create a new name_instance and set its start_event_id to event_id
    """

    for name in nr.names.all():


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

            if name.state in [NameState.APPROVED, NameState.CONDITION]:
                consume_corp_num = corp_num
            else:
                consume_corp_num = None
            
            oracle_cursor.execute("""
            INSERT INTO name_instance (name_instance_id, name_id, choice_number, name, designation,
                                       consumption_date, search_name, start_event_id, end_event_id, corp_num)
            SELECT name_instance_seq.nextval,name_id,choice_number,name,designation,
                   sysdate,search_name,l_event_id,NULL,:corp_num
            FROM name_instance 
            WHERE name_id=:name_id 
            and end_event_id=:event_id
            """,
                name_id=n_id,
                event_id=event_id,
                corp_num=consume_corp_num)
