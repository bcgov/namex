import pytest

from sftp_nuans_report.config import Config
from sftp_nuans_report.sftpnuans import create_app


@pytest.fixture(scope='session')
def app(request):
    """
    Returns session-wide application.
    """
    app = create_app(Config)

    return app


@pytest.fixture(scope='session')
def client_ctx(app):
    """
    Returns session-wide Flask test client.
    """
    with app.test_client() as c:
        yield c
