import pytest

from app import create_app, db as _db, jwt as _jwt
from config import TestConfig
import sys, os


@pytest.fixture(scope="session")
def app(request):
    """
    Returns session-wide application.
    """
    app = create_app(TestConfig)

    return app


@pytest.fixture(scope="session")
def client(app):
    """
    Returns session-wide Flask test client.
    """
    return app.test_client()


@pytest.fixture(scope="session")
def jwt(app):
    """
    Returns session-wide jwt manager
    """
    return _jwt

@pytest.fixture(scope="session")
def client_ctx(app):
    """
    Returns session-wide Flask test client.
    """
    with app.test_client() as c:
        yield c
