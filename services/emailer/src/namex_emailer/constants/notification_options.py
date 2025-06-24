from enum import Enum


class Option(Enum):
    """NR notification option."""

    # Notification options (no attachment in the email)
    BEFORE_EXPIRY = "before-expiry"
    EXPIRED = "expired"
    RENEWAL = "renewal"
    UPGRADE = "upgrade"
    REFUND = "refund"

    # decision options (has attachment in the email)
    APPROVED = "APPROVED"
    CONDITIONAL = "CONDITIONAL"
    REJECTED = "REJECTED"

    CONSENT_RECEIVED = "CONSENT_RECEIVED"


# Group definitions
NOTIFICATION_OPTIONS = {
    Option.BEFORE_EXPIRY,
    Option.EXPIRED,
    Option.RENEWAL,
    Option.UPGRADE,
    Option.REFUND,
}

DECISION_OPTIONS = {
    Option.APPROVED,
    Option.CONDITIONAL,
    Option.REJECTED,
}
