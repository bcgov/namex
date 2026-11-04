"""Designation non existent issue classes."""

from namex.resources.auto_analyse.issues import DesignationNonExistentIssue

from ....response_objects import NameAnalysisIssue


class BcDesignationNonExistentIssue(DesignationNonExistentIssue):
    """BC designation non existent issue."""

    pass


class XproDesignationNonExistentIssue(DesignationNonExistentIssue):
    """XPRO designation non existent issue."""

    def create_issue(self):
        """Create XPRO designation non existent issue."""
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
            name_actions=[],
        )

        return issue
