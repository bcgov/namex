from namex.models import State, Request as RequestDAO, Name as NameDAO


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
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.DRAFT
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    return nr


def create_cond_reserved():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.COND_RESERVE
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    return nr


def create_reserved():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.RESERVED
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    return nr


def create_conditional():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.CONDITIONAL
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    return nr


def create_approved():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.APPROVED
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr.names = [name1]
    nr.save_to_db()

    return nr
