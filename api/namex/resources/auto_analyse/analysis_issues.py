from datetime import date
from string import Template

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from namex.utils.service_utils import get_entity_type_description

# Import DTOs
from .response_objects.name_analysis_issue import NameAnalysisIssue
from .response_objects.name_action import NameAction, NameActions, WordPositions
from .response_objects.consenting_body import ConsentingBody
from .response_objects.conflict import Conflict


class AnalysisResponseIssue:
    issue_type = "Issue"  # Maybe get rid of this guy
    header = "Further Action Required"
    status_text = ""
    status = "fa"  # This is a CODE [AV | FA | RC]
    issue = None

    '''
    @:param setup_config Setup[]
    '''
    def __init__(self, entity_type, setup_config):
        self.entity_type = entity_type
        self.setup_config = []
        self.set_issue_setups(setup_config)

    def create_issue(self, procedure_result):
        return self.issue

    '''
    @:param setup_config Setup[]
    '''
    def set_issue_setups(self, setup_config):
        self.setup_config = setup_config

    @classmethod
    def _join_list_words(cls, list_words):
        return "<b>" + ", ".join(list_words) + "</b>"


class CheckIsValid(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.CHECK_IS_VALID
    status_text = "Approved"
    issue = None

    def create_issue(self, procedure_result):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1=None,
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=None,
            show_examination_button=None,
            conflicts=None,
            setup=None,
            name_actions=None
        )

        return issue


"""
Word Classification Engine Issues
"""


'''
@:deprecated
'''

# TODO: Get RID OF THIS!!!


class IncorrectCategory(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.INCORRECT_CATEGORY
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="Category of the word is incorrect.",
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=True,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        issue.name_actions = [
            NameAction(
                type=NameActions.HIGHLIGHT
            )
        ]

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue


"""
Well-Formed Name Issues
"""


class ContainsUnclassifiableWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        list_name = procedure_result.values['list_name']
        list_none = procedure_result.values['list_none']

        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="The word(s) " + self._join_list_words(list_none) + " have not previously been approved for use.",
            line2="Please check wait times at the top of the screen.",
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        # TODO: Fix the case eg. 'Asdfadsf Something Asdfadsf Company Ltd.'...
        #  If there's a duplicate of an unclassified word, just grabbing the index won't do!
        issue.name_actions = []
        for word in list_none:
            none_word_idx = list_name.index(word)
            issue.name_actions.append(
                NameAction(
                    type=NameActions.HIGHLIGHT,
                    word=word,
                    index=none_word_idx
                )
            )

        # Setup boxes
        issue.setup = self.setup_config
        # Replace template strings in setup boxes
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue


class AddDistinctiveWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.ADD_DISTINCTIVE_WORD
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="Requires a word at the beginning of your name that sets it apart.",
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        list_name = procedure_result.values['list_name']

        issue.name_actions = [
            NameAction(
                type=NameActions.BRACKETS,
                position=WordPositions.START,
                message="Add a Word Here",
                word=list_name[0] if list_name.__len__() > 0 else None,
                index=0
            )
        ]

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue


class AddDescriptiveWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        list_name = procedure_result.values['list_name']
        list_dist = procedure_result.values['list_dist']

        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="Requires a word that describes the nature of your business.",
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        last_dist_word = list_dist.pop() if list_dist.__len__() > 0 else None
        # TODO: Why was this like this before?
        # dist_word_idx = list_name.index(last_dist_word) # if list_dist.__len__() > 0 else 0
        dist_word_idx = list_name.index(last_dist_word) if list_dist.__len__() > 0 else 0
        issue.name_actions = [
            NameAction(
                type=NameActions.BRACKETS,
                position=WordPositions.END,
                message="Add a Descriptive Word Here",
                word=last_dist_word,
                index=dist_word_idx
            )
        ]

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue


class TooManyWordsIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.TOO_MANY_WORDS
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="Names longer than three words, not including proper designations, may be sent to examination.",
            line2="Please check wait times at the top of the screen.",
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=True,
            conflicts=None,
            setup=None,
            name_actions=None
        )

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue


"""
General Name Issues
"""


class ContainsWordsToAvoidIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.WORDS_TO_AVOID
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        list_name = procedure_result.values['list_name']
        list_avoid = procedure_result.values['list_avoid']

        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="The word(s) " + self._join_list_words(list_avoid) + " cannot be used.",
            line2="",
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        # TODO: If there's a duplicate of a word to avoid, just grabbing the index might not do!
        issue.name_actions = []
        for word in list_avoid:
            avoid_word_idx = list_name.index(word)
            issue.name_actions.append(
                NameAction(
                    type=NameActions.STRIKE,
                    word=word,
                    index=avoid_word_idx
                )
            )

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue


# TODO: Is this even a thing?
'''
@:deprecated
'''


class WordSpecialUse(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.WORD_SPECIAL_USE
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        list_name = procedure_result.values['list_name']
        list_special = procedure_result.values['list_special']

        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="",
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=True,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        # TODO: If there's a duplicate of a word to avoid, just grabbing the index might not do!
        issue.name_actions = []
        for word in list_special:
            list_special_idx = list_name.index(word)
            issue.name_actions.append(
                NameAction(
                    type=NameActions.HIGHLIGHT,
                    word=word,
                    index=list_special_idx
                )
            )

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue


class NameRequiresConsentIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.NAME_REQUIRES_CONSENT
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        list_name = procedure_result.values['list_name']
        list_consent = procedure_result.values['list_consent']

        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="The word(s) " + self._join_list_words(list_consent) + " are restricted and may require consent.",
            line2="Please check the options below.",
            consenting_body=ConsentingBody(
                name="",
                email=""
            ),
            designations=None,
            show_reserve_button=None,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        issue.name_actions = []
        for word in list_consent:
            consent_word_idx = list_name.index(word)
            issue.name_actions.append(
                NameAction(
                    type=NameActions.HIGHLIGHT,
                    word=word,
                    index=consent_word_idx
                )
            )

        # TODO: Where does this info come from?
        issue.consenting_body = ConsentingBody(
            name="Example Conflict Company Ltd.",
            email="email@example.com"
        )

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue


class CorporateNameConflictIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.CORPORATE_CONFLICT
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        list_name = procedure_result.values['list_name']
        list_dist = procedure_result.values['list_dist']
        list_desc = procedure_result.values['list_desc']
        list_conflicts = procedure_result.values['list_conflicts']

        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="Too similar to an existing name.",
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=None,
            show_examination_button=False,
            conflicts=[],
            setup=None,
            name_actions=[]
        )

        '''
        eg:
        list_name: <class 'list'>: ['mountain', 'view', 'growers']
        list_dist: <class 'list'>: [['mountain'], ['mountain', 'view']]
        list_desc: <class 'list'>: [['view', 'growers'], ['growers']]
        list_conflicts: <class 'dict'>: {'MOUNTAIN VIEW GROWERS INC.': {'mountain': ['mountain'], 'view': ['view'], 'growers': ['growers']}}
        '''

        # Grab the first conflict
        current_conflict_name = list(list_conflicts.keys())[0]  # eg: 'MOUNTAIN VIEW GROWERS INC.'
        current_conflict = list_conflicts[current_conflict_name]  # eg: {'mountain': ['mountain'], 'view': ['view'], 'growers': ['growers']}
        current_conflict_keys = list(current_conflict.keys()) if current_conflict else []

        is_exact_match = (list_name == current_conflict_keys)

        list_dist_words = list(set([item for sublist in list_dist for item in sublist]))
        list_desc_words = list(set([item for sublist in list_desc for item in sublist]))

        # Apply our is_exact_match strategy:
        # - Add brackets after the first distinctive word
        # - Add brackets after the last descriptive word?
        # - Strike out the last word

        list_remove = []  # These are passed down to the Template

        if is_exact_match:
            # Loop over the list_name words, we need to decide to do with each word
            for word in list_name:
                name_word_idx = list_name.index(word)

                # Highlight the descriptives
                # <class 'list'>: ['mountain', 'view']
                if word in list_dist_words:
                    issue.name_actions.append(NameAction(
                        word=word,
                        index=name_word_idx,
                        type=NameActions.HIGHLIGHT
                    ))

                # Strike out the last descriptive word
                if word in list_desc_words and name_word_idx == list_name.__len__() - 1:
                    # <class 'list'>: ['growers', 'view']
                    list_remove.append(word)
                    issue.name_actions.append(NameAction(
                        word=word,
                        index=name_word_idx,
                        type=NameActions.STRIKE
                    ))

        if not is_exact_match:
            # Loop over the list_name words, we need to decide to do with each word
            for word in list_name:
                name_word_idx = list_name.index(word)

                # Highlight the descriptives
                # <class 'list'>: ['mountain', 'view']
                if word in list_dist_words:
                    issue.name_actions.append(NameAction(
                        word=word,
                        index=name_word_idx,
                        type=NameActions.HIGHLIGHT
                    ))

                # Strike out the last descriptive word
                '''
                if word in list_desc_words and name_word_idx == list_name.__len__() - 1:
                    # <class 'list'>: ['growers', 'view']
                    issue.name_actions.append(NameAction(
                        word=word,
                        index=name_word_idx,
                        type=NameActions.STRIKE
                    ))
                '''

        issue.conflicts = []

        conflict = Conflict(
            name=current_conflict_name,
            date=date.today()
        )

        issue.conflicts.append(conflict)

        # Setup boxes
        issue.setup = self.setup_config
        # Replace template strings in setup boxes
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute({
                        'list_name': self._join_list_words(list_name),
                        'list_remove': self._join_list_words(list_remove),
                        'list_dist': self._join_list_words(list_dist_words),
                        'list_desc': self._join_list_words(list_desc_words)
                    }))

        return issue


class DesignationNonExistentIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.DESIGNATION_NON_EXISTENT
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        list_name = procedure_result.values['list_name']
        correct_designations = procedure_result.values['correct_designations']

        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="The name must include one of the following designation(s):",
            line2=None,
            consenting_body=None,
            designations=correct_designations,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        # Setup boxes
        issue.setup = self.setup_config
        # Replace template strings in setup boxes
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute({
                        'list_name': self._join_list_words(list_name),
                        'correct_designations': self._join_list_words(correct_designations)
                    }))

        return issue


class DesignationMismatchIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.DESIGNATION_MISMATCH
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        list_name = procedure_result.values['list_name']
        incorrect_designations = procedure_result.values['incorrect_designations']
        correct_designations = procedure_result.values['correct_designations']
        # TODO: Implement the misplaced designations cases!
        # TODO: I think we can remove this, misplaced has been moved out into its own procedure!
        # misplaced_any_designation = procedure_result.values['misplaced_any_designation']
        # misplaced_end_designation = procedure_result.values['misplaced_end_designation']

        # TODO: If case comes back in upper case for the incorrect designations we won't have a match...
        # Convert all strings to lower-case before comparing
        incorrect_designations_lc = list(map(lambda d: d.lower() if isinstance(d, str) else '', incorrect_designations))
        list_name_lc = list(map(lambda d: d.lower(), list_name))

        entity_type_description = get_entity_type_description(self.entity_type)

        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="The " + self._join_list_words(incorrect_designations) + " designation(s) cannot be used with selected entity type of " + entity_type_description + " </b>",
            line2=None,
            consenting_body=None,
            designations=correct_designations,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        # Loop over the list_name words, we need to decide to do with each word
        for word in list_name_lc:
            name_word_idx = list_name.index(word)

            # Highlight the descriptives
            # <class 'list'>: ['mountain', 'view']
            if word in incorrect_designations_lc:
                issue.name_actions.append(NameAction(
                    word=word,
                    index=name_word_idx,
                    type=NameActions.HIGHLIGHT
                ))

        # Setup boxes
        issue.setup = self.setup_config
        # Replace template strings in setup boxes
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute({
                        'list_name': self._join_list_words(list_name),
                        'correct_designations': self._join_list_words(correct_designations),
                        'incorrect_designations': self._join_list_words(incorrect_designations),
                        'entity_type': self.entity_type  # TODO: Map this CODE!
                    }))

        return issue


class DesignationMisplacedIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.DESIGNATION_MISPLACED
    status_text = "Further Action Required"
    issue = None

    def create_issue(self, procedure_result):
        list_name = procedure_result.values['list_name']
        misplaced_any_designation = procedure_result.values['misplaced_any_designation']
        misplaced_end_designation = procedure_result.values['misplaced_end_designation']
        misplaced_all_designation = procedure_result.values['misplaced_all_designation']

        list_name_lc = list(map(lambda d: d.lower(), list_name))

        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="The " + self._join_list_words(
                misplaced_end_designation) + " designation(s) cannot be used in a position different to end of the name." ,
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )


        # Loop over the list_name words, we need to decide to do with each word
        for word in list_name_lc:
            name_word_idx = list_name.index(word)

            # Highlight the descriptives
            # <class 'list'>: ['mountain', 'view']
            if word in misplaced_all_designation:
                issue.name_actions.append(NameAction(
                    word=word,
                    index=name_word_idx,
                    type=NameActions.HIGHLIGHT
                ))


        # Setup boxes
        # TODO: We need setup boxes for this new stuff...
        issue.setup = self.setup_config

        return issue
