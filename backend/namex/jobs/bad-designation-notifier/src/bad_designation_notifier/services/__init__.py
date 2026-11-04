"""Service layer package for bad designation notifier."""
# services/__init__.py

from .database_service import get_bad_designations
from .email_service import send_email_notification

__all__ = ["get_bad_designations", "send_email_notification"]
