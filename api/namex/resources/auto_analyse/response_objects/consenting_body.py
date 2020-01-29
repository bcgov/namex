from . import Serializable


class ConsentingBody(Serializable):
    def __init__(self, **kwargs):
        self.name = kwargs['name'] or ''  # Required! <string>
        self.email = kwargs['email'] or None  # <string> | None