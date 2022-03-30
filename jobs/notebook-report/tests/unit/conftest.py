"""conftest for the notebook."""
import pytest

from config import Config
from notebookreport import create_app


@pytest.fixture(scope='session')
def app(request):
    """Init apps and Returns session-wide application."""
    app = create_app(Config)

    return app


@pytest.fixture(scope='session')
def client_ctx(app):
    """Init client and returns session-wide Flask test client."""
    with app.test_client() as c:
        yield c
