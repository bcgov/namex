from datetime import datetime, timedelta

from namex.constants import \
    NameRequestActions, \
    NameRequestDraftActions, NameRequestReservedActions, NameRequestActiveActions, NameRequestCancelledActions, \
    NameRequestHoldActions, NameRequestInProgressActions, NameRequestExpiredActions, NameRequestConsumedActions, \
    NameRequestHistoricalActions, NameRequestActiveRejectedActions, NameRequestExpiredRejectedActions

from namex.models import State

from .utils import has_active_payment, has_complete_payment
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
        if nr_model and has_complete_payment(nr_model):
            return True

        return False
    except Exception as err:
        raise NameRequestActionError(err)


def display_reapply_action(nr_model=None):
    try:
        if nr_model and nr_model.stateCd in (State.CONDITIONAL, State.APPROVED):
            if nr_model.expirationDate and not nr_model.is_expired:
                todays_date = datetime.utcnow().date()
                expiry_date = nr_model.expirationDate.date()

                delta = expiry_date - todays_date
                if delta.days <= 5:
                    return True
        return False
    except Exception as err:
        raise NameRequestActionError(err)


def display_resend_action(nr_model=None):
    return True


action_handlers = {
    NameRequestActions.EDIT.value: display_edit_action,
    NameRequestActions.UPGRADE.value: display_upgrade_action,
    NameRequestActions.CANCEL.value: display_cancel_action,
    NameRequestActions.REFUND.value: display_refund_action,
    NameRequestActions.RECEIPT.value: display_receipt_action,
    NameRequestActions.REAPPLY.value: display_reapply_action,
    NameRequestActions.RESEND.value: display_resend_action
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
            State.RESERVED: build_actions(NameRequestReservedActions.list(), nr_model),
            State.COND_RESERVE: build_actions(NameRequestReservedActions.list(), nr_model),
            # Not expired
            State.CONDITIONAL: build_actions(NameRequestActiveActions.list(), nr_model),
            State.APPROVED: build_actions(NameRequestActiveActions.list(), nr_model),
            State.INPROGRESS: build_actions(NameRequestInProgressActions.list(), nr_model),
            State.HOLD: build_actions(NameRequestHoldActions.list(), nr_model),
            State.HISTORICAL: build_actions(NameRequestHistoricalActions.list(), nr_model),
            State.CANCELLED: build_actions(NameRequestCancelledActions.list(), nr_model),
            State.REJECTED: build_actions(NameRequestActiveRejectedActions.list(), nr_model)
        }.get(next_state)
    except Exception as err:
        raise NameRequestActionError(err)


def to_draft(resource, nr, on_success_cb=None):
    valid_states = [State.DRAFT, State.INPROGRESS]
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

    # Check for payment
    # TODO: Fix this!
    # if nr.payment_token is None:
    #     raise NameRequestException(message=state_transition_error_msg.format(current_state=nr.stateCd, next_state=State.CONDITIONAL) + ', payment token is not defined')

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

    # Check for payment
    # TODO: Fix this!
    # if nr.payment_token is None:
    #     raise NameRequestException(message=state_transition_error_msg.format(current_state=nr.stateCd, next_state=State.APPROVED) + ', payment token is not defined')

    resource.next_state_code = State.APPROVED
    nr.stateCd = State.APPROVED
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
        State.DRAFT: to_draft,
        State.RESERVED: to_reserved,
        State.COND_RESERVE: to_cond_reserved,
        State.CONDITIONAL: to_conditional,
        State.APPROVED: to_approved,
        State.CANCELLED: to_cancelled
    }.get(next_state)(self, name_request, on_success)
