from __future__ import annotations

import json

from namex.models import User
from tests.python.end_points.util import create_header


def test_get_new_user_settings(client, jwt, app):
    """Test getting user settings for a new user."""
    new_user_settings = client.get('api/v1/usersettings', headers=create_header(jwt, [User.EDITOR], 'test-settings'))
    data = new_user_settings.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('searchColumns')
    # should have generated default settings for a new user
    assert resp.get('searchColumns') == [
        'Status',
        'LastModifiedBy',
        'NameRequestNumber',
        'Names',
        'ApplicantFirstName',
        'ApplicantLastName',
        'NatureOfBusiness',
        'ConsentRequired',
        'Priority',
        'ClientNotification',
        'Submitted',
        'LastUpdate',
        'LastComment',
    ]


def test_get_existing_user_settings(client, jwt, app):
    """Test getting user settings for an existing user."""
    user = User(
        username='test-settings',
        sub='43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
        firstname='',
        lastname='',
        iss='',
        idp_userid='123',  # this needs to match the sub in create_header
        login_source='IDIR',
    )
    user.searchColumns = 'Status'
    user.save_to_db()

    # check it gets the existing settings stored in the db
    existing_user_settings = client.get(
        'api/v1/usersettings', headers=create_header(jwt, [User.EDITOR], 'test-settings')
    )
    data = existing_user_settings.data
    assert data
    resp = json.loads(data.decode('utf-8'))

    assert resp.get('searchColumns')
    assert resp.get('searchColumns') == ['Status']


def test_update_user_settings(client, jwt, app):
    """Test updating user settings for an existing user."""
    # create user with settings
    user = User(
        username='test-settings',
        sub='43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',  # this needs to match the sub in create_header
        firstname='',
        lastname='',
        iss='',
        idp_userid='123',
        login_source='IDIR',
    )
    user.searchColumns = 'Status'
    user.save_to_db()
    # update user with put endpoint
    update_user_settings = client.put(
        'api/v1/usersettings',
        json={'searchColumns': ['Status', 'LastModifiedBy']},
        headers=create_header(jwt, [User.EDITOR], 'test-settings'),
    )
    # assert user was successfully updated
    assert update_user_settings.status_code == 204
    assert user.searchColumns == 'Status,LastModifiedBy'
