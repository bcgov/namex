from enum import Enum

# TODO: I have copied this over to new name processing service, hoping I can get rid of this here...
class DataFrameFields(Enum):
    FIELD_SYNONYMS = 'synonyms_text'
    FIELD_SPECIAL_WORDS = 'rc_words'
    DESCRIPTIVE = 'DESC'
    DISTINCTIVE = 'DIST'
    UNCLASSIFIED = 'NONE'


# TODO: Confirm that this is correct!
class ValidLocations(Enum):
    CA_BC = 'BC'
    CA_NOT_BC = 'CA'
    # CA = 'CA',
    INTL = 'INTL'

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
    # TODO: Arturo why did you comment these out?
    # BC_COOPERATIVE = 'CP'
    # BC_BENEFIT_COMPANY = 'BC'
    # BC_COMMUNITY_CONTRIBUTION_COMPANY = 'CC'

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class BCUnprotectedNameEntityTypes(Enum):
    BC_SOLE_PROPRIETORSHIP = 'FR'
    BC_DOING_BUSINESS_AS = 'DBA'
    BC_GENERAL_PARTNERSHIP = 'GP'
    BC_LIMITED_PARTNERSHIP = 'LP'
    BC_LIMITED_LIABILITY_PARTNERSHIP = 'LL'

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

class XproUnprotectedNameEntityTypes(Enum):
    XPRO_CORPORATION = 'XCR'
    XPRO_UNLIMITED_LIABILITY_COMPANY = 'XUL'
    # TODO: Arturo, why is XCP now commented out?
    # XPRO_COOPERATIVE = 'XCP'
    # XPRO_LIMITED_LIABILITY_COMPANY = 'XLC'
    XPRO_LIMITED_LIABILITY_COMPANY = 'RLC'  # TODO: Where is this code!
    XPRO_LIMITED_PARTNERSHIP = 'XLP'
    XPRO_LIMITED_LIABILITY_PARTNERSHIP = 'XLL'

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_