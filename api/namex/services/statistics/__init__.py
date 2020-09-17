from namex.constants import AbstractEnum

response_keys = ['auto_approved_count', 'priority_wait_time', 'regular_wait_time']


class UnitTime(AbstractEnum):
    DAY = 'days'
    HR = 'hours'
    MIN = 'minutes'
