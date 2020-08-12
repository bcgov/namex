from namex.models import Request
from namex.models import Event
from namex.services.statistics import response_keys
from namex.utils.service_utils import get_waiting_time
from namex.utils.sql_alchemy import query_result_to_dict


class WaitTimeStatsService:
    def __init__(self):
        pass

    @classmethod
    def get_approved_names_counter(cls):
        approved_names_counter = Event.get_approved_names_counter()

        return approved_names_counter

    @classmethod
    def get_queue_requests(cls, is_priority):
        queue_requests = Request.get_queue_requests(is_priority)

        return queue_requests

    @classmethod
    def get_statistics(cls):
        response_values = []

        approved_names = cls.get_approved_names_counter()
        response_values.append(approved_names)

        priority_queue_requests = cls.get_queue_requests(is_priority=True)
        regular_queue_requests = cls.get_queue_requests(is_priority=False)

        avg_examination = Event.get_avg_examination_time_secs()

        waiting_time_priority_queue = get_waiting_time(avg_examination, priority_queue_requests)
        response_values.append(waiting_time_priority_queue)

        waiting_time_regular_queue = get_waiting_time(avg_examination, regular_queue_requests)
        response_values.append(waiting_time_regular_queue)

        response = query_result_to_dict(response_values, response_keys)

        return response

    @classmethod
    def get_response(cls, approved_names, waiting_time_priority_queue, waiting_time_regular_queue):
        response = {'auto_approved_count': approved_names[0][0],
                    'priority_wait_time': waiting_time_priority_queue,
                    'regular_wait_time': waiting_time_regular_queue}
        return response
