import math
from datetime import datetime

from namex.models import Request
from namex.models import Event
from namex.services.statistics import response_keys, UnitTime
from namex.utils.sql_alchemy import query_result_to_dict


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
            regular =  math.ceil(waiting_time.examinationTime)

        return regular

    @classmethod
    def get_waiting_time_dict(cls, submitted_date):

        oldest_draft = Request.get_oldest_draft()
        if oldest_draft is None:
            oldest_draft_date = datetime.now().astimezone()
        else:
            oldest_draft_date = oldest_draft.submittedDate

        # add one to waiting time to account for current day
        delta = submitted_date - oldest_draft_date
        response_data = {'oldest_draft': oldest_draft_date.isoformat(), 'waiting_time': delta.days}

        return response_data

    @classmethod
    def get_statistics(cls):
        # For now not using this to improve performance
        # response_values = [cls.get_approved_names_counter(),
        #                    cls.get_waiting_time_priority_queue(unit=UnitTime.HR.value),
        #                    cls.get_waiting_time_regular_queue(unit=UnitTime.DAY.value)]

        oldest_draft = Request.get_oldest_draft()
        todays_date = datetime.utcnow().date()
        submitted_date = oldest_draft.submittedDate.date()
        # add one to waiting time to account for current day
        delta = todays_date - submitted_date + 1

        response_values = [0,
                           0, #cls.get_waiting_time_priority_queue(unit=UnitTime.HR.value),
                           delta.days]

        response = query_result_to_dict(response_keys, response_values)

        return response
