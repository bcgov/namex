from datetime import datetime

# TODO: We may need this import later
# from http import HTTPStatus
from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property

COMPLETED_VALUE = None


class PaymentModelMixin:
    _payment_token = None
    _payment_status_code = None
    _payment_completion_date = None
    _effective_date = None
    _completion_date = None
    _status = None

    @hybrid_property
    def payment_status_code(self):
        """Property containing the payment error type."""
        return self._payment_status_code

    @payment_status_code.setter
    def payment_status_code(self, error_type: str):
        if self.locked:
            self._raise_default_lock_exception()

        self._payment_status_code = error_type

    @hybrid_property
    def payment_token(self):
        """Property containing the payment token."""
        return self._payment_token

    @payment_token.setter
    def payment_token(self, token: int):
        if self.locked:
            self._raise_default_lock_exception()

        self._payment_token = token

    @hybrid_property
    def payment_completion_date(self):
        """Property containing the date the payment cleared."""
        return self._payment_completion_date

    @payment_completion_date.setter
    def payment_completion_date(self, value: datetime):
        if self.locked or self._payment_token:
            self._payment_completion_date = value

            if self._effective_date is None or self._effective_date <= self._payment_completion_date:
                self._status = COMPLETED_VALUE
        else:
            # TODO: Handle exceptions
            # raise Exception(
            #    error="Payment Dates cannot set for unlocked filings unless the filing hasn't been saved yet.",
            #    status_code=HTTPStatus.FORBIDDEN
            # )
            pass

    @property
    def locked(self):
        """Return the locked state of the filing.

        Once a filing, with valid json has an invoice attached, it can no longer be altered and is locked.
        Exception to this rule, payment_completion_date requires the filing to be locked.
        """
        insp = inspect(self)
        attr_state = insp.attrs._payment_token

        # Inspect requires the member, and the hybrid decorator doesn't help us here
        if self._payment_token and not attr_state.history.added:
            return True

        return False

    def set_processed(self):
        """Assign the completion date, unless it is already set."""
        if not self._completion_date:
            self._completion_date = datetime.utcnow()

    @staticmethod
    def _raise_default_lock_exception():
        # TODO: Handle exceptions
        # raise Exception(
        #     error='Entity cannot be changed after the invoice is created.',
        #     status_code=HTTPStatus.FORBIDDEN
        # )
        pass

    @staticmethod
    def get_by_payment_token(token: str):
        """Optional member to get a payment using its token id."""
        pass

    def reset_filing_to_draft(self, draft_value):
        """Reset Filing to draft and remove payment token."""
        self._status = draft_value
        self._payment_token = None
