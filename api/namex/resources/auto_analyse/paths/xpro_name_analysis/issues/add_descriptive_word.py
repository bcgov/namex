# Import DTOs
from ....response_objects import NameAnalysisIssue

from namex.resources.auto_analyse.issues import AddDescriptiveWordIssue


class XproAddDescriptiveWordIssue(AddDescriptiveWordIssue):
    def create_issue(self):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="",
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            # Set the show_examination_button to TRUE for all Xpro issues
            show_examination_button=True,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        return issue
