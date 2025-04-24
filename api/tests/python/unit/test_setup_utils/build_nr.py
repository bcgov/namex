from namex.models import db, State, Request as RequestDAO, Name as NameDAO

default_test_names = [
    {
        'name': 'ABC ENGINEERING',
        'choice': 1,
        'designation': 'LTD.',
        'name_type_cd': 'CO',
        'consent_words': '',
        'conflict1': 'ABC ENGINEERING LTD.',
        'conflict1_num': '0515211',
    },
    {
        'name': 'ABC PLUMBING',
        'choice': 1,
        'designation': 'LTD.',
        'name_type_cd': 'CO',
        'consent_words': '',
        'conflict1': 'ABC PLUMBING LTD.',
        'conflict1_num': '0515211',
    },
]


def build_name(test_name, generate_id_seq=True):
    name = NameDAO()
    if generate_id_seq:
        seq = db.Sequence('names_id_seq')
        name_id = db.engine.execute(seq)
        name.id = test_name.get('id', name_id)

    name.choice = 1
    name.name = test_name.get('name', '')
    name.designation = test_name.get('designation', '')
    name.name_type_cd = test_name.get('name_type_cd', '')
    name.consent_words = test_name.get('consent_words', '')
    name.conflict1 = test_name.get('conflict1', '')
    name.conflict1_num = test_name.get('conflict1_num', '')
    name.corpNum = test_name.get('corpNum', None)

    return name


def build_nr(nr_state, data=None, test_names=None, generate_id_seq=None):
    """
    Creates an NR in a given state.
    :param nr_state:
    :param data:
    :param test_names:
    :param generate_id_seq:
    :return:
    """
    test_names = test_names if test_names else default_test_names

    return {
        State.DRAFT: build_draft,
        State.EXPIRED: build_expired,
        State.RESERVED: build_reserved,
        State.COND_RESERVE: build_cond_reserved,
        State.CONDITIONAL: build_conditional,
        State.CONSUMED: build_consumed,
        State.APPROVED: build_approved,
        State.CANCELLED: build_cancelled,
        State.HOLD: build_hold,
        State.INPROGRESS: build_in_progress,
        State.HISTORICAL: build_historical,
        State.REJECTED: build_rejected,
    }.get(nr_state)(data, test_names, generate_id_seq)


def build_draft(data=None, test_names=None, generate_id_seq=None):
    try:
        nr = RequestDAO()

        # Set defaults, if these exist in the provided data they will be overwritten
        nr.stateCd = State.DRAFT
        nr.requestId = 1460775
        nr._source = 'NRO'

        if not data:
            data = {}

        # Map the data, if provided
        for key, value in data.items():
            # Don't set list attrs, they have to be set separately to handle sequences
            if hasattr(nr, key) and not isinstance(data.get(key), list):
                nr.__setattr__(key, value)

        nr.names = []
        for test_name in test_names:
            nr.names.append(build_name(test_name, generate_id_seq))

        return nr
    except Exception as err:
        print(repr(err))


def build_cond_reserved(data=None, test_names=None, generate_id_seq=None):
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.COND_RESERVE
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name))

    return nr


def build_reserved(data=None, test_names=None, generate_id_seq=None):
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.RESERVED
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name, generate_id_seq))

    return nr


def build_conditional(data=None, test_names=None, generate_id_seq=None):
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.CONDITIONAL
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name, generate_id_seq))

    return nr


def build_consumed(data=None, test_names=None, generate_id_seq=None):
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.CONSUMED
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name, generate_id_seq))

    return nr


def build_approved(data=None, test_names=None, generate_id_seq=None):
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.APPROVED
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name, generate_id_seq))

    return nr


def build_expired(data=None, test_names=None, generate_id_seq=None):
    """
    :param data:
    :param test_names:
    :param generate_id_seq:
    :return:
    """
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.EXPIRED
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name, generate_id_seq))

    return nr


def build_cancelled(data=None, test_names=None, generate_id_seq=None):
    """
    :param data:
    :param test_names:
    :param generate_id_seq:
    :return:
    """
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.CANCELLED
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name, generate_id_seq))

    return nr


def build_hold(data=None, test_names=None, generate_id_seq=None):
    """
    :param data:
    :param test_names:
    :param generate_id_seq:
    :return:
    """
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.HOLD
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name, generate_id_seq))

    return nr


def build_in_progress(data=None, test_names=None, generate_id_seq=None):
    """
    :param data:
    :param test_names:
    :param generate_id_seq:
    :return:
    """
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.INPROGRESS
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name, generate_id_seq))

    return nr


def build_historical(data=None, test_names=None, generate_id_seq=None):
    """
    :param data:
    :param test_names:
    :param generate_id_seq:
    :return:
    """
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.HISTORICAL
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name, generate_id_seq))

    return nr


def build_rejected(data=None, test_names=None, generate_id_seq=None):
    """
    :param data:
    :param test_names:
    :param generate_id_seq:
    :return:
    """
    nr = RequestDAO()

    # Set defaults, if these exist in the provided data they will be overwritten
    nr.stateCd = State.REJECTED
    nr.requestId = 1460775
    nr._source = 'NRO'

    if not data:
        data = {}

    # Map the data, if provided
    for key, value in data.items():
        # Don't set list attrs, they have to be set separately to handle sequences
        if hasattr(nr, key) and not isinstance(data.get(key), list):
            nr.__setattr__(key, value)

    nr.names = []
    for test_name in test_names:
        nr.names.append(build_name(test_name, generate_id_seq))

    return nr
