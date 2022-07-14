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
    user = os.getenv('FDW_NAMES_DATABASE_TEST_USERNAME', '')
    password = os.getenv('FDW_NAMES_DATABASE_TEST_PASSWORD', '')
    name = os.getenv('FDW_NAMES_DATABASE_TEST_NAME', '')
    host = os.getenv('FDW_NAMES_DATABASE_TEST_HOST', '')
    port = os.getenv('FDW_NAMES_DATABASE_TEST_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{host}:{port}/{name}'
    db = SQLAlchemy()
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    return db
