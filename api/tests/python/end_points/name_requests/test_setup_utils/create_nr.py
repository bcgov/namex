from namex.models import State
from tests.python.unit.test_setup_utils.build_nr import build_nr


def create_nr(nr_state, data=None):
    """
    Creates an NR in a given state.
    :param nr_state:
    :param data:
    :return:
    """

    return {
        State.DRAFT: create_draft,
        State.RESERVED: create_reserved,
        State.COND_RESERVE: create_cond_reserved,
        State.CONDITIONAL: create_conditional,
        State.APPROVED: create_approved,
    }.get(nr_state)(data)


def create_draft(data=None):
    nr = build_nr(State.DRAFT, data)
    nr.nrNum = 'NR 0000002'
    nr.save_to_db()

    return nr


def create_cond_reserved(data=None):
    nr = build_nr(State.COND_RESERVE, data)
    nr.nrNum = 'NR 0000002'
    nr.save_to_db()

    return nr


def create_reserved(data=None):
    nr = build_nr(State.RESERVED, data)
    nr.nrNum = 'NR 0000002'
    nr.save_to_db()

    return nr


def create_conditional(data=None):
    nr = build_nr(State.CONDITIONAL, data)
    nr.nrNum = 'NR 0000002'
    nr.save_to_db()

    return nr


def create_approved(data=None):
    nr = build_nr(State.APPROVED, data)
    nr.nrNum = 'NR 0000002'
    nr.save_to_db()

    return nr
