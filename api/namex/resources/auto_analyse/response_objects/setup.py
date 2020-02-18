from . import Serializable


class Setup(Serializable):
    def __init__(self, **kwargs):
        # TODO: Type the list of buttons!
        self.button = kwargs['button'] if kwargs.get('button') else ''
        self.checkbox = kwargs['checkbox'] if kwargs.get('checkbox') else ''
        # TODO: Can we get Scott to change 'header' to header?
        self.header = kwargs['header'] if kwargs.get('header') else ''
        self.line1 = kwargs['line1'] if kwargs.get('line1') else ''
        self.line2 = kwargs['line2'] if kwargs.get('line2') else ''
