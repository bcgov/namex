from namex.constants import \
    NameRequestDraftActions, NameRequestReservedActions, NameRequestActiveActions, NameRequestCancelledActions, \
    NameRequestHoldActions, NameRequestInProgressActions, NameRequestExpiredActions, NameRequestConsumedActions, \
    NameRequestHistoricalActions, NameRequestActiveRejectedActions, NameRequestExpiredRejectedActions

from namex.models import State

from .exceptions import NameRequestException, InvalidStateError

state_transition_error_msg = 'Invalid state transition [{current_state}] -> [{next_state}]'
invalid_state_transition_msg = 'Invalid state transition [{current_state}] -> [{next_state}], valid states are [{valid_states}]'


def get_nr_state_actions(next_state):
    """
    Get the corresponding actions for a particular Name Request state
    :param next_state:
    :return:
    """

    return {
        State.DRAFT: NameRequestDraftActions.list(),
        State.RESERVED: NameRequestReservedActions.list(),
        State.COND_RESERVE: NameRequestReservedActions.list(),
        # Not expired
        State.CONDITIONAL: NameRequestActiveActions.list(),
        State.APPROVED: NameRequestActiveActions.list(),
        # TODO: What if CONDITIONAL or APPROVED is expired, we need to be able to handle that here!
        State.INPROGRESS: NameRequestInProgressActions.list(),
        State.HOLD: NameRequestHoldActions.list(),
        State.HISTORICAL: NameRequestHistoricalActions.list(),
        State.CANCELLED: NameRequestCancelledActions.list(),
        State.REJECTED: NameRequestActiveRejectedActions.list()
        # TODO: What if REJECTED is expired, we need to be able to handle that here!
    }.get(next_state)


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
    if nr.payment_token is None:
        raise NameRequestException(message=state_transition_error_msg.format(current_state=nr.stateCd, next_state=State.CONDITIONAL) + ', payment token is not defined')

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
    if nr.payment_token is None:
        raise NameRequestException(message=state_transition_error_msg.format(current_state=nr.stateCd, next_state=State.APPROVED) + ', payment token is not defined')

    resource.next_state_code = State.APPROVED
    nr.stateCd = State.APPROVED
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_cancelled(resource, nr, on_success_cb):
    valid_states = State.CANCELLABLE_STATES
    if nr.stateCd not in valid_states:
        raise InvalidStateError(message=invalid_state_transition_msg.format(
            current_state=nr.stateCd,
            next_state=State.CANCELLED,
            valid_states=', '.join(valid_states)
        ))

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
