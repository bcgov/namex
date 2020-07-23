from datetime import datetime, timedelta
from pytz import timezone

from namex.constants import request_type_mapping

from namex.models import db
from namex.models.nr_number import NRNumber
from namex.models.user import User

from namex.services.name_request.utils import handle_exception

from namex.utils.logging import setup_logging

from namex.services.name_request.exceptions import GetUserIdError

setup_logging()  # Important to do this first


class AbstractNameRequestMixin(object):
    @property
    def user_id(self):
        try:
            user = User.find_by_username('name_request_service_account')
        except Exception as err:
            raise GetUserIdError(err)

        return user.id

    @property
    def user(self):
        try:
            user = User.find_by_username('name_request_service_account')
        except Exception as err:
            raise GetUserIdError(err)

        return user

    @property
    def request_data(self):
        return self._request_data

    @request_data.setter
    def request_data(self, data):
        self._request_data = data

    @property
    def request_state_code(self):
        return self.request_data.get('stateCd', None)

    @property
    def request_action(self):
        return self.request_data.get('request_action', None)

    @property
    def request_entity(self):
        return self.request_data.get('entity_type', None)

    @property
    def request_names(self):
        return self.request_data.get('names', None)

    @property
    def nr_num(self):
        return self._nr_num

    @nr_num.setter
    def nr_num(self, val):
        self._nr_num = val

    @property
    def nr_id(self):
        return self._nr_id

    @nr_id.setter
    def nr_id(self, val):
        self._nr_id = val

    @property
    def next_state_code(self):
        return self._next_state_code

    @next_state_code.setter
    def next_state_code(self, val):
        self._next_state_code = val

    @classmethod
    def set_request_type(cls, entity_type, request_action):
        for item in request_type_mapping:
            if item[1] == entity_type and item[2] == request_action:
                output = item
                break
        request_type = list(output)
        return request_type[0]

    @classmethod
    def get_request_sequence(cls):
        seq = db.Sequence('requests_id_seq')
        nr_id = db.engine.execute(seq)
        return nr_id

    @classmethod
    def get_applicant_sequence(cls):
        seq = db.Sequence('applicants_party_id_seq')
        party_id = db.engine.execute(seq)
        return party_id

    @classmethod
    def get_name_sequence(cls):
        seq = db.Sequence('names_id_seq')
        name_id = db.engine.execute(seq)
        return name_id

    @classmethod
    def generate_nr(cls):
        r = db.session.query(NRNumber).first()
        if r is None:
            # Set starting nr number
            last_nr = 'NR L000000'
        else:
            last_nr = r.nrNum
            # TODO: Add a check wheN the number has reached 999999
            # and you need to roll over to the next letter in the alphabet and reset the number to 000000

        nr_num = NRNumber.get_next_nr_num(last_nr)
        r.nrNum = nr_num
        r.save_to_db()
        # TODO: Add a check that it updated
        return nr_num

    @classmethod
    def create_expiry_date(cls, start: datetime, expires_in_days: int, expiry_hour: int = 23, expiry_min: int = 59,
                           tz: timezone = timezone('US/Pacific')) -> datetime:

        date = (start.astimezone(tz) + timedelta(days=expires_in_days)) \
            .replace(hour=expiry_hour, minute=expiry_min, second=0, microsecond=0)

        return date

    def generate_nr_keys(self):
        try:
            # temp Nr # until one is generated in oracle
            self.nr_num = self.generate_nr()
            self.nr_id = self.get_request_sequence()
        except Exception as err:
            return handle_exception(err, 'Error getting nr number.', 500)

        return self.nr_num, self.nr_id
