from namex.services.name_request.auto_analyse import AnalysisIssueCodes

# Import DTOs
from namex.resources.auto_analyse.issues import DesignationMismatchIssue


class DesignationRemovalIssue(DesignationMismatchIssue):
    issue_type = AnalysisIssueCodes.DESIGNATION_REMOVAL
    status_text = 'Further Action Required'
    issue = None
