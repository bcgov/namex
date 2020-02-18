from . import Serializable

'''
@:deprecated
'''


class DescriptiveWord(Serializable):
    def __init__(self, **kwargs):
        self.category = kwargs['category'] if kwargs.get('category') else ''  # Required! <string>
        self.word_list = kwargs['word_list'] if kwargs.get('word_list') else None  # <string>[] | None
