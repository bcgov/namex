from enum import Enum

from .abstract import Serializable


class NameActions(Enum):
    STRIKE = 'strike'
    HIGHLIGHT = 'highlight'
    BRACKETS = 'brackets'
    SPELLING = 'spelling'

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
        # Required!
        if kwargs.get('type').value not in NameActions.list():
            raise TypeError('Invalid NameAction, please supply a valid NameAction type')

        if kwargs.get('position') and kwargs.get('position').value not in WordPositions.list():
            raise TypeError('Invalid word position, please supply a valid WordPositions type')

        if kwargs.get('index') and (isinstance(kwargs.get('index'), int) is False or kwargs.get('index', 0) < 0):
            raise TypeError('Invalid index, index must be a positive integer or zero')

        if kwargs.get('endIndex') and (
            isinstance(kwargs.get('endIndex'), int) is False or kwargs.get('endIndex', 0) < 0
        ):
            raise TypeError('Invalid endIndex, endIndex must be a positive integer or zero')

        self.type = kwargs.get('type').value if kwargs.get('type') else None
        self.position = kwargs.get('position').value if kwargs.get('position') else None
        self.message = kwargs.get('message', None)
        self.word = kwargs.get('word', None)
        self.index = kwargs.get('index', None)
        self.endIndex = kwargs.get('endIndex', None)
