from . import Serializable


class NameAnalysisResponse(Serializable):
    def __init__(self, **kwargs):
        # TODO: Can we use 'heading' instead, technically in HTML they're called headings, not headers anyway, and headers in terms of an API should mean HTTP headers?
        self.header = kwargs['header'] or ''
        self.status = kwargs['status'] or ''
        self.issues = kwargs['issues'] or []
