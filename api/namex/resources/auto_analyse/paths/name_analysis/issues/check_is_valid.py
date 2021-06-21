"""Validation issue classes."""
from namex.resources.auto_analyse.issues import CheckIsValidIssue

from ....response_objects import NameAnalysisIssue


class BcCheckIsValidIssue(CheckIsValidIssue):
    """BC validation issue."""

    pass


class XproCheckIsValidIssue(CheckIsValidIssue):
    """XPRO validation issue."""

    def create_issue(self):
        """Create XPRO validation issue."""
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1=None,
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=None,
            # Set the show_examination_button to TRUE for all Xpro issues
            show_examination_button=None,
            conflicts=None,
            setup=None,
            name_actions=None
        )

        return issue
