from .abstract import Serializable

"""
@:deprecated
"""


class DescriptiveWord(Serializable):
    def __init__(self, **kwargs):
        self.category = kwargs.get('category', '')  # Required! <string>
        self.word_list = kwargs.get('word_list', None)  # <string>[] | None
