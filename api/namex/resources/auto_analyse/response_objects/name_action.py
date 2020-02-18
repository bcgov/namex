from . import Serializable

from enum import Enum


class NameActions(Enum):
    STRIKE = 'strike'
    HIGHLIGHT = 'highlight'
    ADD_WORD_BRACKETS = 'add_word_brackets'

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values


class WordPositions(Enum):
    START = 'start'
    END = 'end'

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values


class NameAction(Serializable):
    def __init__(self, **kwargs):
        if not kwargs.get('type').value in NameActions.list():
            raise TypeError('Invalid NameAction, please supply a valid NameAction type')

        if kwargs.get('position') and kwargs['position'].value not in WordPositions.list():
            raise TypeError('Invalid word position, please supply a valid WordPositions type')

        if kwargs.get('index') and (isinstance(kwargs['index'], int) is False or kwargs['index'] < 0):
            raise TypeError('Invalid index, index must be a positive integer or zero')

        # TODO: Make sure index is valid! Add validation.

        self.type = kwargs['type'].value
        self.index = kwargs['index'] if kwargs.get('index') and isinstance(kwargs['index'], int) else None  # Ensure positive index
        self.word = kwargs['word'] if kwargs.get('word') else None
        self.position = kwargs['position'].value if kwargs.get('position') else None  # [start | end] (is there another?)
        self.message = kwargs['message'] if kwargs.get('message') else None  # <string> | None
