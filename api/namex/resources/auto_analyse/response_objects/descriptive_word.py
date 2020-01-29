from . import Serializable


class DescriptiveWord(Serializable):
    def __init__(self, **kwargs):
        self.category = kwargs['category'] or ''  # Required! <string>
        self.wordList = kwargs['wordList'] or None  # <string>[] | None