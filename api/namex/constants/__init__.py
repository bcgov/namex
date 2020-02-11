from enum import Enum


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
    BC_GENERAL_PARTNERSHIP = 'GP'
    BC_LIMITED_PARTNERSHIP = 'LP'
    BC_LIMITED_LIABILITY_PARTNERSHIP = 'LL'

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