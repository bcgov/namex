import datetime

from namex.constants import EventAction, EventUserId

API_BASE_URI = '/api/v1/statistics/'
ENDPOINT_PATH = API_BASE_URI + ''

num_records = 0


def save_names_queue(queue_number_records, priority=False):
    from namex.models import Request as RequestDAO, State

    num = 0
    global num_records

    while queue_number_records > num:
        nr_num_label = 'NR '
        num_records += 1
        num += 1
        nr_num = nr_num_label + str(num_records)

        nr = RequestDAO()
        nr.nrNum = nr_num
        nr.stateCd = State.DRAFT
        nr.priorityCd = 'Y' if priority else 'N'
        nr._source = 'NAMEREQUEST'
        nr.save_to_db()


def save_auto_approved_names(approved_number_records):
    from namex.models import Event as EventDAO, Request as RequestDAO, User as UserDAO, State

    num = 0
    global num_records

    username = 'name_request_service_account'
    usr = UserDAO(username, '', '', '', '', '', '')
    usr.id = 86

    usr.save_to_db()
    while approved_number_records > num:
        nr_num_label = 'NR 00'
        num_records += 1
        num += 1
        nr_num = nr_num_label + str(num_records)

        nr = RequestDAO()
        nr.nrNum = nr_num
        nr.stateCd = State.APPROVED
        nr._source = 'NAMEREQUEST'

        event = EventDAO()
        event.action = EventAction.PUT.value
        event.userId = EventUserId.SERVICE_ACCOUNT.value
        event.stateCd = State.APPROVED
        event.eventDate = datetime.date.today()
        nr.events = [event]
        nr.save_to_db()


def save_approved_names_by_examiner(approved_number_records):
    from namex.models import Request as RequestDAO, State, Event as EventDAO

    num = 0
    global num_records

    while approved_number_records > num:
        num_records += 1
        num += 1
        nr_num_label = 'NR 00'
        nr_num = nr_num_label + str(num_records)

        nr = RequestDAO()
        nr.nrNum = nr_num
        nr.stateCd = State.APPROVED
        nr.submittedDate = datetime.date.today() - datetime.timedelta(days=2)
        nr._source = 'NAMEREQUEST'

        event = EventDAO()
        event.action = EventAction.PATCH.value
        event.stateCd = State.APPROVED
        event.eventDate = datetime.date.today() - datetime.timedelta(days=1)
        nr.events = [event]
        nr.save_to_db()


def save_name(submitted_date, nr_num, priority=False):
    from namex.models import Request as RequestDAO, State

    num = 0
    global num_records

    nr_num_label = 'NR '
    nr_num = nr_num_label + str(nr_num)

    nr = RequestDAO()
    nr.nrNum = nr_num
    nr.stateCd = State.DRAFT
    nr.priorityCd = 'Y' if priority else 'N'
    nr._source = 'NAMEREQUEST'
    nr.submittedDate = submitted_date
    nr.save_to_db()
