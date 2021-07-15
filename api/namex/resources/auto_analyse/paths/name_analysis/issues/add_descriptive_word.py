"""Descriptive issue classes."""
from namex.resources.auto_analyse.issues import AddDescriptiveWordIssue

from ....response_objects import NameAnalysisIssue


class BcAddDescriptiveWordIssue(AddDescriptiveWordIssue):
    """BC descriptive word issue."""

    pass


class XproAddDescriptiveWordIssue(AddDescriptiveWordIssue):
    """XPRO descriptive word issue."""

    def create_issue(self):
        """Create descriptive word issue."""
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
