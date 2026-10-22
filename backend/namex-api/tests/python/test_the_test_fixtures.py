import datetime

from . import FROZEN_DATETIME


# quick test to ensure my fixture is working correctly
def test_patch_datetime_utcnow(freeze_datetime_utcnow):
    assert datetime.datetime.utcnow() == FROZEN_DATETIME
