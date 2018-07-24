from namex.models import User


def test_user(session, client):
    """Start with a blank database."""

    user1 = User(username = 'thor', firstname = 'thor', lastname = 'g', sub = 'abcdefg', iss='http://nowhere.localdomain')

    session.add(user1)
    session.commit()

    assert user1.id is not None
