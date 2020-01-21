# Import DTOs
from namex.resources.auto_analyse import \
    ConsentingBody, \
    NameAction, \
    DescriptiveWord, \
    Conflict, \
    NameAnalysisIssue, \
    NameAnalysisResponse


class AnalysisResponseStrategy:
    strategy_name = 'Analysis Response Strategy'
    issue_type = 'Issue'
    status_text = ''

    def __init__(self):
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

    def create_issue(self):
        # TODO: This MUST be implemented...
        pass

    @staticmethod
    def prepare_payload(issue):
        payload = NameAnalysisResponse(
            status='Test',
            issues=[issue]
        )
        return payload

    def build_response(self):
        issue = self.create_issue()
        response = self.prepare_payload(issue)
        return response


class ValidNameResponseStrategy(AnalysisResponseStrategy):
    issue_type = None
    status_text = 'Approved'

    def create_issue(self):
        issue = super(ValidNameResponseStrategy, self).create_new_issue()
        return issue


class AddDistinctiveWordResponseStrategy(AnalysisResponseStrategy):
    issue_type = 'add_distinctive'
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(AddDistinctiveWordResponseStrategy, self).create_new_issue()
        return issue


class AddDescriptiveWordResponseStrategy(AnalysisResponseStrategy):
    issue_type = 'add_descriptive'
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(AddDescriptiveWordResponseStrategy, self).create_new_issue()
        return issue


class ContainsWordsToAvoidResponseStrategy(AnalysisResponseStrategy):
    issue_type = 'word_to_avoid'
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(ContainsWordsToAvoidResponseStrategy, self).create_new_issue()
        return issue


class DesignationMismatchResponseStrategy(AnalysisResponseStrategy):
    issue_type = 'designation_mismatch'
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(DesignationMismatchResponseStrategy, self).create_new_issue()
        return issue


class TooManyWordsResponseStrategy(AnalysisResponseStrategy):
    issue_type = 'excess_words'
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(TooManyWordsResponseStrategy, self).create_new_issue()
        return issue


class NameRequiresConsentResponseStrategy(AnalysisResponseStrategy):
    issue_type = 'consent_required'
    status_text = 'May be Approved With Consent'

    def create_issue(self):
        issue = super(NameRequiresConsentResponseStrategy, self).create_new_issue()
        return issue


class ContainsUnclassifiableWordResponseStrategy(AnalysisResponseStrategy):
    issue_type = 'unclassified_word'
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(ContainsUnclassifiableWordResponseStrategy, self).create_new_issue()
        return issue


class CorporateNameConflictResponseStrategy(AnalysisResponseStrategy):
    issue_type = 'corp_conflict'
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(CorporateNameConflictResponseStrategy, self).create_new_issue()
        return issue

