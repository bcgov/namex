"""
Query criteria for the RequestWordConditionCriteria model.
"""


class RequestConditionCriteria(object):
    def __init__(self, **kwargs):
        self.nr_num = kwargs.get('nr_num', None)  # Required! <string>
        self.fields = kwargs.get('fields', [])
        self.filters = kwargs.get('filters', [])

    """
    Used to validate criteria instances.
    """

    @staticmethod
    def is_valid_criteria(criteria):
        # TODO: Do we want to duck type this instead? We really only care about the shape...
        if not isinstance(criteria, RequestConditionCriteria):
            raise Exception('Invalid criteria')
