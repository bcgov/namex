from datetime import datetime, time
from zoneinfo import ZoneInfo

from namex.constants import DATE_FORMAT_NAMEX_SEARCH

VANCOUVER_TZ = ZoneInfo('America/Vancouver')
UTC_TZ = ZoneInfo('UTC')

def get_server_now():
    """Get the server now datetime object with local timezone"""
    return datetime.now(UTC_TZ).astimezone(VANCOUVER_TZ)


def get_server_now_str():
    """Get the server now date as a string"""
    server_now = get_server_now()
    result = server_now.strftime(DATE_FORMAT_NAMEX_SEARCH)
    return result


def get_server_now_with_delta(time_delta):
    """Get the server now datetime object with delta and local timezone"""
    server_now = get_server_now()
    result = server_now + time_delta
    return result


def get_server_now_with_delta_str(timedelta):
    """Get the server now date string with delta"""
    server_now_with_delta = get_server_now_with_delta(timedelta)
    result = server_now_with_delta.strftime(DATE_FORMAT_NAMEX_SEARCH)
    return result


def get_utc_server_now_with_delta(time_delta):
    """Get the server now datetime object with delta as a UTC datetime"""
    server_now = get_server_now()
    server_now = server_now + time_delta
    result = server_now.astimezone(UTC_TZ)
    return result


def get_utc_server_now_with_delta_str(time_delta):
    """Get the server now datetime object with delta as a UTC datetime string"""
    utc_server_now_with_delta = get_utc_server_now_with_delta(time_delta)
    result = utc_server_now_with_delta.strftime(DATE_FORMAT_NAMEX_SEARCH)
    return result


def get_utc_server_now():
    """Get the server now datetime object as a UTC datetime"""
    server_now = get_server_now()
    result = server_now.astimezone(UTC_TZ)
    return result


def create_utc_min_date_time(date_str: str):
    """Create UTC datetime with min time from provided date string."""
    utc_date_time = datetime.strptime(date_str, DATE_FORMAT_NAMEX_SEARCH)
    min_time = time(hour=0, minute=0, second=0, microsecond=0)
    utc_date_time = datetime.combine(utc_date_time, min_time, tzinfo=UTC_TZ)
    return utc_date_time


def create_utc_date_time(date_str: str, hour: int, minute: int, second: int, microsecond: int):
    """Create UTC datetime with date and time from provided input params."""
    utc_date_time = datetime.strptime(date_str, DATE_FORMAT_NAMEX_SEARCH)
    time_part = time(hour=hour, minute=minute, second=second, microsecond=microsecond)
    utc_date_time = datetime.combine(utc_date_time, time_part, tzinfo=UTC_TZ)
    return utc_date_time
