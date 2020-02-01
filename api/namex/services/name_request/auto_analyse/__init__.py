from enum import Enum

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

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values

# TODO: Confirm that this is correct!
class ValidLocations(Enum):
    CA_BC = 'BC'
    CA_NOT_BC = 'CA'
    # CA = 'CA',
    INTL = 'INTL'


class AnalysisRequestActions(Enum):
    NEW = 'NEW'  # Start a new business (NAME PROTECTION)
    AML = 'AML'  # Amalgamate (NAME PROTECTION, BC ONLY)
    DBA = 'DBA'  # Get a new trade name (NO NAME PROTECTION)
    CHG = 'CHG'  # Change your name (it's coming stub it out)
    MVE = 'MVE'  # Move your business
    CNV = 'CNV'  # Convert to another structure
    REH = 'REH'  # Restore from historical business
    REN = 'REN'  # Restore by starting a new business


class AnalysisResultCodes(Enum):
    VALID_NAME = 'auto_approved'
    ADD_DISTINCTIVE_WORD = 'add_distinctive'
    ADD_DESCRIPTIVE_WORD = 'add_descriptive'
    WORD_TO_AVOID = 'word_to_avoid'
    DESIGNATION_MISMATCH = 'designation_mismatch'
    DESIGNATION_MISPLACED = 'designation_misplaced'
    NAME_REQUIRES_CONSENT = 'consent_required'
    CONTAINS_UNCLASSIFIABLE_WORD = 'unclassified_word'
    CORPORATE_CONFLICT = 'corp_conflict'


# Not a 'todo', just a note for later - these probably correlate to some JSON schemas in the LEAR project
# bcgov/lear/schemas/src/registry_schemas/schemas for namerequest schema
class BCProtectedNameEntityTypes(Enum):
    BC_CORPORATION = 'CR'
    BC_UNLIMITED_LIABILITY_COMPANY = 'UL'
    BC_COOPERATIVE = 'CP'
    BC_BENEFIT_COMPANY = 'BC'
    BC_COMMUNITY_CONTRIBUTION_COMPANY = 'CC'


class BCUnprotectedNameEntityTypes(Enum):
    BC_SOLE_PROPRIETORSHIP = 'FR'
    BC_DOING_BUSINESS_AS = 'DBA'
    BC_COOPERATIVE = 'GP'
    BC_BC_BENEFIT_COMPANY = 'LP'
    BC_CC_COMMUNITY_CONTRIBUTION_COMPANY = 'LL'


class XproUnprotectedNameEntityTypes(Enum):
    XPRO_CORPORATION = 'XCR'
    XPRO_UNLIMITED_LIABILITY_COMPANY = 'XUL'
    XPRO_COOPERATIVE = 'XCP'
    XPRO_LIMITED_LIABILITY_COMPANY = 'XLC'
    XPRO_LIMITED_PARTNERSHIP = 'XLP'
    XPRO_LIMITED_LIABILITY_PARTNERSHIP = 'XLL'

