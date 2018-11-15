import pytest
from pytest_mock import mocker
from flask import current_app

from nro.app import create_app

from config import Config


@pytest.fixture(scope="session")
def app(request):
    """
    Returns session-wide application.
    """
    app = create_app(Config)

    return app


@pytest.fixture(scope="session")
def client_ctx(app):
    """
    Returns session-wide Flask test client.
    """
    with app.test_client() as c:
        yield c
