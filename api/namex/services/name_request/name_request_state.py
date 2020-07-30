from namex.constants import \
    NameRequestDraftActions, NameRequestReservedActions, NameRequestActiveActions, NameRequestCancelledActions, \
    NameRequestHoldActions, NameRequestInProgressActions, NameRequestExpiredActions, NameRequestConsumedActions, \
    NameRequestHistoricalActions, NameRequestActiveRejectedActions, NameRequestExpiredRejectedActions

from namex.models import State

from .exceptions import NameRequestException


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
    if nr.stateCd in [State.DRAFT]:
        resource.next_state_code = State.DRAFT
        nr.stateCd = State.DRAFT

        if on_success_cb:
            nr = on_success_cb(nr, resource)
        return nr


def to_cond_reserved(resource, nr, on_success_cb):
    if nr.stateCd in [State.DRAFT, State.COND_RESERVE]:
        resource.next_state_code = State.COND_RESERVE
        nr.stateCd = State.COND_RESERVE
        if on_success_cb:
            nr = on_success_cb(nr, resource)
        return nr


def to_reserved(resource, nr, on_success_cb):
    if nr.stateCd in [State.DRAFT, State.RESERVED]:
        resource.next_state_code = State.RESERVED
        nr.stateCd = State.RESERVED
        if on_success_cb:
            nr = on_success_cb(nr, resource)
        return nr


def to_conditional(resource, nr, on_success_cb):
    if nr.stateCd != State.COND_RESERVE:
        raise NameRequestException(message='Invalid state transition')

    # Check for payment
    if nr.payment_token is None:
        raise NameRequestException(message='Transition error, payment token is not defined')

    resource.next_state_code = State.CONDITIONAL
    nr.stateCd = State.CONDITIONAL
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_approved(resource, nr, on_success_cb):
    if nr.stateCd != State.RESERVED:
        raise NameRequestException(message='Invalid state transition')

    # Check for payment
    if nr.payment_token is None:
        raise NameRequestException(message='Transition error, payment token is not defined')

    resource.next_state_code = State.APPROVED
    nr.stateCd = State.APPROVED
    if on_success_cb:
        nr = on_success_cb(nr, resource)
    return nr


def to_cancelled(resource, nr, on_success_cb):
    if nr.stateCd in State.CANCELLABLE_STATES:
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
