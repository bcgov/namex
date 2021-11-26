from datetime import datetime, timedelta
from pytz import timezone

from namex.models import db
from namex.models.nr_number import NRNumber
from namex.models.user import User

from namex.utils.logging import setup_logging

from namex.services.name_request.utils import get_mapped_request_type, get_mapped_entity_and_action_code
from namex.services.name_request.exceptions import GetUserIdError, GenerateNRKeysError, MapRequestTypeError

setup_logging()  # Important to do this first


class AbstractNameRequestMixin(object):
    _request_data = None
    _nr_id = None
    _nr_num = None
    _next_state_code = None
    _state_actions = None

    @property
    def user_id(self):
        try:
            user = User.find_by_username('name_request_service_account')
            if not user:
                raise GetUserIdError()
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
        action_cd = self.request_data.get('request_action_cd', None)
        if action_cd:
            return action_cd

    @property
    def request_entity(self):
        entity_type_cd = self.request_data.get('entity_type_cd', None)
        if entity_type_cd:
            return entity_type_cd

    @property
    def request_type(self):
        request_type_cd = self.request_data.get('requestTypeCd', None)
        if request_type_cd:
            return request_type_cd

    @property
    def request_names(self):
        return self.request_data.get('names', [])

    @property
    def current_state_actions(self):
        return self._state_actions

    @current_state_actions.setter
    def current_state_actions(self, data):
        self._state_actions = data

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
    def get_mapped_request_type(cls, entity_type, request_action):
        return get_mapped_request_type(entity_type, request_action)

    @classmethod
    def get_mapped_entity_and_action_code(cls, request_type):
        return get_mapped_entity_and_action_code(request_type)

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
            r = NRNumber()
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
        """Create an expiry date in given days and at 11:59pm.

        In order to add days without having 1 hour difference between the two dates in summer time changes 
        we need to calculate the new date using naive dates (not aware of timezone) and after that we can add the timezone.
        """
        utc_tz = timezone('UTC')

        # converts the input date to UTC and removes tzinfo:
        naive_date_utc = start.astimezone(utc_tz).replace(tzinfo=None)
        # calculates the new day in UTC
        future_date_utc = (naive_date_utc + timedelta(days=expires_in_days))
        # make it localized back to UTC and convert it to PST
        expiry_date_pst = utc_tz.localize(future_date_utc).astimezone(tz)
        # set the time to 11:59pm in PST
        expiry_date_pst_with_adjusted_time = expiry_date_pst.replace(hour=expiry_hour, minute=expiry_min, second=0, microsecond=0)

        return expiry_date_pst_with_adjusted_time

    def generate_nr_keys(self):
        try:
            # temp Nr # until one is generated in oracle
            self.nr_num = self.generate_nr()
            self.nr_id = self.get_request_sequence()
        except Exception as err:
            raise GenerateNRKeysError(err)

        return self.nr_num, self.nr_id
