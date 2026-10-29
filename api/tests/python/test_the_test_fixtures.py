from datetime import datetime, timezone
from unittest.mock import patch

import pytest


FROZEN_DATETIME = datetime(
    2001, 8, 5, 7, 7, 58, 272362, tzinfo=timezone.utc
)


@pytest.fixture
def freeze_datetime_utcnow():
    with patch("tests.python.test_the_test_fixtures.datetime") as mock_datetime:
        mock_datetime.now.return_value = FROZEN_DATETIME
        yield