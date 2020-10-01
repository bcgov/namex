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
    ('CR', EntityTypes.CORPORATION.value, RequestAction.NEW_AML.value, True),
    ('CR', EntityTypes.CORPORATION.value, RequestAction.NEW.value),
    ('CR', EntityTypes.CORPORATION.value, RequestAction.AML.value),
    ('CCR', EntityTypes.CORPORATION.value, RequestAction.CHG.value, True),
    ('CT', EntityTypes.CORPORATION.value, RequestAction.MVE.value, True),
    ('RCR', EntityTypes.CORPORATION.value, RequestAction.REST.value, True),
    ('RCR', EntityTypes.CORPORATION.value, RequestAction.REH.value),
    ('RCR', EntityTypes.CORPORATION.value, RequestAction.REN.value),
    ('XCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.NEW_AML.value, True),
    ('XCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.NEW.value),
    ('XCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.AML.value),
    ('XCCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.CHG.value, True),
    ('XRCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.REST.value, True),
    ('XRCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.REH.value),
    ('XRCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.REN.value),
    ('AS', EntityTypes.XPRO_CORPORATION.value, RequestAction.AS.value, True),
    ('LC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.NEW.value, True),
    ('CLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.CHG.value, True),
    ('RLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.REST.value, True),
    ('RLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.REN.value),
    ('RLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.REH.value),
    ('AL', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.AS.value, True),
    ('FR', EntityTypes.FIRM.value, RequestAction.NEW.value, True),
    ('FR', EntityTypes.SOLE_PROPRIETORSHIP.value, RequestAction.NEW.value),
    ('FR', EntityTypes.DOING_BUSINESS_AS.value, RequestAction.NEW.value),
    ('FR', EntityTypes.GENERAL_PARTNERSHIP.value, RequestAction.NEW.value),
    ('CFR', EntityTypes.SOLE_PROPRIETORSHIP.value, RequestAction.CHG.value, True),
    ('CFR', EntityTypes.GENERAL_PARTNERSHIP.value, RequestAction.CHG.value),
    ('CFR', EntityTypes.DOING_BUSINESS_AS.value, RequestAction.CHG.value),
    ('LL', EntityTypes.LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.NEW.value, True),
    ('CLL', EntityTypes.LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.CHG.value, True),
    ('XLL', EntityTypes.XPRO_LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.NEW.value, True),
    ('XCLL', EntityTypes.XPRO_LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.CHG.value, True),
    ('LP', EntityTypes.LIMITED_PARTNERSHIP.value, RequestAction.NEW.value, True),
    ('CLP', EntityTypes.LIMITED_PARTNERSHIP.value, RequestAction.CHG.value, True),
    ('XLP', EntityTypes.XPRO_LIMITED_PARTNERSHIP.value, RequestAction.NEW.value, True),
    ('XCLP', EntityTypes.XPRO_LIMITED_PARTNERSHIP.value, RequestAction.CHG.value, True),
    ('SO', EntityTypes.SOCIETY.value, RequestAction.NEW.value, True),
    ('ASO', EntityTypes.SOCIETY.value, RequestAction.AML.value, True),
    ('CSO', EntityTypes.SOCIETY.value, RequestAction.CHG.value, True),
    ('RSO', EntityTypes.SOCIETY.value, RequestAction.REST.value, True),
    ('RSO', EntityTypes.SOCIETY.value, RequestAction.REN.value),
    ('RSO', EntityTypes.SOCIETY.value, RequestAction.REH.value),
    ('CTSO', EntityTypes.SOCIETY.value, RequestAction.MVE.value, True),
    ('CSSO', EntityTypes.SOCIETY.value, RequestAction.CNV.value, True),
    ('XSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.NEW.value, True),
    ('XCSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.CHG.value, True),
    ('XRSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.REST.value, True),
    ('XRSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.REH.value),
    ('XRSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.REN.value),
    ('XASO', EntityTypes.XPRO_SOCIETY.value, RequestAction.AS.value, True),
    ('XCASO', EntityTypes.XPRO_SOCIETY.value, RequestAction.ACHG.value, True),
    ('CP', EntityTypes.COOPERATIVE.value, RequestAction.NEW_AML.value, True),
    ('CP', EntityTypes.COOPERATIVE.value, RequestAction.NEW.value),
    ('CP', EntityTypes.COOPERATIVE.value, RequestAction.AML.value),
    ('CCP', EntityTypes.COOPERATIVE.value, RequestAction.CHG.value, True),
    ('CTC', EntityTypes.COOPERATIVE.value, RequestAction.MVE.value, True),
    ('RCP', EntityTypes.COOPERATIVE.value, RequestAction.REST.value, True),
    ('RCP', EntityTypes.COOPERATIVE.value, RequestAction.REH.value),
    ('RCP', EntityTypes.COOPERATIVE.value, RequestAction.REN.value),
    ('XCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.NEW_AML.value, True),
    ('XCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.NEW.value),
    ('XCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.AML.value),
    ('XCCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.CHG.value, True),
    ('XRCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.REST.value, True),
    ('XRCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.REH.value),
    ('XRCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.REN.value),
    ('CC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.NEW_AML.value, True),
    ('CC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.NEW.value),
    ('CC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.AML.value),
    ('CCV', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.CNV.value, True),
    ('CCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.CHG.value, True),
    ('CCCT', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.MVE.value, True),
    ('RCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.REST.value, True),
    ('RCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.REH.value),
    ('RCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.REN.value),
    ('UL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.NEW.value, True),
    ('UL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.AML.value),
    ('UC', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.CNV.value, True),
    ('CUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.CHG.value, True),
    ('ULCT', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.MVE.value, True),
    ('RUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REST.value, True),
    ('RUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REH.value),
    ('RUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REN.value),
    ('UA', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.AS.value, True),
    ('XUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.NEW_AML.value, True),
    ('XUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.NEW.value),
    ('XUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.AML.value),
    ('XCUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.CHG.value, True),
    ('XRUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REST.value, True),
    ('XRUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REH.value),
    ('XRUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REN.value),
    ('FI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.NEW.value, True),
    ('CFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.CHG.value, True),
    ('RFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.REST.value, True),
    ('RFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.REH.value),
    ('RFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.REN.value),
    ('PA', EntityTypes.PRIVATE_ACT.value, RequestAction.NEW.value, True),
    ('PAR', EntityTypes.PARISH.value, RequestAction.NEW.value, True),
    ('BC', EntityTypes.BENEFIT_COMPANY.value, RequestAction.NEW.value, True),
    ('BEAM', EntityTypes.BENEFIT_COMPANY.value, RequestAction.AML.value, True),
    ('BEC', EntityTypes.BENEFIT_COMPANY.value, RequestAction.CHG.value, True),
    ('BECT', EntityTypes.BENEFIT_COMPANY.value, RequestAction.MVE.value, True),
    ('BERE', EntityTypes.BENEFIT_COMPANY.value, RequestAction.REST.value, True),
    ('BERE', EntityTypes.BENEFIT_COMPANY.value, RequestAction.REH.value),
    ('BERE', EntityTypes.BENEFIT_COMPANY.value, RequestAction.REN.value),
    ('BECV', EntityTypes.BENEFIT_COMPANY.value, RequestAction.CNV.value, True),
    ('BECR', EntityTypes.CORPORATION.value, RequestAction.CNV.value, True)
]

reverse_request_type_mapping = [m for m in request_type_mapping if len(m) == 4 and m[3] is True]


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
    REAPPLY = 'REAPPLY'
    RESEND = 'RESEND'  # Re-send notification
    COMPLETE = 'COMPLETE'


class NameRequestDraftActions(AbstractEnum):
    EDIT = NameRequestActions.EDIT.value
    UPGRADE = NameRequestActions.UPGRADE.value
    REFUND = NameRequestActions.REFUND.value
    RECEIPT = NameRequestActions.RECEIPT.value


class NameRequestActiveActions(AbstractEnum):
    """
    Actions available when an NR is 'active' eg. in an APPROVED or CONDITIONAL state, NOT expired, and NOT consumed.
    """
    EDIT = NameRequestActions.EDIT.value
    CANCEL = NameRequestActions.CANCEL.value  # TODO: Ensure there is NO refund for this!
    RECEIPT = NameRequestActions.RECEIPT.value
    REAPPLY = NameRequestActions.REAPPLY.value
    RESEND = NameRequestActions.RESEND.value


class NameRequestReservedActions(AbstractEnum):
    pass


class NameRequestHoldActions(AbstractEnum):
    pass


class NameRequestInProgressActions(AbstractEnum):
    pass


class NameRequestExpiredActions(AbstractEnum):
    """
    Actions available when an NR is in an APPROVED or CONDITIONAL state, expired, and NOT consumed.
    """
    EDIT = NameRequestActions.EDIT.value
    RECEIPT = NameRequestActions.RECEIPT.value
    RESEND = NameRequestActions.RESEND.value


class NameRequestConsumedActions(AbstractEnum):
    """
    Actions available when an NR is in an APPROVED or CONDITIONAL state, and consumed.
    """
    EDIT = NameRequestActions.EDIT.value  # TODO: Can only EDIT contact info
    RECEIPT = NameRequestActions.RECEIPT.value
    RESEND = NameRequestActions.RESEND.value


class NameRequestHistoricalActions(AbstractEnum):
    # TODO: Check to make sure there is a valid payment ID before returning this action
    RECEIPT = NameRequestActions.RECEIPT.value


class NameRequestCancelledActions(AbstractEnum):
    RECEIPT = NameRequestActions.RECEIPT.value


class NameRequestActiveRejectedActions(AbstractEnum):
    EDIT = NameRequestActions.EDIT.value  # TODO: Can only EDIT contact info
    RECEIPT = NameRequestActions.RECEIPT.value
    RESEND = NameRequestActions.RESEND.value


class NameRequestExpiredRejectedActions(AbstractEnum):
    EDIT = NameRequestActions.EDIT.value  # TODO: Can only EDIT contact info
    RECEIPT = NameRequestActions.RECEIPT.value
    RESEND = NameRequestActions.RESEND.value


class NameRequestRollbackActions(AbstractEnum):
    CANCEL = 'cancel'
    RESTORE_STATE = 'restore'  # TODO: Not implemented yet
    ROLLBACK_PAYMENT = 'rollback-payment'  # TODO: Not implemented yet


class NROChangeFlags(AbstractEnum):
    REQUEST = 'is_changed__request'
    PREV_REQ = 'is_changed__previous_request'
    APPLICANT = 'is_changed__applicant'
    NAME_1 = 'is_changed__name1'
    NAME_2 = 'is_changed__name2'
    NAME_3 = 'is_changed__name3'
    ADDRESS = 'is_changed__address'
    NWPTA_AB = 'is_changed__nwpta_ab'
    NWPTA_SK = 'is_changed__nwpta_sk'
    CONSENT = 'is_changed_consent'
    STATE = 'is_changed__request_state'


class EventState(AbstractEnum):
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CONDITIONAL = 'CONDITIONAL'
    CANCELLED = 'CANCELLED'


# TODO: Why are these the only states, also, although this is imported in the project nothing really uses it...
class RequestState(AbstractEnum):
    DRAFT = 'DRAFT'
    HOLD = 'HOLD'
    INPROGRESS = 'INPROGRESS'


class PaymentStatusCode(AbstractEnum):
    """
    Payment status code mappings for SBC Pay
    """
    DRAFT = 'DRAFT'
    INPROGRESS = 'IN_PROGRESS'
    CREATED = 'CREATED'
    COMPLETED = 'COMPLETED'
    PARTIAL = 'PARTIAL'
    FAILED = 'PARTIAL'
    REFUNDED = 'REFUNDED'
    CANCELLED = 'CANCELLED'


# TODO: Confirm these statuses!
class PaymentState(AbstractEnum):
    """
    Internal PaymentState codes for Payment model
    """
    CREATED = 'CREATED'  # A payment has been created
    PENDING = 'PENDING'  # A newly created Payment
    INPROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    PARTIAL = 'PARTIAL'
    FAILED = 'PARTIAL'
    REFUNDED = 'REFUNDED'
    CANCELLED = 'CANCELLED'


class PaymentAction(AbstractEnum):
    """
    Payment actions
    """
    COMPLETE_RESERVATION = 'COMPLETE_RESERVATION'
    COMPLETE_UPGRADE = 'COMPLETE_UPGRADE'


class EventAction(AbstractEnum):
    PUT = 'put'
    PATCH = 'patch'


class EventUserId(AbstractEnum):
    SERVICE_ACCOUNT = 86


class RequestPriority(AbstractEnum):
    Y = 'Y'
    N = 'N'
