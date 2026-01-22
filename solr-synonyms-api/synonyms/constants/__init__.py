from enum import Enum


class AbstractEnum(Enum):
    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


# TODO: I have copied this over to new name processing service, hoping I can get rid of this here...
class DataFrameFields(Enum):
    FIELD_SYNONYMS = "synonyms_text"
    FIELD_SPECIAL_WORDS = "rc_words"
    DESCRIPTIVE = "DESC"
    DISTINCTIVE = "DIST"
    UNCLASSIFIED = "NONE"


class DesignationPositionCodes(AbstractEnum):
    START = "start"
    END = "end"
    ANY = "any"


class ValidLocations(AbstractEnum):
    CA_BC = "BC"
    CA_NOT_BC = "CA"
    # CA = 'CA',
    INTL = "IN"


"""
We use the full name in the Enum code KEY so there is always context to what the code type represents,
so we don't always have to refer to the Enum description, documentation, or this file.

The Enum code VALUE (str) is the actual mapping value for the Enum code type
"""


class EntityTypes(AbstractEnum):
    # BC Types
    CORPORATION = "CR"
    UNLIMITED_LIABILITY_COMPANY = "UL"
    SOLE_PROPRIETORSHIP = "FR"
    GENERAL_PARTNERSHIP = "GP"
    DOING_BUSINESS_AS = "DBA"
    LIMITED_PARTNERSHIP = "LP"
    LIMITED_LIABILITY_PARTNERSHIP = "LL"
    COOPERATIVE = "CP"
    BENEFIT_COMPANY = "BC"
    COMMUNITY_CONTRIBUTION_COMPANY = "CC"
    SOCIETY = "SO"
    PRIVATE_ACT = "PA"
    FINANCIAL_INSTITUTION = "FI"
    PARISH = "PAR"
    # XPRO and Foreign Types
    XPRO_CORPORATION = "XCR"
    XPRO_UNLIMITED_LIABILITY_COMPANY = "XUL"
    XPRO_LIMITED_LIABILITY_COMPANY = "RLC"
    XPRO_LIMITED_PARTNERSHIP = "XLP"
    XPRO_LIMITED_LIABILITY_PARTNERSHIP = "XLL"
    XPRO_COOPERATIVE = "XCP"
    XPRO_SOCIETY = "XSO"
    # Used for mapping back to legacy oracle codes
    FIRM = "FIRM"


"""
Sole Proprietorship
Doing Business As
Corporation
Unlimited Liability Co.
Benefit Co.
General Partnership
Limited Partnership
Limited Liability Partnership
Co-operative
Community Contribution Co.
"""


class BCProtectedNameEntityTypes(AbstractEnum):
    SOLE_PROPRIETORSHIP = EntityTypes.SOLE_PROPRIETORSHIP.value
    DOING_BUSINESS_AS = EntityTypes.DOING_BUSINESS_AS.value
    CORPORATION = EntityTypes.CORPORATION.value
    UNLIMITED_LIABILITY_COMPANY = EntityTypes.UNLIMITED_LIABILITY_COMPANY.value
    BENEFIT_COMPANY = EntityTypes.BENEFIT_COMPANY.value
    GENERAL_PARTNERSHIP = EntityTypes.GENERAL_PARTNERSHIP.value
    LIMITED_PARTNERSHIP = EntityTypes.LIMITED_PARTNERSHIP.value
    LIMITED_LIABILITY_PARTNERSHIP = EntityTypes.LIMITED_LIABILITY_PARTNERSHIP.value
    COOPERATIVE = EntityTypes.COOPERATIVE.value
    COMMUNITY_CONTRIBUTION_COMPANY = EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value
    SOCIETY = EntityTypes.SOCIETY.value


# TODO: Are these still valid for unprotected?
class BCUnprotectedNameEntityTypes(AbstractEnum):
    SOLE_PROPRIETORSHIP = EntityTypes.SOLE_PROPRIETORSHIP.value
    DOING_BUSINESS_AS = EntityTypes.DOING_BUSINESS_AS.value
    GENERAL_PARTNERSHIP = EntityTypes.GENERAL_PARTNERSHIP.value
    LIMITED_PARTNERSHIP = EntityTypes.LIMITED_PARTNERSHIP.value
    LIMITED_LIABILITY_PARTNERSHIP = EntityTypes.LIMITED_LIABILITY_PARTNERSHIP.value


class XproUnprotectedNameEntityTypes(AbstractEnum):
    XPRO_CORPORATION = EntityTypes.XPRO_CORPORATION.value
    XPRO_UNLIMITED_LIABILITY_COMPANY = EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value
    XPRO_LIMITED_LIABILITY_COMPANY = EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value
    XPRO_LIMITED_PARTNERSHIP = EntityTypes.XPRO_LIMITED_PARTNERSHIP.value
    XPRO_LIMITED_LIABILITY_PARTNERSHIP = EntityTypes.XPRO_LIMITED_LIABILITY_PARTNERSHIP.value
    XPRO_SOCIETY = EntityTypes.XPRO_SOCIETY.value
