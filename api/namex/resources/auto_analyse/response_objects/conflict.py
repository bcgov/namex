from . import Serializable


class Conflict(Serializable):
    def __init__(self, **kwargs):
        self.name = kwargs['name'] if kwargs.get('name') else ''  # Required! <string>
        self.date = kwargs['date'] if kwargs.get('date') else None  # <date> | None
