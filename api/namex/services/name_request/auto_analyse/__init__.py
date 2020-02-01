from enum import Enum

# Define service variables

# Modes
MODE_SYNS = 'Syns'
MODE_SUBS = 'Subs'
MODE_STOP = 'Stop'

# Categories
dsg_end = 'Designations_end'
dsg_any = 'Designations_any'
stop_w = 'Stop Words'

# Limit number of words to analyse
MAX_LIMIT = 4


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
    TOO_MANY_WORDS = 'excess_words'
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

