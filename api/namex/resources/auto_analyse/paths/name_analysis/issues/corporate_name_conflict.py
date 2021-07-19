"""Corporate Name Conflict issue classes."""
from namex.resources.auto_analyse.issues import CorporateNameConflictIssue

from ....response_objects import NameAnalysisIssue


class BcCorporateNameConflictIssue(CorporateNameConflictIssue):
    """BC corporate name conflict issue."""

    pass


class XproCorporateNameConflictIssue(CorporateNameConflictIssue):
    """XPRO corporate name conflict issue."""

    def create_issue(self):
        """Create XPRO corporate name conflict issue."""
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1='',
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=None,
            # Set the show_examination_button to TRUE for all Xpro issues
            show_examination_button=False,
            conflicts=[],
            setup=None,
            name_actions=[]
        )

        return issue
