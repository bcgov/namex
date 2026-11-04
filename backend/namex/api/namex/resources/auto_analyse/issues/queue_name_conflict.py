from namex.resources.auto_analyse.issues import CorporateNameConflictIssue
from namex.services.name_request.auto_analyse import AnalysisIssueCodes


class QueueNameConflictIssue(CorporateNameConflictIssue):
    issue_type = AnalysisIssueCodes.QUEUE_CONFLICT
    status_text = 'Further Action Required'
    issue = None
