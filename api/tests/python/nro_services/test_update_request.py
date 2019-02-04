import cx_Oracle
from namex import nro
from namex.models import User
from tests.python import integration_oracle_namesdb, integration_oracle_local_namesdb
from namex.services.nro.change_nr import \
    _update_nro_names, \
    _update_request, \
    _get_event_id, \
    _create_nro_transaction, \
    _update_nro_request_state


@integration_oracle_namesdb
def test_nro_connection(app):

    conn = nro.connection
    assert type(conn) is cx_Oracle.Connection


class NamesList:
    mynames = []
    def addNames(self, names):
        self.mynames = names

    def all(self):
        return iter(self.mynames)


class FakeRequest:
    requestId = '42'
    previousRequestId = '15'
    names = NamesList();


class FakeName:
    nameId = '42'
    name = ''
    choice = 1


@integration_oracle_namesdb
@integration_oracle_local_namesdb
def test_preserves_previous_request_id(app):
    con = nro.connection
    cursor = con.cursor()
    cursor.execute("""
        declare exist number;
        begin
            select count(1) into exist from user_tables where table_name='REQUEST';
            if exist = 1 then
                execute immediate 'drop table request';
            end if;
        end;        
    """)
    cursor.execute('create table request (request_id varchar(10), previous_request_id varchar(10))')
    cursor.execute("insert into request(request_id, previous_request_id) values('42', '99')")
    _update_request(cursor, FakeRequest(), None, {
        'is_changed__request': False,
        'is_changed__previous_request': True
    })

    cursor.execute("select previous_request_id from request")
    (value,) = cursor.fetchone()

    assert '99' == value


@integration_oracle_namesdb
def test_create_nro_transaction(app):
    con = nro.connection
    cursor = con.cursor()

    eid = _get_event_id(cursor)

    fake_request = FakeRequest()
    fake_request.requestId = 884047

    _create_nro_transaction(cursor, fake_request, eid)

    cursor.execute("select event_id, transaction_type_cd from transaction where request_id = {} order by event_id desc".format(fake_request.requestId))
    (value, transaction_type_cd) = cursor.fetchone()

    assert eid == value
    assert value != 0
    assert value != None
    assert transaction_type_cd == 'ADMIN'


@integration_oracle_namesdb
def test_create_nro_transaction_with_type(app):
    con = nro.connection
    cursor = con.cursor()

    eid = _get_event_id(cursor)

    fake_request = FakeRequest()
    fake_request.requestId = 884047

    _create_nro_transaction(cursor, fake_request, eid, 'CORRT')

    cursor.execute("select event_id, transaction_type_cd from transaction where request_id = {} order by event_id desc".format(fake_request.requestId))
    (value, transaction_type_cd) = cursor.fetchone()

    assert eid == value
    assert transaction_type_cd == 'CORRT'


@integration_oracle_namesdb
def test_update_nro_request_state_to_draft(app):
    con = nro.connection
    cursor = con.cursor()

    eid = _get_event_id(cursor)

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')

    fake_request = FakeRequest()
    fake_request.requestId = 884047
    fake_request.stateCd = 'DRAFT'
    fake_request.activeUser = user

    _update_nro_request_state(cursor, fake_request, eid, {'is_changed__request_state': True})

    cursor.execute("select state_type_cd from request_state where request_id = {} and start_event_id = {}"
                   .format(fake_request.requestId, eid))
    (state_type_cd,) = cursor.fetchone()

    assert state_type_cd == 'D'


@integration_oracle_namesdb
def test_update_nro_request_state_to_approved(app):
    """
    Code should not allow us to set state to anything except Draft
    """
    con = nro.connection
    cursor = con.cursor()

    eid = _get_event_id(cursor)

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')

    fake_request = FakeRequest()
    fake_request.requestId = 884047
    fake_request.stateCd = 'APPROVED'
    fake_request.activeUser = user

    _update_nro_request_state(cursor, fake_request, eid, {'is_changed__request_state': True})

    cursor.execute("select state_type_cd from request_state where request_id = {} and start_event_id = {}"
                   .format(fake_request.requestId, eid))
    resultset = cursor.fetchone()

    assert resultset is None


@integration_oracle_namesdb
def test_update_nro_change_and_remove_name_choices(app):
    """
    Ensure name can be changed, or removed.
    """
    con = nro.connection
    cursor = con.cursor()

    eid = _get_event_id(cursor)

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')

    fake_request = FakeRequest()
    fake_name1 = FakeName()
    fake_name2 = FakeName()
    fake_name3 = FakeName()

    fake_name1.choice = 1
    fake_name2.choice = 2
    fake_name3.choice = 3
    # Update the second name only, and remove the third:
    fake_name1.name = "Fake name"
    fake_name2.name = 'Second fake name'
    fake_name3.name = ''
    names = NamesList()
    names.addNames([fake_name1, fake_name2, fake_name3])
    fake_request.names = names

    fake_request.requestId = 142729
    fake_request.stateCd = 'INPROGRESS'
    fake_request.activeUser = user

    change_flags = {
        'is_changed__name1': False,
        'is_changed__name2': True,
        'is_changed__name3': True,
    }

    # Fail if our test data is not still valid:
    cursor.execute("""
        select ni.name
        from name n, name_instance ni
        where  ni.name_id = n.name_id 
        and n.request_id = {} 
        and ni.end_event_id is null """
                   .format(fake_request.requestId))
    result = list(cursor.fetchall())
    assert len(result) == 3
    assert (result[1][0] != 'Second fake name')

    _update_nro_names(cursor, fake_request, eid, change_flags)

    cursor.execute("""
        select ni.name
        from name n, name_instance ni
        where  ni.name_id = n.name_id 
        and n.request_id = {} 
        and ni.end_event_id is null """
                   .format(fake_request.requestId))
    result = list(cursor.fetchall())

    assert result
    assert len(result) == 2
    assert result[0][0] != 'Fake name'
    assert result[1][0] == 'Second fake name'


@integration_oracle_namesdb
def test_update_nro_add_new_name_choice(app):
    """
    Ensure name can be changed, or removed.
    """
    con = nro.connection
    cursor = con.cursor()

    eid = _get_event_id(cursor)

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')

    fake_request = FakeRequest()
    fake_name1 = FakeName()
    fake_name2 = FakeName()

    fake_name1.choice = 1
    fake_name2.choice = 2
    # Add a second name choice:
    fake_name1.name = "Fake name"
    fake_name2.name = 'Second fake name'
    names = NamesList()
    names.addNames([fake_name1, fake_name2])
    fake_request.names = names

    fake_request.requestId = 884047
    fake_request.stateCd = 'INPROGRESS'
    fake_request.activeUser = user

    change_flags = {
        'is_changed__name1': False,
        'is_changed__name2': True,
        'is_changed__name3': False,
    }

    # Fail if our test data is not still valid:
    cursor.execute("""
        select ni.name
        from name n, name_instance ni
        where  ni.name_id = n.name_id 
        and n.request_id = {} 
        and ni.end_event_id is null """
                   .format(fake_request.requestId))
    result = list(cursor.fetchall())
    assert len(result) == 1

    _update_nro_names(cursor, fake_request, eid, change_flags)

    cursor.execute("""
        select ni.name
        from name n, name_instance ni
        where  ni.name_id = n.name_id 
        and n.request_id = {} 
        and ni.end_event_id is null """
                   .format(fake_request.requestId))
    result = list(cursor.fetchall())

    assert result
    assert len(result) == 2
    assert result[0][0] != 'Fake name'
