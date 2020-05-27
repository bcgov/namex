from .abstract import Serializable


class Conflict(Serializable):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.date = kwargs.get('date', None)
