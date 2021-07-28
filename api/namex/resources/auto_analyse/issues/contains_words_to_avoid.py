from string import Template

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

# Import DTOs
from .abstract import AnalysisResponseIssue
from ..response_objects import NameAnalysisIssue
from ..response_objects import NameAction, NameActions


class ContainsWordsToAvoidIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.WORDS_TO_AVOID
    status_text = "Further Action Required"
    issue = None

    def create_issue(self):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="",
            line2="",
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        return issue

    def configure_issue(self, procedure_result):
        # list_name = self._lc_list_items(self.analysis_response.name_tokens)  # procedure_result.values['list_name']
        list_avoid = self._lc_list_items(procedure_result.values['list_avoid'])
        list_avoid_compound = self._lc_list_items(procedure_result.values['list_avoid_compound'])

        issue = self.create_issue()
        issue.line1 = "The word(s) " + self._join_list_words(list_avoid_compound) + " cannot be used."

        # TODO: If there's a duplicate of a word to avoid, just grabbing the index might not do!
        issue.name_actions = []
        for word in list_avoid:
            # offset_idx, word_idx, word_idx_offset, composite_token_offset = self.adjust_word_index(
            #     self.analysis_response.name_as_submitted,
            #     self.analysis_response.name_original_tokens,
            #     self.analysis_response.name_tokens,
            #     list_name.index(word)
            # )

            issue.name_actions.append(
                NameAction(
                    type=NameActions.STRIKE,
                    word=word,
                    index=0
                )
            )

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue
