import math
from datetime import datetime, timedelta

import numpy as np

from namex.models import Event, Request
from namex.services.statistics import get_utc_now, response_keys
from namex.utils.api_resource import handle_exception
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
                oldest_draft_date = datetime.now().astimezone()
            else:
                oldest_draft_date = oldest_draft.submittedDate

            # add one to waiting time to account for current day
            delta = datetime.now().astimezone() - oldest_draft_date + timedelta(days=1)
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
