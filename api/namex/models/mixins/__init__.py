from datetime import date, datetime
from http import HTTPStatus
from sqlalchemy import desc, event, inspect, or_
from sqlalchemy.ext.hybrid import hybrid_property

class PaymentModelMixin:
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

        if self.locked or \
                (self._payment_token and self._filing_json):
            self._payment_completion_date = value
            if self.effective_date is None or \
                    self.effective_date <= self._payment_completion_date:
                self._status = Filing.Status.COMPLETED.value
        else:
            raise BusinessException(
                error="Payment Dates cannot set for unlocked filings unless the filing hasn't been saved yet.",
                status_code=HTTPStatus.FORBIDDEN
            )

    @property
    def locked(self):
        """Return the locked state of the filing.

        Once a filing, with valid json has an invoice attached, it can no longer be altered and is locked.
        Exception to this rule, payment_completion_date requires the filing to be locked.
        """
        insp = inspect(self)
        attr_state = insp.attrs._payment_token  # pylint: disable=protected-access;
        # inspect requires the member, and the hybrid decorator doesn't help us here
        if (self._payment_token and not attr_state.history.added) or self.colin_event_ids:
            return True

        return False

    def set_processed(self):
        """Assign the completion date, unless it is already set."""
        if not self._completion_date:
            self._completion_date = datetime.utcnow()

    @staticmethod
    def _raise_default_lock_exception():
        raise BusinessException(
            error='Filings cannot be changed after the invoice is created.',
            status_code=HTTPStatus.FORBIDDEN
        )

    @staticmethod
    def get_temp_reg_filing(temp_reg_id: str = None, filing_id: str = None):
        """Return a Filing by it's payment token."""
        filing = db.session.query(Filing). \
            filter(Filing.temp_reg == temp_reg_id). \
            filter(Filing.id == filing_id). \
            one_or_none()
        return filing

    @staticmethod
    def get_filing_by_payment_token(token: str):
        """Return a Filing by it's payment token."""
        filing = db.session.query(Filing). \
            filter(Filing.payment_token == token). \
            one_or_none()
        return filing


    def save(self):
        """Save and commit immediately."""
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        """Save toThe session, do not commit immediately."""
        db.session.add(self)

    def delete(self):
        """Raise an error if the filing is locked."""
        if self.locked:
            raise BusinessException(
                error='Deletion not allowed.',
                status_code=HTTPStatus.FORBIDDEN
            )
        db.session.delete(self)
        db.session.commit()

    def reset_filing_to_draft(self):
        """Reset Filing to draft and remove payment token."""
        self._status = Filing.Status.DRAFT.value
        self._payment_token = None
        self.save()


@event.listens_for(Filing, 'before_delete')
def block_filing_delete_listener_function(mapper, connection, target):  # pylint: disable=unused-argument
    """Raise an error when a delete is attempted on a Filing."""
    filing = target

    if filing.locked:
        raise BusinessException(
            error='Deletion not allowed.',
            status_code=HTTPStatus.FORBIDDEN
        )


