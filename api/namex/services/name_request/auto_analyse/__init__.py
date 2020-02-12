import jsonpickle
import json
from enum import Enum

# Limit number of words to analyse
# TODO: We can set this to three later (in PROD), but this is way easier to test with a higher max limit
# eg. I can easily test for a bunch of issues using Flerkin Mountain View Engineering Cooperative
# TODO: Make this configurable in OpenShift
MAX_LIMIT = 4

# Limit number of words to analyse
MAX_LIMIT = 4


class ProcedureResult:
    def __init__(self, **kwargs):
        self.is_valid = kwargs.get('is_valid', False)
        self.result_code = kwargs.get('result_code', None)
        self.values = kwargs.get('values', None)

# Field dataframe
field_synonyms = 'synonyms_text'
field_special_words = 'rc_words'

field_synonyms = 'synonyms_text'
field_special_words = 'rc_words'


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
    ADD_DISTINCTIVE_WORD = 'add_distinctive'
    ADD_DESCRIPTIVE_WORD = 'add_descriptive'
    WORD_TO_AVOID = 'word_to_avoid'
    DESIGNATION_MISMATCH = 'designation_mismatch'
    DESIGNATION_MISPLACED = 'designation_misplaced'
    NAME_REQUIRES_CONSENT = 'consent_required'
    CONTAINS_UNCLASSIFIABLE_WORD = 'unclassified_word'
    CORPORATE_CONFLICT = 'corp_conflict'

    def __getstate__(self):
        pickled_state = str(self.value)
        return pickled_state

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values




