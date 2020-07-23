from enum import Enum

# Modes
MODE_SYNS = 'Syns'
MODE_SUBS = 'Subs'
MODE_STOP = 'Stop'

# Categories
dsg_end = 'Designations_end'
dsg_any = 'Designations_any'
stop_w = 'Stop Words'


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


class DesignationPositionCodes(AbstractEnum):
    START = 'start'
    END = 'end'
    ANY = 'any'


class LanguageCodes(AbstractEnum):
    ENG = 'ENGLISH'
    FR = 'FRENCH'


class ValidLocations(AbstractEnum):
    CA_BC = 'BC'
    CA_NOT_BC = 'CA'
    # CA = 'CA',
    INTL = 'IN'


class ValidSources(AbstractEnum):
    NAMEX = 'NAMEX'
    NAMEREQUEST = 'NAMEREQUEST'
    NRO = 'NRO'
    SO = 'SO'


# Request Action for name request and namex (includes legacy)
class RequestAction(AbstractEnum):
    NEW = 'NEW'
    MVE = 'MVE'
    CHG = 'CHG'
    DBA = 'DBA'
    AML = 'AML'
    CNV = 'CNV'
    REH = 'REH'
    REN = 'REN'
    AS = 'ASSUMED'
    ACHG = 'CHG-ASSUM'
    # required for legacy
    NEW_AML = 'NRO-NEWAML'
    REST = 'NRO-REST'


'''
We use the full name in the Enum code KEY so there is always context to what the code type represents, 
so we don't always have to refer to the Enum description, documentation, or this file.

The Enum code VALUE (str) is the actual mapping value for the Enum code type
'''


class EntityTypes(AbstractEnum):
    # BC Types
    CORPORATION = 'CR'
    UNLIMITED_LIABILITY_COMPANY = 'UL'
    SOLE_PROPRIETORSHIP = 'FR'
    GENERAL_PARTNERSHIP = 'GP'
    DOING_BUSINESS_AS = 'DBA'
    LIMITED_PARTNERSHIP = 'LP'
    LIMITED_LIABILITY_PARTNERSHIP = 'LL'
    COOPERATIVE = 'CP'
    BENEFIT_COMPANY = 'BC'
    COMMUNITY_CONTRIBUTION_COMPANY = 'CC'
    SOCIETY = 'SO'
    PRIVATE_ACT = 'PA'
    FINANCIAL_INSTITUTION = 'FI'
    PARISH = 'PAR'
    # XPRO and Foreign Types
    XPRO_CORPORATION = 'XCR'
    XPRO_UNLIMITED_LIABILITY_COMPANY = 'XUL'
    XPRO_LIMITED_LIABILITY_COMPANY = 'RLC'
    XPRO_LIMITED_PARTNERSHIP = 'XLP'
    XPRO_LIMITED_LIABILITY_PARTNERSHIP = 'XLL'
    XPRO_COOPERATIVE = 'XCP'
    XPRO_SOCIETY = 'XSO'
    # Used for mapping back to legacy oracle codes
    FIRM = 'FIRM'


EntityTypeDescriptions = {
    # BC Types
    EntityTypes.CORPORATION: 'Corporation',
    EntityTypes.UNLIMITED_LIABILITY_COMPANY: 'Unlimited Liability Company',
    EntityTypes.SOLE_PROPRIETORSHIP: 'Sole Proprietorship',
    EntityTypes.GENERAL_PARTNERSHIP: 'General Partnership',
    EntityTypes.DOING_BUSINESS_AS: 'Doing Business As',
    EntityTypes.LIMITED_PARTNERSHIP: 'Limited Partnership',
    EntityTypes.LIMITED_LIABILITY_PARTNERSHIP: 'Limited Liability Partnership',
    EntityTypes.COOPERATIVE: 'Cooperative',
    EntityTypes.BENEFIT_COMPANY: 'Benefit Company',
    EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY: 'Community Contribution Company',
    EntityTypes.SOCIETY: 'Society',
    EntityTypes.PRIVATE_ACT: 'Private Act',
    EntityTypes.FINANCIAL_INSTITUTION: 'Financial Institution',
    EntityTypes.PARISH: 'Parish',
    # XPRO and Foreign Types
    EntityTypes.XPRO_CORPORATION: 'Extraprovincial Corporation',
    EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY: 'Extraprovincial Unlimited Liability Company',
    EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY: 'Extraprovincial Limited Liability Company',
    EntityTypes.XPRO_LIMITED_PARTNERSHIP: 'Extraprovincial Limited Partnership',
    EntityTypes.XPRO_LIMITED_LIABILITY_PARTNERSHIP: 'Extraprovincial Limited Liability Partnership',
    EntityTypes.XPRO_COOPERATIVE: 'Extraprovincial Cooperative',
    EntityTypes.XPRO_SOCIETY: 'Extraprovincial Society',
    # Used for mapping back to legacy oracle codes, description not required
    EntityTypes.FIRM: 'FIRM (Legacy Oracle)'
}


'''
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
'''


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
    XPRO_COOPERATIVE = EntityTypes.XPRO_COOPERATIVE.value


# Request types (legacy) used in search conflicts
class LegacyBCORPEntityTypes(AbstractEnum):
    CCR = 'CCR'
    CT = 'CT'
    RCR = 'RCR'


class LegacyULCEntityTypes(AbstractEnum):
    UC = 'UC'
    CUL = 'CUL'
    ULCT = 'ULCT'
    RUL = 'RUL'


class LegacyCPEntityTypes(AbstractEnum):
    CCP = 'CCP'
    CTC = 'CTC'
    RCP = 'RCP'


class LegacyCCCEntityTypes(AbstractEnum):
    CCV = 'CCV'
    CC = 'CCC'
    CCCT = 'CCCT'
    RCC = 'RCC'


class LegacySOEntityTypes(AbstractEnum):
    ASO = 'ASO'
    CSO = 'CSO'
    RSO = 'RSO'
    CTSO = 'CTSO'
    CSSO = 'CSSO'


class LegacyFIEntityTypes(AbstractEnum):
    CFI = 'CFI'
    RFI = 'RFI'


class LegacyXCORPEntityTypes(AbstractEnum):
    XCCR = 'XCCR'
    XRCR = 'XRCR'
    AS = 'AS'


class LegacyXULCEntityTypes(AbstractEnum):
    UA = 'UA'
    XCUL = 'XCUL'
    XRUL = 'XRUL'


class LegacyXCPEntityTypes(AbstractEnum):
    XCCP = 'XCCP'
    XRCP = 'XRCP'


class LegacyXSOEntityTypes(AbstractEnum):
    XCSO = 'XCSO'
    XRSO = 'XRSO'
    XASO = 'XASO'
    XCASO = 'XCASO'


# Request types (legacy) used in search conflicts
class LegacyEntityTypes:
    CORPORATION = LegacyBCORPEntityTypes
    UNLIMITED_LIABILITY_COMPANY = LegacyULCEntityTypes
    COOPERATIVE = LegacyCPEntityTypes
    COMMUNITY_CONTRIBUTION_COMPANY = LegacyCCCEntityTypes
    SOCIETY = LegacySOEntityTypes
    FINANCIAL_INSTITUTION = LegacyFIEntityTypes
    XPRO_CORPORATION = LegacyXCORPEntityTypes
    XPRO_UNLIMITED_LIABILITY_COMPANY = LegacyXULCEntityTypes
    XPRO_COOPERATIVE = LegacyXCPEntityTypes
    XPRO_SOCIETY = LegacyXSOEntityTypes


request_type_mapping = [
    ('CR', EntityTypes.CORPORATION.value, RequestAction.NEW_AML.value),
    ('CR', EntityTypes.CORPORATION.value, RequestAction.NEW.value),
    ('CCR', EntityTypes.CORPORATION.value, RequestAction.CHG.value),
    ('CT', EntityTypes.CORPORATION.value, RequestAction.MVE.value),
    ('RCR', EntityTypes.CORPORATION.value, RequestAction.REST.value),
    ('XCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.NEW.value),
    ('XCCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.CHG.value),
    ('XRCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.REST.value),
    ('AS', EntityTypes.XPRO_CORPORATION.value, RequestAction.AS.value),
    ('LC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.NEW.value),
    ('CLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.CHG.value),
    ('RLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.REST.value),
    ('AL', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.AS.value),
    ('FR', EntityTypes.FIRM.value, RequestAction.NEW.value),
    ('CFR', EntityTypes.FIRM.value, RequestAction.CHG.value),
    ('LL', EntityTypes.LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.NEW.value),
    ('CLL', EntityTypes.LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.CHG.value),
    ('XLL', EntityTypes.XPRO_LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.NEW.value),
    ('XCLL', EntityTypes.XPRO_LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.CHG.value),
    ('LP', EntityTypes.LIMITED_PARTNERSHIP.value, RequestAction.NEW.value),
    ('CLP', EntityTypes.LIMITED_PARTNERSHIP.value, RequestAction.CHG.value),
    ('XLP', EntityTypes.XPRO_LIMITED_PARTNERSHIP.value, RequestAction.NEW.value),
    ('XCLP', EntityTypes.XPRO_LIMITED_PARTNERSHIP.value, RequestAction.CHG.value),
    ('SO', EntityTypes.SOCIETY.value, RequestAction.NEW.value),
    ('ASO', EntityTypes.SOCIETY.value, RequestAction.AML.value),
    ('CSO', EntityTypes.SOCIETY.value, RequestAction.CHG.value),
    ('RSO', EntityTypes.SOCIETY.value, RequestAction.REST.value),
    ('CTSO', EntityTypes.SOCIETY.value, RequestAction.MVE.value),
    ('CSSO', EntityTypes.SOCIETY.value, RequestAction.CNV.value),
    ('XSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.NEW.value),
    ('XCSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.CHG.value),
    ('XRSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.REST.value),
    ('XASO', EntityTypes.XPRO_SOCIETY.value, RequestAction.AS.value),
    ('XCASO', EntityTypes.XPRO_SOCIETY.value, RequestAction.ACHG.value),
    ('CP', EntityTypes.COOPERATIVE.value, RequestAction.NEW_AML.value),
    ('CCP', EntityTypes.COOPERATIVE.value, RequestAction.CHG.value),
    ('CTC', EntityTypes.COOPERATIVE.value, RequestAction.MVE.value),
    ('RCP', EntityTypes.COOPERATIVE.value, RequestAction.REST.value),
    ('XCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.NEW.value),
    ('XCCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.CHG.value),
    ('XRCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.REST.value),
    ('CC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.NEW_AML.value),
    ('CCV', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.CNV.value),
    ('CCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.CHG.value),
    ('CCCT', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.MVE.value),
    ('RCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.REST.value),
    ('UL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.NEW.value),
    ('UC', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.CNV.value),
    ('CUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.CHG.value),
    ('ULCT', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.MVE.value),
    ('RUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REST.value),
    ('UA', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.AS.value),
    ('XUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.NEW.value),
    ('XCUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.CHG.value),
    ('XRUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REST.value),
    ('FI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.NEW.value),
    ('CFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.CHG.value),
    ('RFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.REST.value),
    ('PA', EntityTypes.PRIVATE_ACT.value, RequestAction.NEW.value),
    ('PAR', EntityTypes.PARISH.value, RequestAction.NEW.value),
    ('BC', EntityTypes.BENEFIT_COMPANY.value, RequestAction.NEW.value),
    ('BEAM', EntityTypes.BENEFIT_COMPANY.value, RequestAction.AML.value),
    ('BEC', EntityTypes.BENEFIT_COMPANY.value, RequestAction.CHG.value),
    ('BECT', EntityTypes.BENEFIT_COMPANY.value, RequestAction.MVE.value),
    ('BERE', EntityTypes.BENEFIT_COMPANY.value, RequestAction.REST.value),
    ('BECV', EntityTypes.BENEFIT_COMPANY.value, RequestAction.CNV.value),
    ('BECR', EntityTypes.BENEFIT_COMPANY.value, RequestAction.CNV.value)
]


class NameState(AbstractEnum):
    NOT_EXAMINED = 'NE'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CONDITION = 'CONDITION'
    # Needed for name request reservation before completing the NR
    RESERVED = 'RESERVED'
    COND_RESERVE = 'COND-RESERVE'


class NameRequestActions(AbstractEnum):
    EDIT = 'EDIT'
    UPGRADE = 'UPGRADE'  # Upgrade priority
    CANCEL = 'CANCEL'
    REFUND = 'REFUND'  # Cancel with refund
    RECEIPT = 'RECEIPT'
    # Needed for name request reservation before completing the NR
    REAPPLY = 'RESERVED'
    RESEND = 'RESEND'  # Re-send notification


class NameRequestDraftActions(AbstractEnum):
    EDIT = NameRequestActions.EDIT.value
    UPGRADE = NameRequestActions.UPGRADE.value
    # CANCEL = NameRequestActions.CANCEL.value
    REFUND = NameRequestActions.REFUND.value
    RECEIPT = NameRequestActions.RECEIPT.value  # TODO: Is this even possible? I don't think we can can a receipt if it's a draft...
    # REAPPLY = NameRequestActions.REAPPLY.value
    # RESEND = NameRequestActions.RESEND.value


# TODO: What about these? I don't see them in the spreadsheet...
class NameRequestReservedActions(AbstractEnum):
    EDIT = NameRequestActions.EDIT.value
    UPGRADE = NameRequestActions.UPGRADE.value
    # CANCEL = NameRequestActions.CANCEL.value
    REFUND = NameRequestActions.REFUND.value
    RECEIPT = NameRequestActions.RECEIPT.value  # TODO: Is this even possible? I don't think we can can a receipt if it's a draft...
    # REAPPLY = NameRequestActions.REAPPLY.value
    # RESEND = NameRequestActions.RESEND.value


class NameRequestActiveActions(AbstractEnum):
    """
    Actions available when an NR is 'active' eg. in an APPROVED or CONDITIONAL state, NOT expired, and NOT consumed.
    """
    EDIT = NameRequestActions.EDIT.value
    # UPGRADE = NameRequestActions.UPGRADE.value
    CANCEL = NameRequestActions.CANCEL.value  # TODO: Confirm
    RECEIPT = NameRequestActions.RECEIPT.value
    REAPPLY = NameRequestActions.REAPPLY.value
    RESEND = NameRequestActions.RESEND.value


class NameRequestHoldActions(AbstractEnum):
    pass


class NameRequestInProgressActions(AbstractEnum):
    pass


class NameRequestExpiredActions(AbstractEnum):
    """
    Actions available when an NR is in an APPROVED or CONDITIONAL state, expired, and NOT consumed.
    """
    EDIT = NameRequestActions.EDIT.value
    # UPGRADE = NameRequestActions.UPGRADE.value  # TODO: Confirm
    # CANCEL = NameRequestActions.CANCEL.value
    RECEIPT = NameRequestActions.RECEIPT.value
    # REAPPLY = NameRequestActions.REAPPLY.value
    RESEND = NameRequestActions.RESEND.value


class NameRequestConsumedActions(AbstractEnum):
    """
    Actions available when an NR is in an APPROVED or CONDITIONAL state, and consumed.
    """
    # EDIT = NameRequestActions.EDIT.value
    # UPGRADE = NameRequestActions.UPGRADE.value
    # CANCEL = NameRequestActions.CANCEL.value
    RECEIPT = NameRequestActions.RECEIPT.value
    # REAPPLY = NameRequestActions.REAPPLY.value
    RESEND = NameRequestActions.RESEND.value


class NameRequestHistoricalActions(AbstractEnum):
    # EDIT = NameRequestActions.EDIT.value
    # UPGRADE = NameRequestActions.UPGRADE.value
    # CANCEL = NameRequestActions.CANCEL.value
    RECEIPT = NameRequestActions.RECEIPT.value
    # REAPPLY = NameRequestActions.REAPPLY.value
    # RESEND = NameRequestActions.RESEND.value


class NameRequestCancelledActions(AbstractEnum):
    EDIT = NameRequestActions.EDIT.value
    # UPGRADE = NameRequestActions.UPGRADE.value
    # CANCEL = NameRequestActions.CANCEL.value
    RECEIPT = NameRequestActions.RECEIPT.value
    # REAPPLY = NameRequestActions.REAPPLY.value
    # RESEND = NameRequestActions.RESEND.value  # TODO: Confirm


class NameRequestActiveRejectedActions(AbstractEnum):
    # EDIT = NameRequestActions.EDIT.value
    # UPGRADE = NameRequestActions.UPGRADE.value
    # CANCEL = NameRequestActions.CANCEL.value
    # RECEIPT = NameRequestActions.RECEIPT.value
    # REAPPLY = NameRequestActions.REAPPLY.value
    RESEND = NameRequestActions.RESEND.value


class NameRequestExpiredRejectedActions(AbstractEnum):
    # EDIT = NameRequestActions.EDIT.value
    # UPGRADE = NameRequestActions.UPGRADE.value
    # CANCEL = NameRequestActions.CANCEL.value
    # RECEIPT = NameRequestActions.RECEIPT.value
    # REAPPLY = NameRequestActions.REAPPLY.value
    RESEND = NameRequestActions.RESEND.value
