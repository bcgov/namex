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


class AnalysisResultCodes(Enum):
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

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values


# Not a 'todo', just a note for later - these probably correlate to some JSON schemas in the LEAR project
# bcgov/lear/schemas/src/registry_schemas/schemas for namerequest schema
class BCProtectedNameEntityTypes(Enum):
    BC_CORPORATION = 'CR'
    BC_UNLIMITED_LIABILITY_COMPANY = 'UL'
    BC_COOPERATIVE = 'CP'
    BC_BENEFIT_COMPANY = 'BC'
    BC_COMMUNITY_CONTRIBUTION_COMPANY = 'CC'

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values


class BCUnprotectedNameEntityTypes(Enum):
    BC_SOLE_PROPRIETORSHIP = 'FR'
    BC_DOING_BUSINESS_AS = 'DBA'
    BC_COOPERATIVE = 'GP'
    BC_BC_BENEFIT_COMPANY = 'LP'
    BC_CC_COMMUNITY_CONTRIBUTION_COMPANY = 'LL'

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values


class XproUnprotectedNameEntityTypes(Enum):
    XPRO_CORPORATION = 'XCR'
    XPRO_UNLIMITED_LIABILITY_COMPANY = 'XUL'
    XPRO_COOPERATIVE = 'XCP'
    XPRO_LIMITED_LIABILITY_COMPANY = 'XLC'
    XPRO_LIMITED_PARTNERSHIP = 'XLP'
    XPRO_LIMITED_LIABILITY_PARTNERSHIP = 'XLL'

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values

