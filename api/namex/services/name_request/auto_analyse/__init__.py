import jsonpickle
import json
from enum import Enum

# Define service variables

# Limit number of words to analyse
MAX_LIMIT = 4


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

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values


class AnalysisResultCodes(str, Enum):
    VALID_NAME = 'auto_approved'

    ADD_DISTINCTIVE_WORD = 'add_distinctive'  # Well formed
    ADD_DESCRIPTIVE_WORD = 'add_descriptive'  # Well formed
    TOO_MANY_WORDS = 'excess_words'  # Well formed
    # Stop if error with Well Formed
    CONTAINS_UNCLASSIFIABLE_WORD = 'unclassified_word'  # To examiner
    # Stop if error
    CORPORATE_CONFLICT = 'corp_conflict'
    # Stop if error
    # TODO: What about these other guys?
    WORD_TO_AVOID = 'word_to_avoid'
    DESIGNATION_MISMATCH = 'designation_mismatch'
    NAME_REQUIRES_CONSENT = 'consent_required'

    def __getstate__(self):
        pickled_state = str(self.value)
        return pickled_state

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values
