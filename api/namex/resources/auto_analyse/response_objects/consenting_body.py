from . import Serializable


class ConsentingBody(Serializable):
    def __init__(self, **kwargs):
        self.name = kwargs['name'] if kwargs.get('name') else ''  # Required! <string>
        self.email = kwargs['email'] if kwargs.get('email') else None  # <string> | None
