from enum import Enum
from nltk.stem import PorterStemmer

porter = PorterStemmer()

# Limit number of words to analyse
# TODO: We can set this to three later (in PROD), but this is way easier to test with a higher max limit
# eg. I can easily test for a bunch of issues using Flerkin Mountain View Engineering Cooperative
# TODO: Make this configurable in OpenShift
MAX_LIMIT = 4

# TODO: Make this configurable in OpenShift
# Limit number of matches returned to user
MAX_MATCHES_LIMIT = 1


# TODO: I have copied this over to new name processing service, hoping I can get rid of this here...
class DataFrameFields(Enum):
    FIELD_SYNONYMS = 'synonyms_text'
    FIELD_SPECIAL_WORDS = 'rc_words'
    DESCRIPTIVE = 'DESC'
    DISTINCTIVE = 'DIST'
    UNCLASSIFIED = 'NONE'


class ProcedureResult:
    def __init__(self, **kwargs):
        self.is_valid = kwargs.get('is_valid', False)
        self.result_code = kwargs.get('result_code', None)
        self.values = kwargs.get('values', None)


class AnalysisRequestActions(str, Enum):
    NEW = 'NEW'  # Start a new business (NAME PROTECTION)
    AML = 'AML'  # Amalgamate (NAME PROTECTION, BC ONLY)
    DBA = 'DBA'  # Get a new trade name (NO NAME PROTECTION)
    CHG = 'CHG'  # Change your name (it's coming stub it out)
    MVE = 'MVE'  # Move your business
    CNV = 'CNV'  # Convert to another structure
    REH = 'REH'  # Restore from historical business
    REN = 'REN'  # Restore by starting a new business
    REST = 'REST'  # NOT 100% sure what this is

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values


class AnalysisResponseCodes(str, Enum):
    # TODO: Not the best idea to have a cased constant, but this is what is used on the frontend, we can change it later
    AUTO_APPROVED = 'Available'
    FURTHER_ACTION_REQUIRED = 'fa'


class AnalysisIssueCodes(str, Enum):
    CHECK_IS_VALID = 'check_is_valid'
    ADD_DISTINCTIVE_WORD = 'add_distinctive'  # Well formed
    ADD_DESCRIPTIVE_WORD = 'add_descriptive'  # Well formed
    TOO_MANY_WORDS = 'excess_words'  # Well formed
    INCORRECT_CATEGORY = 'incorrect_category'  # Well formed
    # Stop if error with Well Formed
    CONTAINS_UNCLASSIFIABLE_WORD = 'unclassified_word'  # To examiner
    # Stop if error
    CORPORATE_CONFLICT = 'corp_conflict'
    QUEUE_CONFLICT = "queue_conflict"
    # Stop if error
    # TODO: What about these other guys?
    WORDS_TO_AVOID = 'word_to_avoid'
    WORD_SPECIAL_USE = 'word_special_use'
    DESIGNATION_MISMATCH = 'designation_mismatch'
    END_DESIGNATION_MORE_THAN_ONCE = 'end_designation_more_than_once'
    DESIGNATION_MISPLACED = 'designation_misplaced'
    NAME_REQUIRES_CONSENT = 'consent_required'
    DESIGNATION_NON_EXISTENT = 'designation_non_existent'

    def __getstate__(self):
        pickled_state = str(self.value)
        return pickled_state

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values
