
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

FROZEN_DATETIME = datetime(
    2001, 8, 5, 7, 7, 58, 272362, tzinfo=timezone.utc
)


@pytest.fixture
def freeze_datetime_utcnow():
    with patch.object(
        __import__(__name__, fromlist=['datetime']),
        'datetime',
    ) as mock_datetime:
        mock_datetime.now.return_value = FROZEN_DATETIME
        yield


def test_patch_datetime_utcnow(freeze_datetime_utcnow):
    assert datetime.now(timezone.utc) == FROZEN_DATETIME
