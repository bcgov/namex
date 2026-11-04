from string import Template

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..response_objects import NameAction, NameActions, NameAnalysisIssue, WordPositions

# Import DTOs
from .abstract import AnalysisResponseIssue


class AddDescriptiveWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD
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
        # list_name = self._lc_list_items(self.analysis_response.name_tokens)  # procedure_result.values['list_name']
        list_dist = self._lc_list_items(procedure_result.values['list_dist'])

        issue = self.create_issue()
        issue.line1 = 'Requires a word that describes the nature of your business.'

        last_dist_word = list_dist[-1] if list_dist.__len__() > 0 else None
        # TODO: Why was this like this before?
        # dist_word_idx = list_name.index(last_dist_word) # if list_dist.__len__() > 0 else 0
        # dist_word_idx = list_name.index(last_dist_word) if list_dist.__len__() > 0 else 0
        # offset_idx, word_idx, word_idx_offset, composite_token_offset = self.adjust_word_index(
        #     self.analysis_response.name_as_submitted,
        #     self.analysis_response.name_original_tokens,
        #     self.analysis_response.name_tokens,
        #     dist_word_idx
        # )

        issue.name_actions = [
            NameAction(
                type=NameActions.BRACKETS,
                position=WordPositions.END,
                message='Add a Descriptive Word Here',
                word=last_dist_word,
                index=0,
            )
        ]

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue
