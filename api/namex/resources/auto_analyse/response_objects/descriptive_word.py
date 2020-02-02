from . import Serializable


class DescriptiveWord(Serializable):
    def __init__(self, **kwargs):
        self.category = kwargs['category'] if kwargs.get('category') else ''  # Required! <string>
        self.wordList = kwargs['wordList'] if kwargs.get('wordList') else None  # <string>[] | None
