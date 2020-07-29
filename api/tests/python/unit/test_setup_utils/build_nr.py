from namex.models import State, Request as RequestDAO, Name as NameDAO

test_names = [
    {'name': 'ABC PLUMBING', 'designation': 'LTD.'},
    {'name': 'ABC ENGINEERING', 'designation': 'LTD.'}
]


def build_nr(nr_state):
    """
    Creates an NR in a given state.
    :param nr_state:
    :return:
    """
    return {
        State.DRAFT: build_draft,
        State.RESERVED: build_reserved,
        State.COND_RESERVE: build_cond_reserved,
        State.CONDITIONAL: build_conditional,
        State.APPROVED: build_approved
    }.get(nr_state)()


def build_draft():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.DRAFT
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = test_names[0].get('name')
    nr.names = [name1]

    return nr


def build_cond_reserved():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.COND_RESERVE
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = test_names[0].get('name')
    nr.names = [name1]

    return nr


def build_reserved():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.RESERVED
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = test_names[0].get('name')
    nr.names = [name1]

    return nr


def build_conditional():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.CONDITIONAL
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = test_names[0].get('name')
    nr.names = [name1]

    return nr


def build_approved():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.APPROVED
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = test_names[0].get('name')
    nr.names = [name1]

    return nr
