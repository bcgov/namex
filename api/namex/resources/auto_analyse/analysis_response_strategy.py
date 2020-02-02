# Import DTOs
from .response_objects.name_analysis_issue import NameAnalysisIssue
from .response_objects.name_analysis_response import NameAnalysisResponse
from .response_objects.name_action import NameAction
from .response_objects.consenting_body import ConsentingBody
from .response_objects.conflict import Conflict
from .response_objects.descriptive_word import DescriptiveWord


class AnalysisResponseStrategy:
    strategy_name = 'Analysis Response Strategy'
    issue_type = 'Issue'
    status_text = ''
    issue = None

    def __init__(self, analysis_result):
        pass

    @classmethod
    def create_issue(cls):
        return cls.issue

    @classmethod
    def prepare_payload(cls, issue):
        payload = NameAnalysisResponse(
            status=cls.status_text,
            issues=[issue]
        )
        return payload

    '''
    This is invoked by consumers of this class
    '''
    def build_response(self):
        issue = self.create_issue()
        response = self.prepare_payload(issue)
        return response
