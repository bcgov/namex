from datetime import datetime
from dateutil import tz

def get_server_now():
    return datetime.now()


def get_server_now_str():
    result = datetime.now().strftime('%Y-%m-%d')
    return result


def get_utc_server_now_with_delta(timedelta):
    server_now = get_server_now() + timedelta
    result = server_now.astimezone(tz.UTC)
    return result


def get_utc_server_now_with_delta_str(timedelta):
    utc_server_now_with_delta = get_utc_server_now_with_delta(timedelta)
    result = utc_server_now_with_delta.strftime('%Y-%m-%d')
    return result


def get_utc_server_now():
    server_now = get_server_now()
    result = server_now.astimezone(tz.UTC)
    return result

