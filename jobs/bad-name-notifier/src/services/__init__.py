# services/__init__.py

from .database_service import get_bad_names
from .email_service import send_email_notification

__all__ = ["get_bad_names", "send_email_notification"]
