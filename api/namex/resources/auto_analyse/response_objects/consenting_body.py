from . import Serializable


class ConsentingBody(Serializable):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')  # Required! <string>
        self.email = kwargs.get('email', None)  # <string> | None
