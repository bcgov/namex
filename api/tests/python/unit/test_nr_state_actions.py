"""
Unit tests for Name Request state actions.
"""

from namex.constants import \
    NameRequestDraftActions, NameRequestReservedActions, NameRequestActiveActions, NameRequestCancelledActions, \
    NameRequestHoldActions, NameRequestInProgressActions, NameRequestExpiredActions, NameRequestConsumedActions, \
    NameRequestHistoricalActions, NameRequestActiveRejectedActions, NameRequestExpiredRejectedActions

from namex.models import State
from namex.services.name_request.name_request_state import get_nr_state_actions


def test_nr_state_actions():
    print('\n Draft state actions \n')
    print(repr(NameRequestDraftActions.list()))
    actions = get_nr_state_actions(State.DRAFT)
    print(repr(actions))

    print('\n Reserved state actions \n')
    print(repr(NameRequestReservedActions.list()))
    actions = get_nr_state_actions(State.RESERVED)
    print(repr(actions))

    print('\n Conditionally reserved state actions \n')
    print(repr(NameRequestReservedActions.list()))
    actions = get_nr_state_actions(State.COND_RESERVE)
    print(repr(actions))

    print('\n Conditional state actions \n')
    print(repr(NameRequestActiveActions.list()))
    actions = get_nr_state_actions(State.CONDITIONAL)
    print(repr(actions))

    print('\n Approved state actions \n')
    print(repr(NameRequestActiveActions.list()))
    actions = get_nr_state_actions(State.APPROVED)
    print(repr(actions))

    print('\n In Progress state actions \n')
    print(repr(NameRequestInProgressActions.list()))
    actions = get_nr_state_actions(State.INPROGRESS)
    print(repr(actions))

    print('\n Hold state actions \n')
    print(repr(NameRequestHoldActions.list()))
    actions = get_nr_state_actions(State.HOLD)
    print(repr(actions))

    print('\n Historical state actions \n')
    print(repr(NameRequestHistoricalActions.list()))
    actions = get_nr_state_actions(State.HISTORICAL)
    print(repr(actions))

    print('\n Cancelled state actions \n')
    print(repr(NameRequestCancelledActions.list()))
    actions = get_nr_state_actions(State.CANCELLED)
    print(repr(actions))

    print('\n Rejected state actions \n')
    print(repr(NameRequestActiveRejectedActions.list()))
    actions = get_nr_state_actions(State.REJECTED)
    print(repr(actions))
