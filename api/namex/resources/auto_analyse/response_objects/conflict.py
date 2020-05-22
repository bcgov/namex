from . import Serializable


class Conflict(Serializable):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.date = kwargs.get('date', None)
        self.corp_num = kwargs.get('corp_num', '')
        self.consumption_date = kwargs.get('consumption_date', None)
