from . import Serializable


class NameAction(Serializable):
    def __init__(self, **kwargs):
        self.type = kwargs['type'] or ''  # Required! [strike | add_word_brackets | highlight]
        self.position = kwargs['position'] or None  # [start | end] (is there another?)
        self.message = kwargs['message'] or None  # <string> | None