from app.models import Name, NameSchema, State, StateSchema
import sys

def test_state_draft(session):
    """Start with a blank database."""

    # setup
    state_schema = StateSchema()

    # get the name from the data base & assert it was updated
    state = State.query.filter_by(cd=State.DRAFT).one_or_none()
    assert state is not None
    assert state.cd is not None
    assert state.cd == State.DRAFT
