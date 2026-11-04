from datetime import timedelta

from namex.models import Event, Request
from namex.services.statistics import response_keys
from namex.utils.api_resource import handle_exception
from namex.utils.pg8000_compat import pg8000_utcnow, safe_datetime_delta
from namex.utils.sql_alchemy import query_result_to_dict


class WaitTimeStatsService:
    def __init__(self):
        pass

    @classmethod
    def get_approved_names_counter(cls):
        approved_names_counter = Event.get_approved_names_counter().approvedNamesCounter

        return approved_names_counter

    @classmethod
    def get_waiting_time_dict(cls):
        try:
            if not (oldest_draft := Request.get_oldest_draft()):
                oldest_draft_date = pg8000_utcnow()
            else:
                oldest_draft_date = oldest_draft.submittedDate

            # add one to waiting time to account for current day
            delta = safe_datetime_delta(pg8000_utcnow(), oldest_draft_date) + timedelta(days=1)
            response_data = {'oldest_draft': oldest_draft_date.isoformat(), 'waiting_time': delta.days}
        except Exception as err:
            return handle_exception(err, repr(err), 500)

        return response_data

    @classmethod
    def get_statistics(cls):
        priority_wait_time = Request.get_waiting_time(priority_queue=True) or 0
        regular_wait_time = Request.get_waiting_time(priority_queue=False) or 0

        response_values = [0, priority_wait_time, regular_wait_time]
        response = query_result_to_dict(response_keys, response_values)
        return response
