"""Too Many Words Issue classes."""
from namex.resources.auto_analyse.issues import TooManyWordsIssue

from ....response_objects import NameAnalysisIssue


class BcTooManyWordsIssue(TooManyWordsIssue):
    """BC too many words issue."""

    pass


class XproTooManyWordsIssue(TooManyWordsIssue):
    """XPRO too many words issue."""

    def create_issue(self):
        """Create XPRO too many words issue."""
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1='',
            line2='',
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            # Set the show_examination_button to TRUE for all Xpro issues
            show_examination_button=True,
            conflicts=None,
            setup=None,
            name_actions=None
        )

        return issue
