from namex.models import User


def test_user(session, client):
    """Start with a blank database."""

    user1 = User(username = 'thor', firstname = 'thor', lastname = 'g', sub = 'abcdefg', iss='http://nowhere.localdomain')

    session.add(user1)
    session.commit()

    assert user1.id is not None

def test_user_search_columns(session, client):
    """Start with a blank database."""

    user1 = User(username = 'kial', firstname = 'kial', lastname = 'g', sub = 'abcdefg', iss='http://nowhere.localdomain')

    session.add(user1)
    session.commit()

    assert user1.searchColumns is not None
    assert user1.searchColumns == 'Status,LastModifiedBy,NameRequestNumber,Names,ApplicantFirstName,ApplicantLastName,NatureOfBusiness,ConsentRequired,Priority,ClientNotification,Submitted,LastUpdate,LastComment'


def test_get_service_account_user(session, client):
    """Assert service account user."""
    # add a user for the comment
    user = User('nro_service_account', '', '', '8ca7d47a-024e-4c85-a367-57c9c93de1cd',
                'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc')
    user.save_to_db()

    service_account = User.get_service_account_user()

    assert service_account.username == user.username
