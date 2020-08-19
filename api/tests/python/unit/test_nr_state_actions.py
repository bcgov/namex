"""
Unit tests for Name Request state actions.
"""
from datetime import datetime, timedelta

from namex.constants import \
    NameRequestDraftActions, NameRequestReservedActions, NameRequestActiveActions, NameRequestCancelledActions, \
    NameRequestHoldActions, NameRequestInProgressActions, NameRequestExpiredActions, NameRequestConsumedActions, \
    NameRequestHistoricalActions, NameRequestActiveRejectedActions, NameRequestExpiredRejectedActions

from namex.models import State, Request
from namex.services.name_request.name_request_state import get_nr_state_actions


def test_nr_state_actions():
    nr_model = Request()
    nr_model.expirationDate = datetime.utcnow() + timedelta(days=3)
    nr_model.priorityCd = None
    nr_model.priorityDate = None

    print('\n Draft state actions \n')
    print(repr(NameRequestDraftActions.list()))
    actions = get_nr_state_actions(State.DRAFT, nr_model)
    print(repr(actions))

    print('\n Reserved state actions \n')
    print(repr(NameRequestReservedActions.list()))
    actions = get_nr_state_actions(State.RESERVED, nr_model)
    print(repr(actions))

    print('\n Conditionally reserved state actions \n')
    print(repr(NameRequestReservedActions.list()))
    actions = get_nr_state_actions(State.COND_RESERVE, nr_model)
    print(repr(actions))

    print('\n Conditional state actions \n')
    print(repr(NameRequestActiveActions.list()))
    actions = get_nr_state_actions(State.CONDITIONAL, nr_model)
    print(repr(actions))

    print('\n Approved state actions \n')
    print(repr(NameRequestActiveActions.list()))
    actions = get_nr_state_actions(State.APPROVED, nr_model)
    print(repr(actions))

    print('\n In Progress state actions \n')
    print(repr(NameRequestInProgressActions.list()))
    actions = get_nr_state_actions(State.INPROGRESS, nr_model)
    print(repr(actions))

    print('\n Hold state actions \n')
    print(repr(NameRequestHoldActions.list()))
    actions = get_nr_state_actions(State.HOLD, nr_model)
    print(repr(actions))

    print('\n Historical state actions \n')
    print(repr(NameRequestHistoricalActions.list()))
    actions = get_nr_state_actions(State.HISTORICAL, nr_model)
    print(repr(actions))

    print('\n Cancelled state actions \n')
    print(repr(NameRequestCancelledActions.list()))
    actions = get_nr_state_actions(State.CANCELLED, nr_model)
    print(repr(actions))

    print('\n Rejected state actions \n')
    print(repr(NameRequestActiveRejectedActions.list()))
    actions = get_nr_state_actions(State.REJECTED, nr_model)
    print(repr(actions))
