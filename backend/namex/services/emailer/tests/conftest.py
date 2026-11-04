# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Common setup and fixtures for the pytest suite used by this service."""

import datetime
import os
import sys
from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv

# Add the project root (emailer/) to sys.path so 'config' can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create a mock CloudTasksClient with task_path() returning a real string
mock_client_instance = MagicMock()
mock_client_instance.task_path.side_effect = lambda *args, **kwargs: f"/tasks/{kwargs['task']}"
mock_tasks_module = MagicMock()
mock_tasks_module.CloudTasksClient.return_value = mock_client_instance
sys.modules["google.cloud.tasks_v2.services.cloud_tasks.client"] = mock_tasks_module

from config import Testing
from namex_emailer import create_app

from . import FROZEN_DATETIME

# Automatically load the .env file from the root of the project
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


@contextmanager
def not_raises(exception):
    """Corallary to the pytest raises builtin.

    Assures that an exception is NOT thrown.
    """
    try:
        yield
    except exception:
        raise pytest.fail(f"DID RAISE {exception}")


# fixture to freeze utcnow to a fixed date-time
@pytest.fixture
def freeze_datetime_utcnow(monkeypatch):
    """Fixture to return a static time for utcnow()."""

    class _Datetime:
        @classmethod
        def utcnow(cls):
            return FROZEN_DATETIME

    monkeypatch.setattr(datetime, "datetime", _Datetime)


@pytest.fixture(scope="session")
def app():
    """Return a session-wide application configured in TEST mode."""
    _app = create_app(Testing)

    return _app


@pytest.fixture
def config(app):
    """Return the application config."""
    return app.config


@pytest.fixture(scope="session")
def client(app):
    """Return a session-wide Flask test client."""
    return app.test_client()


@pytest.fixture
def session(app):
    with app.app_context():
        yield
