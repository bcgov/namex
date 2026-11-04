"""Contains words to avoid issue classes."""

from namex.resources.auto_analyse.issues import ContainsWordsToAvoidIssue

from ....response_objects import NameAnalysisIssue


class BcContainsWordsToAvoidIssue(ContainsWordsToAvoidIssue):
    """BC contains words to avoid."""

    pass


class XproContainsWordsToAvoidIssue(ContainsWordsToAvoidIssue):
    """XPRO contains words to avoid."""

    def create_issue(self):
        """Create XPRO contains words to avoid issue."""
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1='',
            line2='',
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            # Set the show_examination_button to TRUE for all Xpro issues
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[],
        )

        return issue
