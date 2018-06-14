import pytest
from app import create_app
from config import TestConfig


@pytest.fixture
def client():

    app = create_app(TestConfig())
    client = app.test_client()

    yield client

