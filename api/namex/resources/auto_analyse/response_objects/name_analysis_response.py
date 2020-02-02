from . import Serializable


class NameAnalysisResponse(Serializable):
    def __init__(self, **kwargs):
        self.status = kwargs['status'] or ''
        self.issues = kwargs['issues'] or []
