from flask import jsonify
from flask import json
from namex.models import User

import pytest


token_header = {
                "alg": "RS256",
                "typ": "JWT",
                "kid": "flask-jwt-oidc-test-client"
               }
claims = {
            "iss": "https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc",
            "sub": "43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc",
            "aud": "NameX-Dev",
            "exp": 31531718745,
            "iat": 1531718745,
            "jti": "flask-jwt-oidc-test-support",
            "typ": "Bearer",
            "username": "test-user",
            "realm_access": {
                "roles": [
                    "{}".format(User.EDITOR),
                    "{}".format(User.APPROVER),
                    "viewer",
                    "user"
                ]
            }
         }

claims_editor = {
            "iss": "https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc",
            "sub": "43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc",
            "aud": "NameX-Dev",
            "exp": 21531718745,
            "iat": 1531718745,
            "jti": "flask-jwt-oidc-test-support",
            "typ": "Bearer",
            "username": "test-user",
            "realm_access": {
                "roles": [
                    "{}".format(User.VIEWONLY),
                    "{}".format(User.EDITOR),
                    "user"
                ]
            }
         }

claims_viewer = {
            "iss": "https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc",
            "sub": "43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc",
            "aud": "NameX-Dev",
            "exp": 11531718745,
            "iat": 1531718745,
            "jti": "flask-jwt-oidc-test-support",
            "typ": "Bearer",
            "username": "test-user",
            "realm_access": {
                "roles": [
                    "{}".format(User.VIEWONLY),
                    "user"
                ]
            }
         }
def test_get_nr_from_nro_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    #add a user for the comment
    user = User('test-user','','','43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc','https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.DRAFT
    nr.requestId = 1460775
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    EventRecorder.record(user, Event.UPDATE_FROM_NRO, nr, {})

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Get NR Details from NRO"' in rv.data


def test_get_inprogress_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.INPROGRESS
    nr.requestId = 1460775
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    EventRecorder.record(user, Event.PATCH, nr, {})

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
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.INPROGRESS
    nr.requestId = 1460775
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
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

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.HOLD
    nr.requestId = 1460775
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    EventRecorder.record(user, Event.PATCH, nr, {})

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Hold Request"' in rv.data

def test_on_hold_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.HOLD
    nr.requestId = 1460775
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    EventRecorder.record(user, Event.PATCH, nr, {})

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

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.EXPIRED
    nr.requestId = 1460775
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    EventRecorder.record(user, Event.POST, nr, {})

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

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.CANCELLED
    nr.requestId = 1460775
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
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

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.CANCELLED
    nr.requestId = 1460775
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    EventRecorder.record(user, Event.PATCH, nr, {})

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

        # create JWT & setup header with a Bearer Token using the JWT
        token = jwt.create_jwt(claims, token_header)
        headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

        nr = RequestDAO()
        nr.nrNum = 'NR 0000002'
        nr.stateCd = State.REJECTED
        nr.requestId = 1460775
        name1 = NameDAO()
        name1.choice = 1
        name1.name = 'TEST NAME ONE'
        nr.names = [name1]
        nr.save_to_db()

        EventRecorder.record(user, Event.PATCH, nr, {})

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

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.DRAFT
    nr.requestId = 1460775
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    EventRecorder.record(user, Event.PUT, nr, {"additional": "additional"})

    # get the resource (this is the test)
    rv = client.get('/api/v1/events/NR%200000002', headers=headers)
    assert rv.status_code == 200

    assert b'"user_action": "Edit NR Details"' in rv.data

def test_reopen_event_history(client, jwt, app):
    from namex.models import Request as RequestDAO, State, Name as NameDAO, User, Event
    from namex.services import EventRecorder

    # add a user for the comment
    user = User('test-user', '', '', '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.REJECTED
    nr.requestId = 1460775
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

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.HOLD
    nr.requestId = 1460775
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

    assert b'"user_action": "Edit NR Details"' in rv.data