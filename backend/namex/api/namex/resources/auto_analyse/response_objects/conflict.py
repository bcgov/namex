from .abstract import Serializable


class Conflict(Serializable):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.date = kwargs.get('date', None)
        self.start_date = kwargs.get('start_date', None)
        self.id = kwargs.get('id', '')
        self.source = kwargs.get('source', '')
