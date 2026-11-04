"""Unclassifiable Word issue classes."""

from namex.resources.auto_analyse.issues import ContainsUnclassifiableWordIssue

from ....response_objects import NameAnalysisIssue


class BcContainsUnclassifiableWordIssue(ContainsUnclassifiableWordIssue):
    """BC unclassifiable word."""

    pass


class XproContainsUnclassifiableWordIssue(ContainsUnclassifiableWordIssue):
    """XPRO unclassifiable word."""

    def create_issue(self):
        """Create unclassifiable word issue."""
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
