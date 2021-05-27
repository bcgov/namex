import pytest
from datetime import datetime
from flask import jsonify
from flask import json

from namex.constants import ValidSources
from namex.models import Event, Name as NameDAO, Request as RequestDAO, State, User
from namex.services import EventRecorder

from tests.python.end_points.services.utils import create_header

def create_base_nr():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.PENDING_PAYMENT
    nr.requestId = 1460775
    nr._source = ValidSources.NAMEREQUEST.value
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.additionalInfo = 'test'
    nr.requestTypeCd = 'CR'
    nr.request_action_cd = 'NEW'
    nr.save_to_db()
    return nr

### NR flow through name request:
# 1.  post (create NRL)
# 2.  post (create NR), initialize payment/complete payment
# 3.  namex_pay (create NR), complete payment (if ^ was initialize)
# 4.  edit nr details in name request (optional)
# 5.  post upgrade priority, initialize/complete payment (optional)
# 6.  namex_pay (upgrade priority), complete payment (if ^ was initialize)
# 7.  get details from nro (starts here for NRs from NRO)
# 8.  load nr
# 9.  staff comment (optional)
# 10. marked on hold (optional)
# 11. edit nr details in namex (optional)
# 12. complete name choice
# 13. decision
# 14. updated nro (furnished)
# 15. edit nr details after completion (optional)
# 16. reopen (optional)
# 17. undo decision (requires reopen first)

# TODO: fill out tests for above based on this
def test_event_create_nrl(client, jwt, app):

    #add a user for the comment
    user = User('test-user','','','43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc','url')
    user.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.EDITOR])

    nr = create_base_nr()

    before_record_date = datetime.utcnow()
    EventRecorder.record(user, Event.POST, nr, nr.json())

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200
    assert rv.data
    response = json.loads(rv.data)
    assert response['transactions']
    assert len(response['transactions']) == 1
    assert response['transactions'][0]['additionalInfo'] == 'test'
    assert response['transactions'][0]['consent_dt'] == None
    assert response['transactions'][0]['consentFlag'] == None
    assert response['transactions'][0]['eventDate'] > before_record_date.isoformat()
    assert response['transactions'][0]['expirationDate'] == None
    assert response['transactions'][0]['names'] == [
        {
            'choice': 1,
            'comment': None,
            'conflict1': '',
            'conflict1_num': '',
            'conflict2': '',
            'conflict2_num': '',
            'conflict3': '',
            'conflict3_num': '',
            'consumptionDate': None,
            'corpNum': None,
            'decision_text': '',
            'designation': None,
            'id': 1,
            'name': 'TEST NAME ONE',
            'name_type_cd': None,
            'state': 'NE'
        }
    ]
    assert response['transactions'][0]['priorityCd'] == None
    assert response['transactions'][0]['requestTypeCd'] == 'CR'
    assert response['transactions'][0]['request_action_cd'] == 'NEW'
    assert response['transactions'][0]['stateCd'] == State.PENDING_PAYMENT
    assert response['transactions'][0]['user_action'] == 'Created NRL'
    assert response['transactions'][0]['user_name'] == 'test-user'


def test_get_inprogress_event_history(client, jwt, app):

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc', 'url')
    user.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.EDITOR])

    nr = create_base_nr()
    nr.stateCd = State.DRAFT
    nr.save_to_db()
    EventRecorder.record(user, Event.POST + ' [payment completed] CREATE', nr, nr.json())

    nr.stateCd = State.INPROGRESS
    nr.save_to_db()
    EventRecorder.record(user, Event.PATCH, nr, { 'state': 'INPROGRESS' })
    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Load NR"' in rv.data

def test_get_next_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.EDITOR])

    nr = create_base_nr()
    nr.stateCd = State.DRAFT
    nr.save_to_db()
    EventRecorder.record(user, Event.POST + ' [payment completed] CREATE', nr, nr.json())


    nr.stateCd = State.INPROGRESS
    nr.save_to_db()
    EventRecorder.record(user, Event.GET, nr, {})

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Get Next NR"' in rv.data

def test_on_hold_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    headers = create_header(jwt, [User.EDITOR])

    nr = create_base_nr()
    nr.stateCd = State.HOLD
    nr.save_to_db()

    EventRecorder.record(user, Event.PATCH, nr, { 'state': 'HOLD' })

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Hold Request"' in rv.data

def test_expired_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    headers = create_header(jwt, [User.EDITOR])

    nr = create_base_nr()
    nr.stateCd = State.EXPIRED
    nr.expirationDate = datetime.utcnow()
    nr.save_to_db()

    EventRecorder.record(user, Event.POST, nr, nr.json())

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Expired by NRO"' in rv.data

def test_cancelled_in_nro_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    headers = create_header(jwt, [User.EDITOR])

    nr = create_base_nr()
    nr.stateCd = State.CANCELLED
    nr.save_to_db()

    EventRecorder.record(user, Event.POST, nr, {})

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Cancelled in NRO"' in rv.data

def test_cancelled_in_namex_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    headers = create_header(jwt, [User.EDITOR])

    nr = create_base_nr()
    nr.stateCd = State.CANCELLED
    nr.save_to_db()

    EventRecorder.record(user, Event.PATCH, nr, { 'state': 'CANCELLED' })

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Cancelled in Namex"' in rv.data

def test_decision_event_history(client, jwt, app):
        from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
        from namex.services import EventRecorder

        # add a user for the comment
        user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                    'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
        user.save_to_db()

        headers = create_header(jwt, [User.EDITOR])

        nr = create_base_nr()
        nr.stateCd = State.REJECTED
        nr.save_to_db()

        EventRecorder.record(user, Event.PATCH, nr, { 'state': 'REJECTED' })

        # get the resource (this is the test)
        rv = client.get('/api/v1/events/NR%200000002', headers=headers)
        assert rv.status_code == 200

        assert b'"user_action": "Decision"' in rv.data


def test_edit_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    headers = create_header(jwt, [User.EDITOR])

    nr = create_base_nr()
    nr.stateCd = State.INPROGRESS
    nr.additionalInfo = 'additional'
    nr.save_to_db()

    EventRecorder.record(user, Event.PUT, nr, nr.json())

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Edit NR Details (NameX)"' in rv.data

def test_reopen_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    headers = create_header(jwt, [User.EDITOR])

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.REJECTED
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    EventRecorder.record(user, Event.PATCH, nr, {})

    nr.stateCd = State.INPROGRESS
    EventRecorder.record(user, Event.PUT, nr, {"additional": "additional","furnished": "N"})

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Re-Open"' in rv.data

def test_edit_inprogress_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    headers = create_header(jwt, [User.EDITOR])

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.DRAFT
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    EventRecorder.record(user, Event.POST, nr, nr.json())

    nr.stateCd = State.INPROGRESS
    nr.save_to_db()
    EventRecorder.record(user, Event.PUT, nr, {"additional": "additional","furnished": "N"})

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Edit NR Details (NameX)"' in rv.data