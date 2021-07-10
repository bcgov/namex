"""Name requires consent issue classes."""
from namex.resources.auto_analyse.issues import NameRequiresConsentIssue

from ....response_objects import ConsentingBody, NameAnalysisIssue


class BcNameRequiresConsentIssue(NameRequiresConsentIssue):
    """BC name requires consent issue."""

    pass


class XproNameRequiresConsentIssue(NameRequiresConsentIssue):
    """XPRO name requires consent issue."""

    def create_issue(self):
        """Create XPRO name requires consent issue."""
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1='',
            line2='',
            consenting_body=ConsentingBody(
                name='',
                email=''
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
