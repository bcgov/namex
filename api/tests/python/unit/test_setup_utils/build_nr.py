from namex.models import State, Request as RequestDAO, Name as NameDAO

default_test_names = [
    {
        'name': 'ABC ENGINEERING',
        "choice": 1,
        "designation": "LTD.",
        "name_type_cd": "CO",
        "consent_words": "",
        "conflict1": "ABC ENGINEERING LTD.",
        "conflict1_num": "0515211"
    },
    {
        'name': 'ABC PLUMBING',
        "choice": 1,
        "designation": "LTD.",
        "name_type_cd": "CO",
        "consent_words": "",
        "conflict1": "ABC PLUMBING LTD.",
        "conflict1_num": "0515211"
    }
]


def build_name(test_name):
    name = NameDAO()
    name.id = test_name.get('id', None)
    name.choice = 1
    name.name = test_name.get('name', '')
    name.designation = test_name.get('designation', '')
    name.name_type_cd = test_name.get('name_type_cd', '')
    name.consent_words = test_name.get('consent_words', '')
    name.conflict1 = test_name.get('conflict1', '')
    name.conflict1_num = test_name.get('conflict1_num', '')

    return name


def build_nr(nr_state, test_names=None):
    """
    Creates an NR in a given state.
    :param nr_state:
    :param test_names:
    :return:
    """
    test_names = test_names if test_names else default_test_names

    return {
        State.DRAFT: build_draft,
        State.RESERVED: build_reserved,
        State.COND_RESERVE: build_cond_reserved,
        State.CONDITIONAL: build_conditional,
        State.APPROVED: build_approved
    }.get(nr_state)(test_names)


def build_draft(test_names):
    nr = RequestDAO()
    nr.stateCd = State.DRAFT
    nr.requestId = 1460775
    nr._source = 'NRO'

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name))

    return nr


def build_cond_reserved(test_names):
    nr = RequestDAO()
    nr.stateCd = State.COND_RESERVE
    nr.requestId = 1460775
    nr._source = 'NRO'

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name))

    return nr


def build_reserved(test_names):
    nr = RequestDAO()
    nr.stateCd = State.RESERVED
    nr.requestId = 1460775
    nr._source = 'NRO'

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name))

    return nr


def build_conditional(test_names):
    nr = RequestDAO()
    nr.stateCd = State.CONDITIONAL
    nr.requestId = 1460775
    nr._source = 'NRO'

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name))

    return nr


def build_approved(test_names):
    nr = RequestDAO()
    nr.stateCd = State.APPROVED
    nr.requestId = 1460775
    nr._source = 'NRO'

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name))

    return nr
