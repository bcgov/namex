from namex.models import State, StateSchema


def test_state_draft(session):
    """Start with a blank database."""

    # setup

    # get the name from the data base & assert it was updated
    state = State.query.filter_by(cd=State.DRAFT).one_or_none()
    assert state is not None
    assert state.cd is not None
    assert state.cd == State.DRAFT


def test_all_valid_states_in_db(session):
    states = State.query.all()

    state_cnt = 0
    for state in states:
        state_cnt += 1
        if state.cd not in State.ALL_STATES:
            print('{} not found in {}'.format(state.cd, State.ALL_STATES))
            assert False

    assert len(states) == state_cnt
