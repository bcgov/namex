from datetime import datetime

from namex.constants import AbstractEnum

response_keys = ['auto_approved_count', 'priority_wait_time', 'regular_wait_time']


class UnitTime(AbstractEnum):
    DAY = 'days'
    HR = 'hours'
    MIN = 'minutes'

# this is a separate function to make it easier to mock datetime.utcnow() for testing purposes
def get_utc_now():
    return datetime.utcnow()
