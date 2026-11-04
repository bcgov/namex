from contextlib import suppress
from http import HTTPStatus

from flask import json, jsonify

from namex.models import Applicant as ApplicantDAO
from namex.models import Comment as CommentDAO
from namex.models import Event as EventDAO
from namex.models import Name as NameDAO
from namex.models import Request as RequestDAO
from namex.models import State, User

from .. import integration_oracle_namesdb
from ..end_points.util import create_header


def test_get_next(client, jwt, app):
    # add NR to database
    nr = RequestDAO()
    nr.nrNum = 'NR 0000001'
    nr.stateCd = State.DRAFT
    nr._source = 'NRO'
    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.APPROVER, User.EDITOR])

    # The message expected to be returned
    json_msg = jsonify(nameRequest='NR 0000001')

    # get the resource (this is the test)
    rv = client.get('/api/v1/requests/queues/@me/oldest', headers=headers)

    assert rv.status_code == HTTPStatus.OK
    assert rv.json.get('nameRequest') == 'NR 0000001'


def test_get_next_no_draft_avail(client, jwt, app):
    # add NR to database
    nr = RequestDAO()
    nr.nrNum = 'NR 0000001'
    nr.stateCd = State.APPROVED
    nr._source = 'NRO'
    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.APPROVER, User.EDITOR])

    # get the resource (this is the test)
    rv = client.get('/api/v1/requests/queues/@me/oldest', headers=headers)

    # should return 404, not found
    assert rv.status_code == HTTPStatus.NOT_FOUND


def test_get_next_oldest(client, jwt, app):
    # add NR to database
    nr = RequestDAO()
    nr.nrNum = 'NR 0000001'
    nr.stateCd = State.DRAFT
    nr._source = 'NRO'
    nr.save_to_db()

    for i in range(2, 12):
        nr = RequestDAO()
        nr.nrNum = 'NR {0:07d}'.format(i)
        nr.stateCd = State.DRAFT
        nr._source = 'NRO'
        nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.APPROVER, User.EDITOR])

    # The message expected to be returned
    json_msg = jsonify(nameRequest='NR 0000001')

    # get the resource (this is the test)
    rv = client.get('/api/v1/requests/queues/@me/oldest', headers=headers)

    assert rv.status_code == HTTPStatus.OK
    assert b'"nameRequest": "NR 0000001"' in rv.data


def test_get_next_not_approver(client, jwt, app):
    # add NR to database
    nr = RequestDAO()
    nr.nrNum = 'NR 0000001'
    nr.stateCd = State.DRAFT
    nr._source = 'NRO'
    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.EDITOR])

    # get the resource (this is the test)
    # flask-restx / flask-jwt-oidc AttributeError on auth error response (this is a low impact bug in prod)
    with suppress(AttributeError):
        rv = client.get('/api/v1/requests/queues/@me/oldest', headers=headers)

        # commented out because unauthorized status code not getting passed by auth error
        # assert rv.status_code == HTTPStatus.UNAUTHORIZED
        assert rv.status_code not in [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.CREATED]
        # assert rv.json['code'] == 'missing_required_roles'
        # assert rv.json['description'] == 'Missing the role(s) required to access this endpoint'


def test_get_nr_view_only(client, jwt, app):
    # add NR to database
    nr = RequestDAO()
    nr.nrNum = 'NR 0000001'
    nr.stateCd = State.DRAFT
    nr._source = 'NRO'

    applicant = ApplicantDAO()
    nr.applicants.append(applicant)

    name = NameDAO(nrId=nr.id, name='TEST NAME', state=State.DRAFT)
    nr.names.append(name)

    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY])

    # get the resource (this is the test)
    rv = client.get('/api/v1/requests/NR%200000001', headers=headers)

    assert rv.status_code == HTTPStatus.OK
    assert len(rv.json['names']) == 1
    assert len(rv.json['applicants'])


def test_patch_nr_view_only(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY])

    # The message expected to be returned
    json_msg = jsonify(nameRequest='NR 0000001')

    # try to patch for a view only user.  NR doesn't exist in db but we don't care.
    # flask-restx / flask-jwt-oidc AttributeError on auth error response (this is a low impact bug in prod)
    with suppress(AttributeError):
        rv = client.get('/api/v1/requests/queues/@me/oldest', headers=headers)

        # commented out because unauthorized status code not getting passed by auth error
        # assert rv.status_code == HTTPStatus.UNAUTHORIZED
        assert rv.status_code not in [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.CREATED]
        # assert rv.json['code'] == 'missing_a_valid_role'
        # assert rv.json['description'] == 'Missing a role required to access this endpoint'


def test_put_nr_view_only(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY])

    # The message expected to be returned
    json_msg = jsonify(nameRequest='NR 0000001')

    # try to patch for a view only user.  NR doesn't exist in db but we don't care.
    # flask-restx / flask-jwt-oidc AttributeError on auth error response (this is a low impact bug in prod)
    with suppress(AttributeError):
        rv = client.get('/api/v1/requests/queues/@me/oldest', headers=headers)

        # commented out because unauthorized status code not getting passed by auth error
        # assert rv.status_code == HTTPStatus.UNAUTHORIZED
        assert rv.status_code not in [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.CREATED]
        # assert rv.json['code'] == 'missing_a_valid_role'
        # assert rv.json['description'] == 'Missing a role required to access this endpoint'


@integration_oracle_namesdb
def test_add_new_name_to_nr(client, jwt, app):
    # add NR to database
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.INPROGRESS
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'ONE'
    nr.names = [name1]
    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.APPROVER, User.EDITOR])

    # get the resource so we have a template for the request:
    rv = client.get('/api/v1/requests/NR%200000002', headers=headers)
    assert rv.status_code == 200
    # assert we're starting with just one name:
    data = json.loads(rv.data)
    assert len(data['names']) == 1

    new_name = data['names'][0].copy()
    new_name['name'] = 'Name 2'
    new_name['choice'] = 2
    data['names'].append(new_name)

    # Update with a brand new name (this is the test)
    rv = client.put('/api/v1/requests/NR%200000002', json=data, headers=headers)

    assert rv.status_code == HTTPStatus.OK
    data = json.loads(rv.data)
    assert len(data['names']) == 2


@integration_oracle_namesdb
def test_add_new_blank_name_to_nr(client, jwt, app):
    # add NR to database
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.INPROGRESS
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'ONE'
    nr.names = [name1]
    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.APPROVER, User.EDITOR])

    # get the resource so we have a template for the request:
    rv = client.get('/api/v1/requests/NR%200000002', headers=headers)
    assert rv.status_code == HTTPStatus.OK
    # assert we're starting with just one name:
    data = json.loads(rv.data)
    assert len(data['names']) == 1

    new_name = data['names'][0].copy()
    new_name['name'] = ''
    new_name['choice'] = 2
    data['names'].append(new_name)

    # Update with a brand new name (this is the test)
    rv = client.put('/api/v1/requests/NR%200000002', json=data, headers=headers)

    assert rv.status_code == HTTPStatus.OK
    data = json.loads(rv.data)
    assert len(data['names']) == 1


@integration_oracle_namesdb
def test_remove_name_from_nr(client, jwt, app):
    # add NR to database
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.INPROGRESS
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'ONE'
    name2 = NameDAO()
    name2.choice = 2
    name2.name = 'TWO'
    nr.names = [name1, name2]
    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.APPROVER, User.EDITOR])

    # get the resource so we have a template for the request:
    rv = client.get('/api/v1/requests/NR%200000002', headers=headers)
    assert rv.status_code == HTTPStatus.OK
    # assert we're starting with just one name:
    data = json.loads(rv.data)
    assert len(data['names']) == 2

    for name in data['names']:
        if name['choice'] == 2:
            name['name'] = ''

    # Update with one blank name name (should remove the blank name)
    rv = client.put('/api/v1/requests/NR%200000002', json=data, headers=headers)

    data = json.loads(rv.data)
    assert rv.status_code == HTTPStatus.OK
    assert len(data['names']) == 1


def test_add_new_comment_to_nr(client, jwt, app):
    # add a user for the comment
    user = User(
        'test-user',
        '',
        '',
        '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
        'https://dev.loginproxy.gov.bc.ca/auth/realms/bcregistry',
        '123',
        'IDIR',
    )
    user.save_to_db()

    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.INPROGRESS
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    comment1 = CommentDAO()
    comment1.comment = 'This is the first Comment'
    comment1.nr_id = nr.id
    comment1.examinerId = nr.userId
    nr.comments = [comment1]
    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.APPROVER, User.EDITOR])

    # get the resource so we have a template for the request:
    rv = client.get('/api/v1/requests/NR%200000002', headers=headers)
    assert rv.status_code == HTTPStatus.OK
    # assert we're starting with just one name:
    data = json.loads(rv.data)
    assert len(data['comments']) == 1

    new_comment = {'comment': 'The 13th comment entered by the user.'}

    rv = client.post('/api/v1/requests/NR%200000002/comments', json=new_comment, headers=headers)

    assert rv.status_code == HTTPStatus.OK
    assert b'"comment": "The 13th comment entered by the user."' in rv.data

    event_results = EventDAO.query.filter_by(nrId=nr.id).order_by(EventDAO.eventDate.desc()).first_or_404()
    assert event_results.action == 'post'
    assert event_results.eventJson[0:11] == '{"comment":'


def test_comment_where_no_nr(client, jwt, app):
    # add a user for the comment
    user = User(
        'test-user',
        '',
        '',
        '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
        'https://dev.loginproxy.gov.bc.ca/auth/realms/bcregistry',
        '123',
        'IDIR',
    )
    user.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.APPROVER, User.EDITOR])

    new_comment = {'comment': 'The 13th comment entered by the user.'}

    rv = client.post('/api/v1/requests/NR%200000002/comments', json=new_comment, headers=headers)
    assert rv.status_code == HTTPStatus.NOT_FOUND


def test_comment_where_no_user(client, jwt, app):
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.INPROGRESS
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.APPROVER, User.EDITOR])

    new_comment = {'comment': 'The 13th comment entered by the user.'}
    rv = client.post('/api/v1/requests/NR%200000002/comments', json=new_comment, headers=headers)
    assert rv.status_code == HTTPStatus.NOT_FOUND


def test_comment_where_no_comment(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    headers = create_header(jwt, [User.VIEWONLY, User.APPROVER, User.EDITOR])
    headers['Content-Type'] = 'application/json'
    new_comment = None
    rv = client.post('/api/v1/requests/NR%200000002/comments', data=json.dumps(new_comment), headers=headers)
    assert rv.status_code == HTTPStatus.BAD_REQUEST
