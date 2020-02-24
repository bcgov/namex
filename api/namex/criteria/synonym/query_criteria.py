"""
Query criteria for the Synonym model.
"""


class SynonymQueryCriteria(object):
    def __init__(self, **kwargs):
        self.word = kwargs['word'] if kwargs.get('word') else None  # Required! <string>
        self.fields = kwargs['fields'] if kwargs.get('fields') else []
        self.filters = kwargs['filters'] if kwargs.get('filters') else []

    '''
    Used to validate criteria instances.
    '''
    @staticmethod
    def is_valid_criteria(criteria):
        # TODO: Do we want to duck type this instead? We really only care about the shape...
        if not isinstance(criteria, SynonymQueryCriteria):
            raise Exception('Invalid criteria')
