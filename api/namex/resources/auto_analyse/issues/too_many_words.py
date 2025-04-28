from string import Template

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..response_objects import NameAnalysisIssue

# Import DTOs
from .abstract import AnalysisResponseIssue


class TooManyWordsIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.TOO_MANY_WORDS
    status_text = 'Further Review Required'
    issue = None

    def create_issue(self):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1='',
            line2='',
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=True,
            conflicts=None,
            setup=None,
            name_actions=None,
        )

        return issue

    def configure_issue(self, procedure_result):
        issue = self.create_issue()
        issue.line1 = 'This name cannot be analyzed here and must be sent to staff for review.'

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue
