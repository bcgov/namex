from datetime import datetime
from dateutil import tz

from namex.constants import DATE_FORMAT_NAMEX_SEARCH


def get_server_now():
    """Get the server now datetime object with local timezone"""
    return datetime.now().astimezone(tz.tzlocal())


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
    result = server_now.astimezone(tz.UTC)
    return result


def get_utc_server_now_with_delta_str(time_delta):
    """Get the server now datetime object with delta as a UTC datetime string"""
    utc_server_now_with_delta = get_utc_server_now_with_delta(time_delta)
    result = utc_server_now_with_delta.strftime(DATE_FORMAT_NAMEX_SEARCH)
    return result


def get_utc_server_now():
    """Get the server now datetime object as a UTC datetime"""
    server_now = get_server_now()
    result = server_now.astimezone(tz.UTC)
    return result

