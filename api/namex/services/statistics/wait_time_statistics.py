import math

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
    def get_statistics(cls):
        response_values = [cls.get_approved_names_counter(),
                           cls.get_waiting_time_priority_queue(unit=UnitTime.HR.value),
                           cls.get_waiting_time_regular_queue(unit=UnitTime.DAY.value)]

        response = query_result_to_dict(response_keys, response_values)

        return response
