"""
Query criteria for the Synonym model.
"""


class SynonymQueryCriteria(object):
    def __init__(self, **kwargs):
        self.word = kwargs.get("word", None)  # Required! <string>
        self.fields = kwargs.get("fields", [])
        self.filters = kwargs.get("filters", [])

    """
    Used to validate criteria instances.
    """
    @staticmethod
    def is_valid_criteria(criteria):
        # TODO: Do we want to duck type this instead? We really only care about the shape...
        if not isinstance(criteria, SynonymQueryCriteria):
            raise Exception("Invalid criteria")
