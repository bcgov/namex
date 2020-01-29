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

    def __init__(self, analysis_result):
        pass

    @staticmethod
    def create_new_issue():
        issue = NameAnalysisIssue(
            consentingBody=ConsentingBody(
                name='Test Body',
                email='test@example.com'
            ),
            designations=None,
            descriptiveWords=None,
            issueType=None,
            word=None,
            wordIndex=None,
            showExaminationButton=None,
            conflicts=None,
            options=None,
            nameActions=None
        )

        issue.nameActions = []

        name_action = NameAction(
            type='Test',
            position='start',
            message='Ipsum lorem dolor'
        )

        issue.nameActions.append(name_action)

        return issue

    # TODO: This is an ABSTRACT method and MUST be implemented in extending classes...
    def create_issue(self):
        pass

    @staticmethod
    def prepare_payload(issue):
        payload = NameAnalysisResponse(
            status='Test',
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