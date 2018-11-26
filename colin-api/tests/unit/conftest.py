import pytest
import os
from app import create_app
from config import TestConfig
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture(scope="session")
def app():
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
def client_ctx(app):
    """
    Returns session-wide Flask test client.
    """
    with app.test_client() as c:
        yield c


@pytest.fixture(scope="session")
def fake_names_db(app):
    user = os.getenv('FAKE_NAMES_DATABASE_USERNAME', '')
    password = os.getenv('FAKE_NAMES_DATABASE_PASSWORD', '')
    name = os.getenv('FAKE_NAMES_DATABASE_NAME', '')
    host = os.getenv('FAKE_NAMES_DATABASE_HOST', '')
    port = os.getenv('FAKE_NAMES_DATABASE_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=user,
        password=password,
        host=host,
        port=port,
        name=name,
    )
    db = SQLAlchemy()
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    return db
