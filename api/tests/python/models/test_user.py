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
