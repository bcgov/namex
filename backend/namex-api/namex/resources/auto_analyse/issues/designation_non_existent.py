from string import Template

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..response_objects import NameAnalysisIssue

# Import DTOs
from .abstract import AnalysisResponseIssue


class DesignationNonExistentIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.DESIGNATION_NON_EXISTENT
    status_text = 'Further Action Required'
    issue = None

    def create_issue(self):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1='',
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[],
        )

        return issue

    def configure_issue(self, procedure_result):
        list_name = self._lc_list_items(self.analysis_response.name_tokens)  # procedure_result.values['list_name']
        correct_designations = self._lc_list_items(procedure_result.values['correct_designations'])

        issue = self.create_issue()
        issue.line1 = 'A designation is required.'
        issue.designations = correct_designations

        # Setup boxes
        issue.setup = self.setup_config
        # Replace template strings in setup boxes
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(
                        setup_item,
                        prop,
                        setup_item.__dict__[prop].safe_substitute(
                            {
                                'list_name': self._join_list_words(list_name),
                                'correct_designations': self._join_list_words(correct_designations),
                            }
                        ),
                    )

        return issue
