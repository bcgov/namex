from datetime import datetime, timezone

from namex.constants import AbstractEnum

response_keys = ['auto_approved_count', 'priority_wait_time', 'regular_wait_time']


# this is a separate function to make it easier to mock datetime.now(timezone.utc) for testing purposes
def get_utc_now():
    return datetime.now(timezone.utc)
