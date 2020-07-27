from namex.models import State, Request as RequestDAO, Name as NameDAO
from tests.python.unit.test_setup_utils.build_nr import build_nr


def create_nr(nr_state):
    """
    Creates an NR in a given state.
    :param nr_state:
    :return:
    """
    return {
        State.DRAFT: create_draft,
        State.RESERVED: create_reserved,
        State.COND_RESERVE: create_cond_reserved,
        State.CONDITIONAL: create_conditional,
        State.APPROVED: create_approved
    }.get(nr_state)()


def create_draft():
    nr = build_nr(State.DRAFT)
    nr.save_to_db()

    return nr


def create_cond_reserved():
    nr = build_nr(State.COND_RESERVE)
    nr.save_to_db()

    return nr


def create_reserved():
    nr = build_nr(State.RESERVED)
    nr.save_to_db()

    return nr


def create_conditional():
    nr = build_nr(State.CONDITIONAL)
    nr.save_to_db()

    return nr


def create_approved():
    nr = build_nr(State.APPROVED)
    nr.save_to_db()

    return nr
