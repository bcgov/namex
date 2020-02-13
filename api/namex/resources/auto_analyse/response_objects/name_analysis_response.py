from . import Serializable


class NameAnalysisResponse(Serializable):
    def __init__(self, **kwargs):
        self.header = kwargs['header'] or ''  # TODO: Can we use 'heading' instead?
        self.status = kwargs['status'] or ''
        self.issues = kwargs['issues'] or []
