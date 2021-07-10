"""Incorrect category issue classes."""
from namex.resources.auto_analyse.issues import IncorrectCategoryIssue

from ....response_objects import NameAnalysisIssue


class BcIncorrectCategoryIssue(IncorrectCategoryIssue):
    """BC incorrect category issue."""

    pass


class XproIncorrectCategoryIssue(IncorrectCategoryIssue):
    """XPRO incorrect category issue."""

    def create_issue(self):
        """Create XPRO incorrect category issue."""
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1='',
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            # Set the show_examination_button to TRUE for all Xpro issues
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        return issue
