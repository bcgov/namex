from datetime import datetime, time
from dateutil import tz
import urllib.parse


def get_utc_now():
    return datetime.now(tz=tz.UTC)


def get_utc_now_str():
    utc_now = get_utc_now()
    return convert_to_utc_date_time_str(utc_now)


def get_utc_now_min_time_str():
    utc_now = get_utc_now()
    min_time = time(hour=0, minute=0, second=0, microsecond=0)
    result = datetime.combine(utc_now.date(), min_time, tzinfo=tz.UTC)
    return convert_to_utc_date_time_str(result)

def get_utc_now_max_time_str():
    utc_now = get_utc_now()
    max_time = time(hour=23, minute=59, second=59, microsecond=999999)
    result = datetime.combine(utc_now.date(), max_time, tzinfo=tz.UTC)
    return convert_to_utc_date_time_str(result)

def get_utc_now_with_delta(timedelta):
    utc_date_time = get_utc_now()
    return utc_date_time + timedelta


def get_utc_now_with_delta_str(delta):
    utc_date_time = get_utc_now_with_delta(delta)
    return convert_to_utc_date_time_str(utc_date_time)


def get_utc_now_with_min_delta_str(delta):
    utc_date_time = get_utc_now_with_delta(delta)
    min_time = time(hour=0, minute=0, second=0, microsecond=0)
    result = datetime.combine(utc_date_time.date(), min_time, tzinfo=tz.UTC)
    return convert_to_utc_date_time_str(result)

def get_utc_now_with_max_delta_str(delta):
    utc_date_time = get_utc_now_with_delta(delta)
    max_time = time(hour=23, minute=59, second=59, microsecond=999999)
    result = datetime.combine(utc_date_time.date(), max_time, tzinfo=tz.UTC)
    return convert_to_utc_date_time_str(result)

def convert_to_utc_date_time_str(date_time_obj: datetime):
    result = date_time_obj.strftime('%Y-%m-%d %H:%M:%S%z')
    result = urllib.parse.quote(result)
    return result


def escape_date_time(utc_date_time: str):
    return urllib.parse.quote(utc_date_time)
