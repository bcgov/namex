# Import DTOs
from ....response_objects import NameAnalysisIssue
from ....response_objects import ConsentingBody

from namex.resources.auto_analyse.issues import NameRequiresConsentIssue


class XproNameRequiresConsentIssue(NameRequiresConsentIssue):
    def create_issue(self):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="",
            line2="",
            consenting_body=ConsentingBody(
                name="",
                email=""
            ),
            designations=None,
            show_reserve_button=None,
            # Set the show_examination_button to TRUE for all Xpro issues
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        return issue
