"""
pg8000 compatibility utilities for datetime handling.

This module provides utility functions to handle datetime objects consistently
with pg8000 driver, avoiding timezone-related errors without modifying business logic.
"""
from datetime import datetime, timezone


def ensure_timezone_aware(dt_obj):
    """
    Ensure a datetime object is timezone-aware for pg8000 compatibility.

    Args:
        dt_obj: datetime object or None

    Returns:
        timezone-aware datetime object or None
    """
    if dt_obj is None:
        return None

    if hasattr(dt_obj, 'date') and not hasattr(dt_obj, 'tzinfo'):
        # Handle date objects - convert to datetime with UTC timezone
        return datetime.combine(dt_obj, datetime.min.time()).replace(tzinfo=timezone.utc)
    elif hasattr(dt_obj, 'tzinfo') and dt_obj.tzinfo is None:
        # Handle naive datetime objects - assume UTC
        return dt_obj.replace(tzinfo=timezone.utc)
    else:
        # Already timezone-aware or not a datetime
        return dt_obj


def safe_datetime_delta(dt1, dt2):
    """
    Safely calculate delta between two datetime objects, ensuring timezone compatibility.

    Args:
        dt1: First datetime object
        dt2: Second datetime object

    Returns:
        timedelta object
    """
    dt1_aware = ensure_timezone_aware(dt1)
    dt2_aware = ensure_timezone_aware(dt2)

    return dt1_aware - dt2_aware


def normalize_db_datetime(dt_obj):
    """
    Normalize datetime object retrieved from database for consistent handling.

    This function can be used in model property getters to ensure consistent
    datetime handling without changing business logic.

    Args:
        dt_obj: datetime object from database

    Returns:
        normalized datetime object
    """
    return ensure_timezone_aware(dt_obj)


def safe_date_extraction(dt_or_date_obj):
    """
    Safely extract date from datetime or date object for pg8000 compatibility.

    This addresses the "'datetime.date' object has no attribute 'date'" error.

    Args:
        dt_or_date_obj: datetime or date object

    Returns:
        date object
    """
    if dt_or_date_obj is None:
        return None

    # If it's already a date object, return it directly
    if hasattr(dt_or_date_obj, 'year') and not hasattr(dt_or_date_obj, 'hour'):
        return dt_or_date_obj

    # If it's a datetime object, extract the date
    if hasattr(dt_or_date_obj, 'date'):
        return dt_or_date_obj.date()

    return dt_or_date_obj


def pg8000_utcnow():
    """
    Return timezone-aware UTC datetime for pg8000 compatibility.

    Use this instead of datetime.utcnow() in areas that need timezone-aware datetimes.
    """
    return datetime.now(timezone.utc)
