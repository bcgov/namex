import math
from datetime import datetime, timedelta
import numpy as np

from flask import current_app
from namex.models import Request
from namex.models import Event
from namex.services.statistics import response_keys, UnitTime, get_utc_now
from namex.utils.sql_alchemy import query_result_to_dict
from namex.utils.api_resource import handle_exception

class WaitTimeStatsService:
    def __init__(self):
        pass

    @classmethod
    def get_approved_names_counter(cls):
        approved_names_counter = Event.get_approved_names_counter().approvedNamesCounter

        return approved_names_counter

    @classmethod
    def get_waiting_time_priority_queue(cls, unit):
        waiting_time = Request.get_waiting_time_priority_queue(unit)
        if waiting_time.examinationTime is None:
            return 0
        else:
            priority = math.ceil(waiting_time.examinationTime)

        return priority

    @classmethod
    def get_waiting_time_regular_queue(cls, unit):
        waiting_time = Request.get_waiting_time_regular_queue(unit)
        if waiting_time.examinationTime is None:
            return 0
        else:
            regular = math.ceil(waiting_time.examinationTime)

        return regular

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
        # For now not using this to improve performance
        # response_values = [cls.get_approved_names_counter(),
        #                    cls.get_waiting_time_priority_queue(unit=UnitTime.HR.value),
        #                    cls.get_waiting_time_regular_queue(unit=UnitTime.DAY.value)]

        oldest_draft = Request.get_oldest_draft()
        todays_date = get_utc_now().date()
        submitted_date = oldest_draft.submittedDate.date()

        # note that busday_count does not count the end date provided
        delta = np.busday_count(submitted_date, todays_date)
        delta = int(delta)
        # add one to waiting time to account for specific scenarios
        if np.is_busday(todays_date) or delta == 0:
            delta += 1

        response_values = [0,
                           0, #cls.get_waiting_time_priority_queue(unit=UnitTime.HR.value),
                           delta]

        response = query_result_to_dict(response_keys, response_values)

        return response
