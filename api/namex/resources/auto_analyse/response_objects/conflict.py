from . import Serializable


class Conflict(Serializable):
    def __init__(self, **kwargs):
        self.name = kwargs['name'] or ''  # Required! <string>
        self.date = kwargs['date'] or None  # <date> | None