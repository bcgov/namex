from datetime import datetime, timedelta
from flask_restx.fields import Boolean

from namex.constants import \
    NameRequestActions, \
    NameRequestDraftActions, NameRequestReservedActions, NameRequestActiveActions, NameRequestCancelledActions, \
    NameRequestHoldActions, NameRequestInProgressActions, NameRequestExpiredActions, NameRequestConsumedActions, \
    NameRequestHistoricalActions, NameRequestActiveRejectedActions, NameRequestExpiredRejectedActions, EntityTypes, \
    NameRequestCompletedActions, NameRequestPendingPaymentActions

from namex.constants import PaymentState
from namex.models import State

from .utils import has_active_payment, has_complete_payment, has_completed_or_refunded_payment
from .exceptions import NameRequestException, InvalidStateError, NameRequestIsConsumedError, NameRequestIsExpiredError, NameRequestActionError

state_transition_error_msg = 'Invalid state transition [{current_state}] -> [{next_state}]'
invalid_state_transition_msg = 'Invalid state transition [{current_state}] -> [{next_state}], valid states are [{valid_states}]'


def display_edit_action(nr_model=None):
    try:
        if nr_model and nr_model.stateCd == State.CANCELLED:
            return False

        return True
    except Exception as err:
        raise NameRequestActionError(err)


def display_upgrade_action(nr_model=None):
    try:
        # Has the request already been upgraded?
        if nr_model and nr_model.priorityCd == 'Y':
            return False

        return True
    except Exception as err:
        raise NameRequestActionError(err)


def display_cancel_action(nr_model=None):
    try:
        if (nr_model and nr_model.stateCd == State.CANCELLED) or (nr_model.stateCd not in State.CANCELLABLE_STATES):
            return False

        if nr_model and (nr_model.is_expired or nr_model.has_consumed_name):
            return False

        return True
    except Exception as err:
        raise NameRequestActionError(err)


def display_refund_action(nr_model=None):
    try:
        if nr_model and has_complete_payment(nr_model):
            return True

        return False
    except Exception as err:
        raise NameRequestActionError(err)


def display_receipt_action(nr_model=None):
    try:
        if nr_model and has_completed_or_refunded_payment(nr_model):
            return True

        return False
    except Exception as err:
        raise NameRequestActionError(err)


def display_reapply_action(nr_model=None) -> Boolean:
    """Logic for displaying the renew button."""
    try:
        if nr_model and nr_model.stateCd in (State.CONDITIONAL, State.APPROVED):
            if nr_model.expirationDate and not nr_model.is_expired and not nr_model.has_consumed_name:
                todays_date = datetime.utcnow().date()
                expiry_date = nr_model.expirationDate.date()

                delta = expiry_date - todays_date
                if delta.days <= 14 and delta.days > 0:
                    return True
        return False
    except Exception as err:
        raise NameRequestActionError(err)


def display_resubmit_action(nr_model=None) -> Boolean:
    """Logic for displaying the resubmit button."""
    try:
        if nr_model and nr_model.expirationDate and nr_model.is_expired and not nr_model.has_consumed_name:
                return True
        return False
    except Exception as err:
        raise NameRequestActionError(err)


def display_resend_action(nr_model=None):
    return True

def display_retry_payment(nr_model=None):
    """Logic for displaying retry payment button."""
    try:
        print('retry payment method')
        if nr_model and nr_model.stateCd in (State.PENDING_PAYMENT):
            payment = nr.payments.one_or_none()
            if payment:
                if payment.payment_status_code not in [PaymentState.COMPLETED.value, PaymentState.APPROVED.value]:
                    return True
        return False
    except Exception as err:
        raise NameRequestActionError(err)


def display_incorporate_action(nr_model=None):
    try:
        if nr_model and nr_model.requestTypeCd == EntityTypes.BENEFIT_COMPANY.value:
            return True

        return False
    except Exception as err:
        raise NameRequestActionError(err)


def display_retry_payment_action(nr_model=None):
    return True


def display_result_action(nr_model=None):
    return True


action_handlers = {
    NameRequestActions.EDIT.value: display_edit_action,
    NameRequestActions.UPGRADE.value: display_upgrade_action,
    NameRequestActions.CANCEL.value: display_cancel_action,
    NameRequestActions.REQUEST_REFUND.value: display_refund_action,
    NameRequestActions.RECEIPT.value: display_receipt_action,
    NameRequestActions.REAPPLY.value: display_reapply_action,
    NameRequestActions.RESUBMIT.value: display_resubmit_action,
    NameRequestActions.RESEND.value: display_resend_action,
    NameRequestActions.INCORPORATE.value: display_incorporate_action,
    NameRequestActions.RETRY_PAYMENT.value: display_retry_payment_action,
    NameRequestActions.RESULT.value: display_result_action,
}


def get_nr_state_actions(next_state, nr_model=None):
    """
    Get the corresponding actions for a particular Name Request state
    :param next_state:
    :param nr_model:
    :return:
    """
    def build_actions(state_actions_list, nr):
        try:
            return [sa for sa in state_actions_list if action_handlers[sa](nr)]
        except Exception as action_handler_err:
            raise NameRequestActionError(action_handler_err)

    try:
        return {
            State.DRAFT: build_actions(NameRequestDraftActions.list(), nr_model),
            State.PENDING_PAYMENT: build_actions(NameRequestPendingPaymentActions.list(), nr_model),
            State.RESERVED: build_actions(NameRequestReservedActions.list(), nr_model),
            State.COND_RESERVE: build_actions(NameRequestReservedActions.list(), nr_model),
            # Not expired
            State.CONDITIONAL: build_actions(NameRequestActiveActions.list(), nr_model),
            State.APPROVED: build_actions(NameRequestActiveActions.list(), nr_model),
            State.CONSUMED: build_actions(NameRequestConsumedActions.list(), nr_model),
            State.INPROGRESS: build_actions(NameRequestInProgressActions.list(), nr_model),
            State.HOLD: build_actions(NameRequestHoldActions.list(), nr_model),
            State.HISTORICAL: build_actions(NameRequestHistoricalActions.list(), nr_model),
            State.CANCELLED: build_actions(NameRequestCancelledActions.list(), nr_model),
            State.REFUND_REQUESTED: build_actions(NameRequestCancelledActions.list(), nr_model),
            State.EXPIRED: build_actions(NameRequestExpiredActions.list(), nr_model),
            State.REJECTED: build_actions(NameRequestActiveRejectedActions.list(), nr_model),
            State.COMPLETED: build_actions(NameRequestCompletedActions.list(), nr_model)
        }.get(next_state)
    except Exception as err:
        raise NameRequestActionError(err)


def is_request_editable(nr_state):
    """
    Determine whether a Name Request (NR) with a specific state is editable by a user (not a staff).

    This function takes the state of a Name Request as input and returns True if the NR
    is in a state that allows editing, or False otherwise.

    :param nr_state: The state of the Name Request to be checked.
    :type nr_state: str
    :return: True if the NR is editable, False otherwise.
    :rtype: bool
    """
    return State.DRAFT == nr_state


def is_name_request_refundable(nr_state):
    """
    Determine whether a Name Request (NR) with a specific state is cancellable by a user (not a staff).

    This function takes the state of a Name Request as input and returns True if the NR
    is in a state that allows cancellation, or False otherwise.

    :param nr_state: The state of the Name Request to be checked.
    :type nr_state: str
    :return: True if the NR is cancellable, False otherwise.
    :rtype: bool
    """
    return State.DRAFT == nr_state


def to_draft(resource, nr, on_success_cb=None):
    valid_states = [State.DRAFT, State.INPROGRESS, State.PENDING_PAYMENT]
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.DRAFT,
            valid_states=', '.join(valid_states)
        ))

    resource.next_state_code = State.DRAFT
    nr.stateCd = State.DRAFT

    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_inprogress(resource, nr, on_success_cb=None):
    valid_states = [State.DRAFT, State.INPROGRESS]
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.INPROGRESS,
            valid_states=', '.join(valid_states)
        ))

    resource.next_state_code = State.INPROGRESS
    nr.stateCd = State.INPROGRESS

    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_cond_reserved(resource, nr, on_success_cb):
    valid_states = [State.DRAFT, State.COND_RESERVE]
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.COND_RESERVE,
            valid_states=', '.join(valid_states)
        ))

    resource.next_state_code = State.COND_RESERVE
    nr.stateCd = State.COND_RESERVE
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_reserved(resource, nr, on_success_cb):
    valid_states = [State.DRAFT, State.RESERVED]
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.RESERVED,
            valid_states=', '.join(valid_states)
        ))

    resource.next_state_code = State.RESERVED
    nr.stateCd = State.RESERVED
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_conditional(resource, nr, on_success_cb):
    valid_states = [State.DRAFT, State.COND_RESERVE, State.CONDITIONAL, State.INPROGRESS]
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.CONDITIONAL,
            valid_states=', '.join(valid_states)
        ))

    resource.next_state_code = State.CONDITIONAL
    nr.stateCd = State.CONDITIONAL
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_approved(resource, nr, on_success_cb):
    valid_states = [State.RESERVED, State.APPROVED, State.INPROGRESS]
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.APPROVED,
            valid_states=', '.join(valid_states)
        ))

    resource.next_state_code = State.APPROVED
    nr.stateCd = State.APPROVED
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_rejected(resource, nr, on_success_cb):
    valid_states = [State.REJECTED]
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.REJECTED,
            valid_states=', '.join(valid_states)
        ))

    resource.next_state_code = State.REJECTED
    nr.stateCd = State.REJECTED
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_consumed(resource, nr, on_success_cb):
    valid_states = [State.CONSUMED]
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.CONSUMED,
            valid_states=', '.join(valid_states)
        ))

    resource.next_state_code = State.CONSUMED
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_pending_payment(resource, nr, on_success_cb):
    valid_states = [State.PENDING_PAYMENT]
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.PENDING_PAYMENT,
            valid_states=', '.join(valid_states)
        ))

    resource.next_state_code = State.PENDING_PAYMENT
    nr.stateCd = State.PENDING_PAYMENT
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_cancelled(resource, nr, on_success_cb):
    # Allow cancelled to cancelled state transition here, if this is not to be allowed, catch it when validating the request
    # valid_states = [State.APPROVED, State.CONDITIONAL]
    valid_states = State.CANCELLABLE_STATES
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.CANCELLED,
            valid_states=', '.join(valid_states)
        ))

    if nr.is_expired is True:
        raise NameRequestIsExpiredError()

    if nr.has_consumed_name is True:
        raise NameRequestIsConsumedError()

    resource.next_state_code = State.CANCELLED
    nr.stateCd = State.CANCELLED
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_refund_requested(resource, nr, on_success_cb):
    # Allow cancelled to cancelled state transition here, if this is not to be allowed, catch it when validating the request
    # valid_states = [State.APPROVED, State.CONDITIONAL]
    valid_states = State.CANCELLABLE_STATES
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.REFUND_REQUESTED,
            valid_states=', '.join(valid_states)
        ))

    # TODO: Confirm that we don't need to check for expiry!
    # if nr.is_expired is True:
    #    raise NameRequestIsExpiredError()
    # if nr.has_consumed_name is True:
    #    raise NameRequestIsConsumedError()

    resource.next_state_code = State.REFUND_REQUESTED
    nr.stateCd = State.REFUND_REQUESTED
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def apply_nr_state_change(self, name_request, next_state, on_success=None):
    """
    This is where we handle entity state changes.
    We ONLY change entity state from within this procedure to avoid accidental or undesired state mutation.
    This is defined outside of the BaseNameRequest class so we can functionally test it.
    :param self:
    :param name_request:
    :param next_state:
    :param on_success:
    :return:
    """
    return {
        State.INPROGRESS: to_inprogress,
        State.DRAFT: to_draft,
        State.COND_RESERVE: to_cond_reserved,
        State.RESERVED: to_reserved,
        State.CONDITIONAL: to_conditional,
        State.APPROVED: to_approved,
        State.REJECTED: to_rejected,
        State.CONSUMED: to_consumed,
        State.CANCELLED: to_cancelled,
        State.REFUND_REQUESTED: to_refund_requested,
        State.PENDING_PAYMENT: to_pending_payment
    }.get(next_state)(self, name_request, on_success)
