from . import Serializable


class Setup(Serializable):
    def __init__(self, **kwargs):
        self.button = kwargs.get('button', '')
        self.checkbox = kwargs.get('checkbox', '')
        # TODO: Can we get Scott to change 'header' to header?
        self.type = kwargs.get('type', '')
        self.header = kwargs.get('header', '')
        self.line1 = kwargs.get('line1', '')
        self.line2 = kwargs.get('line2', '')
        self.label = kwargs.get('label', '')
