from enum import Enum

# Modes
MODE_SYNS = 'Syns'
MODE_SUBS = 'Subs'
MODE_STOP = 'Stop'

# Categories
dsg_end = 'Designations_end'
dsg_any = 'Designations_any'
stop_w = 'Stop Words'

DATE_FORMAT_NAMEX_SEARCH = '%Y-%m-%d'
DATE_TIME_FORMAT_SQL = '%Y-%m-%d %H:%M:%S%z'

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
    RESUBMIT = 'RESUBMIT'
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
    FINANCIAL_INSTITUTION = EntityTypes.FINANCIAL_INSTITUTION.value
    PRIVATE_ACT = EntityTypes.PRIVATE_ACT.value
    PARISH = EntityTypes.PARISH.value
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
    ('CR', EntityTypes.CORPORATION.value, RequestAction.RESUBMIT.value),
    ('CCR', EntityTypes.CORPORATION.value, RequestAction.CHG.value, True),
    ('CCR', EntityTypes.CORPORATION.value, RequestAction.RESUBMIT.value),
    ('CT', EntityTypes.CORPORATION.value, RequestAction.MVE.value, True),
    ('CT', EntityTypes.CORPORATION.value, RequestAction.RESUBMIT.value),
    ('RCR', EntityTypes.CORPORATION.value, RequestAction.REST.value, True),
    ('RCR', EntityTypes.CORPORATION.value, RequestAction.REH.value),
    ('RCR', EntityTypes.CORPORATION.value, RequestAction.REN.value),
    ('RCR', EntityTypes.CORPORATION.value, RequestAction.RESUBMIT.value),
    ('XCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.NEW_AML.value, True),
    ('XCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.NEW.value),
    ('XCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.AML.value),
    ('XCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.RESUBMIT.value),
    ('XCCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.CHG.value, True),
    ('XCCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.RESUBMIT.value),
    ('XRCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.REST.value, True),
    ('XRCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.REH.value),
    ('XRCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.REN.value),
    ('XRCR', EntityTypes.XPRO_CORPORATION.value, RequestAction.RESUBMIT.value),
    ('AS', EntityTypes.XPRO_CORPORATION.value, RequestAction.AS.value, True),
    ('AS', EntityTypes.XPRO_CORPORATION.value, RequestAction.RESUBMIT.value),
    ('LC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.NEW.value, True),
    ('LC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('CLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.CHG.value, True),
    ('CLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('RLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.REST.value, True),
    ('RLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.REN.value),
    ('RLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.REH.value),
    ('RLC', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('AL', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.AS.value, True),
    ('AL', EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('FR', EntityTypes.FIRM.value, RequestAction.NEW.value, True),
    ('FR', EntityTypes.SOLE_PROPRIETORSHIP.value, RequestAction.NEW.value),
    ('FR', EntityTypes.DOING_BUSINESS_AS.value, RequestAction.NEW.value),
    ('FR', EntityTypes.GENERAL_PARTNERSHIP.value, RequestAction.NEW.value),
    ('FR', EntityTypes.GENERAL_PARTNERSHIP.value, RequestAction.RESUBMIT.value),
    ('CFR', EntityTypes.SOLE_PROPRIETORSHIP.value, RequestAction.CHG.value, True),
    ('CFR', EntityTypes.GENERAL_PARTNERSHIP.value, RequestAction.CHG.value),
    ('CFR', EntityTypes.DOING_BUSINESS_AS.value, RequestAction.CHG.value),
    ('CFR', EntityTypes.DOING_BUSINESS_AS.value, RequestAction.RESUBMIT.value),
    ('LL', EntityTypes.LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.NEW.value, True),
    ('LL', EntityTypes.LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.RESUBMIT.value),
    ('CLL', EntityTypes.LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.CHG.value, True),
    ('CLL', EntityTypes.LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.RESUBMIT.value),
    ('XLL', EntityTypes.XPRO_LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.NEW.value, True),
    ('XLL', EntityTypes.XPRO_LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.RESUBMIT.value),
    ('XCLL', EntityTypes.XPRO_LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.CHG.value, True),
    ('XCLL', EntityTypes.XPRO_LIMITED_LIABILITY_PARTNERSHIP.value, RequestAction.RESUBMIT.value),
    ('LP', EntityTypes.LIMITED_PARTNERSHIP.value, RequestAction.NEW.value, True),
    ('LP', EntityTypes.LIMITED_PARTNERSHIP.value, RequestAction.RESUBMIT.value),
    ('CLP', EntityTypes.LIMITED_PARTNERSHIP.value, RequestAction.CHG.value, True),
    ('CLP', EntityTypes.LIMITED_PARTNERSHIP.value, RequestAction.RESUBMIT.value),
    ('XLP', EntityTypes.XPRO_LIMITED_PARTNERSHIP.value, RequestAction.NEW.value, True),
    ('XLP', EntityTypes.XPRO_LIMITED_PARTNERSHIP.value, RequestAction.RESUBMIT.value),
    ('XCLP', EntityTypes.XPRO_LIMITED_PARTNERSHIP.value, RequestAction.CHG.value, True),
    ('XCLP', EntityTypes.XPRO_LIMITED_PARTNERSHIP.value, RequestAction.RESUBMIT.value),
    ('SO', EntityTypes.SOCIETY.value, RequestAction.NEW.value, True),
    ('SO', EntityTypes.SOCIETY.value, RequestAction.RESUBMIT.value),
    ('ASO', EntityTypes.SOCIETY.value, RequestAction.AML.value, True),
    ('ASO', EntityTypes.SOCIETY.value, RequestAction.RESUBMIT.value),
    ('CSO', EntityTypes.SOCIETY.value, RequestAction.CHG.value, True),
    ('CSO', EntityTypes.SOCIETY.value, RequestAction.RESUBMIT.value),
    ('RSO', EntityTypes.SOCIETY.value, RequestAction.REST.value, True),
    ('RSO', EntityTypes.SOCIETY.value, RequestAction.REN.value),
    ('RSO', EntityTypes.SOCIETY.value, RequestAction.REH.value),
    ('RSO', EntityTypes.SOCIETY.value, RequestAction.RESUBMIT.value),
    ('CTSO', EntityTypes.SOCIETY.value, RequestAction.MVE.value, True),
    ('CTSO', EntityTypes.SOCIETY.value, RequestAction.RESUBMIT.value),
    ('CSSO', EntityTypes.SOCIETY.value, RequestAction.CNV.value, True),
    ('CSSO', EntityTypes.SOCIETY.value, RequestAction.RESUBMIT.value),
    ('XSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.NEW.value, True),
    ('XSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.RESUBMIT.value),
    ('XCSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.CHG.value, True),
    ('XCSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.RESUBMIT.value),
    ('XRSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.REST.value, True),
    ('XRSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.REH.value),
    ('XRSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.REN.value),
    ('XRSO', EntityTypes.XPRO_SOCIETY.value, RequestAction.RESUBMIT.value),
    ('XASO', EntityTypes.XPRO_SOCIETY.value, RequestAction.AS.value, True),
    ('XASO', EntityTypes.XPRO_SOCIETY.value, RequestAction.RESUBMIT.value),
    ('XCASO', EntityTypes.XPRO_SOCIETY.value, RequestAction.ACHG.value, True),
    ('XCASO', EntityTypes.XPRO_SOCIETY.value, RequestAction.RESUBMIT.value),
    ('CP', EntityTypes.COOPERATIVE.value, RequestAction.NEW_AML.value, True),
    ('CP', EntityTypes.COOPERATIVE.value, RequestAction.NEW.value),
    ('CP', EntityTypes.COOPERATIVE.value, RequestAction.AML.value),
    ('CP', EntityTypes.COOPERATIVE.value, RequestAction.RESUBMIT.value),
    ('CCP', EntityTypes.COOPERATIVE.value, RequestAction.CHG.value, True),
    ('CCP', EntityTypes.COOPERATIVE.value, RequestAction.RESUBMIT.value),
    ('CTC', EntityTypes.COOPERATIVE.value, RequestAction.MVE.value, True),
    ('CTC', EntityTypes.COOPERATIVE.value, RequestAction.RESUBMIT.value),
    ('RCP', EntityTypes.COOPERATIVE.value, RequestAction.REST.value, True),
    ('RCP', EntityTypes.COOPERATIVE.value, RequestAction.REH.value),
    ('RCP', EntityTypes.COOPERATIVE.value, RequestAction.REN.value),
    ('RCP', EntityTypes.COOPERATIVE.value, RequestAction.RESUBMIT.value),
    ('XCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.NEW_AML.value, True),
    ('XCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.NEW.value),
    ('XCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.AML.value),
    ('XCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.RESUBMIT.value),
    ('XCCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.CHG.value, True),
    ('XCCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.RESUBMIT.value),
    ('XRCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.REST.value, True),
    ('XRCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.REH.value),
    ('XRCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.REN.value),
    ('XRCP', EntityTypes.XPRO_COOPERATIVE.value, RequestAction.RESUBMIT.value),
    ('CC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.NEW_AML.value, True),
    ('CC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.NEW.value),
    ('CC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.AML.value),
    ('CC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.RESUBMIT.value),
    ('CCV', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.CNV.value, True),
    ('CCV', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.RESUBMIT.value),
    ('CCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.CHG.value, True),
    ('CCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.RESUBMIT.value),
    ('CCCT', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.MVE.value, True),
    ('CCCT', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.RESUBMIT.value),
    ('RCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.REST.value, True),
    ('RCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.REH.value),
    ('RCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.REN.value),
    ('RCC', EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value, RequestAction.RESUBMIT.value),
    ('UL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.NEW.value, True),
    ('UL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.AML.value),
    ('UL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('UC', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.CNV.value, True),
    ('UC', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('CUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.CHG.value, True),
    ('ULCT', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.MVE.value, True),
    ('ULCT', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('RUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REST.value, True),
    ('RUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REH.value),
    ('RUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REN.value),
    ('RUL', EntityTypes.UNLIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('UA', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.AS.value, True),
    ('UA', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('XUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.NEW_AML.value, True),
    ('XUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.NEW.value),
    ('XUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.AML.value),
    ('XUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('XCUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.CHG.value, True),
    ('XCUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('XRUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REST.value, True),
    ('XRUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REH.value),
    ('XRUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.REN.value),
    ('XRUL', EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value, RequestAction.RESUBMIT.value),
    ('FI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.NEW.value, True),
    ('FI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.RESUBMIT.value),
    ('CFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.CHG.value, True),
    ('CFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.RESUBMIT.value),
    ('RFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.REST.value, True),
    ('RFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.REH.value),
    ('RFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.REN.value),
    ('RFI', EntityTypes.FINANCIAL_INSTITUTION.value, RequestAction.RESUBMIT.value),
    ('PA', EntityTypes.PRIVATE_ACT.value, RequestAction.NEW.value, True),
    ('PA', EntityTypes.PRIVATE_ACT.value, RequestAction.RESUBMIT.value),
    ('PAR', EntityTypes.PARISH.value, RequestAction.NEW.value, True),
    ('PAR', EntityTypes.PARISH.value, RequestAction.RESUBMIT.value),
    ('BC', EntityTypes.BENEFIT_COMPANY.value, RequestAction.NEW.value, True),
    ('BC', EntityTypes.BENEFIT_COMPANY.value, RequestAction.RESUBMIT.value),
    ('BEAM', EntityTypes.BENEFIT_COMPANY.value, RequestAction.AML.value, True),
    ('BEAM', EntityTypes.BENEFIT_COMPANY.value, RequestAction.RESUBMIT.value),
    ('BEC', EntityTypes.BENEFIT_COMPANY.value, RequestAction.CHG.value, True),
    ('BEC', EntityTypes.BENEFIT_COMPANY.value, RequestAction.RESUBMIT.value),
    ('BECT', EntityTypes.BENEFIT_COMPANY.value, RequestAction.MVE.value, True),
    ('BECT', EntityTypes.BENEFIT_COMPANY.value, RequestAction.RESUBMIT.value),
    ('BERE', EntityTypes.BENEFIT_COMPANY.value, RequestAction.REST.value, True),
    ('BERE', EntityTypes.BENEFIT_COMPANY.value, RequestAction.REH.value),
    ('BERE', EntityTypes.BENEFIT_COMPANY.value, RequestAction.REN.value),
    ('BERE', EntityTypes.BENEFIT_COMPANY.value, RequestAction.RESUBMIT.value),
    ('BECV', EntityTypes.BENEFIT_COMPANY.value, RequestAction.CNV.value, True),
    ('BECV', EntityTypes.BENEFIT_COMPANY.value, RequestAction.RESUBMIT.value),
    ('ULBE', EntityTypes.BENEFIT_COMPANY.value, RequestAction.CNV.value, True),
    ('ULBE', EntityTypes.BENEFIT_COMPANY.value, RequestAction.RESUBMIT.value),
    ('BECR', EntityTypes.CORPORATION.value, RequestAction.CNV.value, True),
    ('BECR', EntityTypes.CORPORATION.value, RequestAction.RESUBMIT.value),
    ('ULCB', EntityTypes.CORPORATION.value, RequestAction.CNV.value, True),
    ('ULCB', EntityTypes.CORPORATION.value, RequestAction.RESUBMIT.value)
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
    # Non-payment related actions
    CHECKOUT = 'CHECKOUT'
    CHECKIN = 'CHECKIN'
    EDIT = 'EDIT'
    CANCEL = 'CANCEL'
    RESEND = 'RESEND'
    INCORPORATE = 'INCORPORATE'
    # Payment related actions
    UPGRADE = 'UPGRADE'
    REAPPLY = 'REAPPLY' # FUTURE: replace by 'RENEW' - used when the NR is about to expire
    RESUBMIT = 'RESUBMIT' # Used when the NR is already expired
    RECEIPT = 'RECEIPT'
    CREATE = 'CREATE'
    REQUEST_REFUND = 'REQUEST_REFUND'
    RETRY_PAYMENT = 'RETRY_PAYMENT'
    RESULT = 'RESULT'


class NameRequestPatchActions(AbstractEnum):
    """
    This subset of actions is used by the NameRequest PATCH,
    and are NOT payment related.
    """
    CHECKOUT = NameRequestActions.CHECKOUT.value
    CHECKIN = NameRequestActions.CHECKIN.value
    EDIT = NameRequestActions.EDIT.value
    CANCEL = NameRequestActions.CANCEL.value
    RESEND = NameRequestActions.RESEND.value
    REQUEST_REFUND = NameRequestActions.REQUEST_REFUND.value


class NameRequestPaymentActions(AbstractEnum):
    """
    This subset of actions is used by the NameRequest PATCH,
    and are NOT payment related.
    """
    UPGRADE = NameRequestActions.UPGRADE.value
    REAPPLY = NameRequestActions.REAPPLY.value
    RECEIPT = NameRequestActions.RECEIPT.value
    COMPLETE = NameRequestActions.CREATE.value
    REQUEST_REFUND = NameRequestActions.REQUEST_REFUND.value
    CANCEL = NameRequestActions.CANCEL.value


class NameRequestPendingPaymentActions(AbstractEnum):
    # CANCEL = NameRequestActions.CANCEL.value  # TODO: Ensure there is NO refund for this!
    RETRY_PAYMENT = NameRequestActions.RETRY_PAYMENT.value


class NameRequestDraftActions(AbstractEnum):
    EDIT = NameRequestActions.EDIT.value
    UPGRADE = NameRequestActions.UPGRADE.value
    RECEIPT = NameRequestActions.RECEIPT.value
    REQUEST_REFUND = NameRequestActions.REQUEST_REFUND.value


class NameRequestActiveActions(AbstractEnum):
    """
    Actions available when an NR is 'active' eg. in an APPROVED or CONDITIONAL state, NOT expired, and NOT consumed.
    """
    #EDIT = NameRequestActions.EDIT.value
    CANCEL = NameRequestActions.CANCEL.value  # TODO: Ensure there is NO refund for this!
    REAPPLY = NameRequestActions.REAPPLY.value
    RESUBMIT = NameRequestActions.RESUBMIT.value
    RECEIPT = NameRequestActions.RECEIPT.value
    RESULT = NameRequestActions.RESULT.value
    # RESEND = NameRequestActions.RESEND.value


class NameRequestReservedActions(AbstractEnum):
    pass


class NameRequestHoldActions(AbstractEnum):
    RECEIPT = NameRequestActions.RECEIPT.value


class NameRequestInProgressActions(AbstractEnum):
    """
    These should mostly be the same as the ones for a draft, but they are used differently.
    Define these separately.
    """
    RECEIPT = NameRequestActions.RECEIPT.value


class NameRequestExpiredActions(AbstractEnum):
    """
    Actions available when an NR is in an APPROVED or CONDITIONAL state, expired, and NOT consumed.
    """
    RECEIPT = NameRequestActions.RECEIPT.value
    RESULT = NameRequestActions.RESULT.value
    RESUBMIT = NameRequestActions.RESUBMIT.value
    # RESEND = NameRequestActions.RESEND.value


class NameRequestConsumedActions(AbstractEnum):
    """Actions available when an NR is in an CONSUMED state."""
    #EDIT = NameRequestActions.EDIT.value
    RECEIPT = NameRequestActions.RECEIPT.value
    RESULT = NameRequestActions.RESULT.value


class NameRequestHistoricalActions(AbstractEnum):
    # TODO: Check to make sure there is a valid payment ID before returning this action
    RECEIPT = NameRequestActions.RECEIPT.value


class NameRequestCancelledActions(AbstractEnum):
    RECEIPT = NameRequestActions.RECEIPT.value


class NameRequestCompletedActions(AbstractEnum):
    RECEIPT = NameRequestActions.RECEIPT.value


class NameRequestActiveRejectedActions(AbstractEnum):
    #EDIT = NameRequestActions.EDIT.value  # TODO: Can only EDIT contact info
    RECEIPT = NameRequestActions.RECEIPT.value
    RESULT = NameRequestActions.RESULT.value
    # RESEND = NameRequestActions.RESEND.value


class NameRequestExpiredRejectedActions(AbstractEnum):
    #EDIT = NameRequestActions.EDIT.value  # TODO: Can only EDIT contact info
    RECEIPT = NameRequestActions.RECEIPT.value
    RESULT = NameRequestActions.RESULT.value
    # RESEND = NameRequestActions.RESEND.value


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
    Payment status code mappings for SBC Pay this is separate from PaymentState, as the codes that come back from
    SBC Pay are subject to change so we map the values instead of using the SBC Pay statuses internally.
    There are also certain differences - on our side we track when a refund is requested, which does not mean a refund
    has been issued as on the SBC Pay side, for example (there are other cases too).
    """
    APPROVED = 'APPROVED'
    CREATED = 'CREATED'
    COMPLETED = 'COMPLETED'
    PARTIAL = 'PARTIAL'
    FAILED = 'FAILED'
    REFUNDED = 'REFUNDED'
    CANCELLED = 'CANCELLED'


# TODO: Confirm these statuses!
class PaymentState(AbstractEnum):
    """
    Internal PaymentState codes for Payment model.
    """
    APPROVED = 'APPROVED'
    CREATED = 'CREATED'  # A payment has been created
    PENDING = 'PENDING'  # A newly created Payment
    INPROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    PARTIAL = 'PARTIAL'
    FAILED = 'FAILED'
    REFUND_REQUESTED = 'REFUND_REQUESTED'
    CANCELLED = 'CANCELLED'


class PaymentAction(AbstractEnum):
    """
    Payment actions.
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

class ExpiryDays(str, AbstractEnum):
    NAME_REQUEST_LIFESPAN_DAYS = 56
    NAME_REQUEST_REH_REN_LIFESPAN_DAYS = 421
