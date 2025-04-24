from string import Template

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..response_objects import ConsentingBody, NameAction, NameActions, NameAnalysisIssue

# Import DTOs
from .abstract import AnalysisResponseIssue


class NameRequiresConsentIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.NAME_REQUIRES_CONSENT
    status_text = 'Further Action Required'
    issue = None

    def create_issue(self):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1='',
            line2='',
            consenting_body=ConsentingBody(name='', email=''),
            designations=None,
            show_reserve_button=None,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[],
        )

        return issue

    def configure_issue(self, procedure_result):
        list_name = self.analysis_response.name_tokens  # procedure_result.values['list_name']
        list_consent = self._lc_list_items(procedure_result.values['list_consent'])
        list_consent_original = self._lc_list_items(procedure_result.values['list_consent_original'])

        issue = self.create_issue()
        issue.line1 = (
            'The word(s) ' + self._join_list_words(list_consent_original) + ' are restricted and may require consent.'
        )

        issue.name_actions = []
        for word in list_consent:
            offset_idx, word_idx, word_idx_offset, composite_token_offset = self.adjust_word_index(
                self.analysis_response.name_as_submitted,
                self.analysis_response.name_original_tokens,
                self.analysis_response.name_tokens,
                list_name.index(word.lower()),
            )

            issue.name_actions.append(NameAction(type=NameActions.HIGHLIGHT, word=word, index=offset_idx))

        # TODO: Where does this info come from?
        issue.consenting_body = ConsentingBody(name='Example Conflict Company Ltd.', email='email@example.com')

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue
