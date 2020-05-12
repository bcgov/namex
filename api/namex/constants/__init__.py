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


# TODO: Confirm that this is correct!
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


# Not a 'todo', just a note for later - these probably correlate to some JSON schemas in the LEAR project
# bcgov/lear/schemas/src/registry_schemas/schemas for namerequest schema
class BCProtectedNameEntityTypes(AbstractEnum):
    CORPORATION = 'CR'
    UNLIMITED_LIABILITY_COMPANY = 'UL'


class BCUnprotectedNameEntityTypes(AbstractEnum):
    SOLE_PROPRIETORSHIP = 'FR'
    DOING_BUSINESS_AS = 'DBA'
    GENERAL_PARTNERSHIP = 'GP'
    LIMITED_PARTNERSHIP = 'LP'
    LIMITED_LIABILITY_PARTNERSHIP = 'LL'


class XproUnprotectedNameEntityTypes(AbstractEnum):
    XPRO_CORPORATION = 'XCR'
    XPRO_UNLIMITED_LIABILITY_COMPANY = 'XUL'
    XPRO_LIMITED_LIABILITY_COMPANY = 'RLC'
    XPRO_LIMITED_PARTNERSHIP = 'XLP'
    XPRO_LIMITED_LIABILITY_PARTNERSHIP = 'XLL'


# TODO: Refactor this, use code enum KEYS as described in BCProtectedNameEntityTypes, etc.
#  When complete, merge with EntityTypes, above...
# Entity Types derived from the legacy request_type
class EntityType(Enum):
    # BC Types
    BCORP = 'CR'
    ULC = 'UL'
    SP = 'FR'
    GP = 'GP'
    DBA = 'DBA'
    LP = 'LP'
    LLP = 'LL'
    CP = 'CP'
    BC = 'BC'
    CCC = 'CC'
    SO = 'SO'
    PRIV = 'PA'
    FI = 'FI'
    PAR = 'PAR'
    # XPRO and Foreign Types
    XCORP = 'XCR'
    XULC = 'XUL'
    XLLC = 'RLC'
    XLP = 'XLP'
    XLLP = 'XLL'
    XCP = 'XCP'
    XSO = 'XSO'
    # legacy
    FIRM = 'FIRM'


# Request types (legacy) used in search conflicts
class EntityTypeBCORP(AbstractEnum):
    CCR = 'CCR'
    CT = 'CT'
    RCR = 'RCR'


class EntityTypeULC(AbstractEnum):
    UC = 'UC'
    CUL = 'CUL'
    ULCT = 'ULCT'
    RUL = 'RUL'


class EntityTypeCP(AbstractEnum):
    CCP = 'CCP'
    CTC = 'CTC'
    RCP = 'RCP'


class EntityTypeCCC(AbstractEnum):
    CCV = 'CCV'
    CC = 'CCC'
    CCCT = 'CCCT'
    RCC = 'RCC'


class EntityTypeSO(AbstractEnum):
    ASO = 'ASO'
    CSO = 'CSO'
    RSO = 'RSO'
    CTSO = 'CTSO'
    CSSO = 'CSSO'


class EntityTypeFI(AbstractEnum):
    CFI = 'CFI'
    RFI = 'RFI'


class EntityTypeXCORP(AbstractEnum):
    XCCR = 'XCCR'
    XRCR = 'XRCR'
    AS = 'AS'


class EntityTypeXULC(AbstractEnum):
    UA = 'UA'
    XCUL = 'XCUL'
    XRUL = 'XRUL'


class EntityTypeXCP(AbstractEnum):
    XCCP = 'XCCP'
    XRCP = 'XRCP'


class EntityTypeXSO(AbstractEnum):
    XCSO = 'XCSO'
    XRSO = 'XRSO'
    XASO = 'XASO'
    XCASO = 'XCASO'


request_type_mapping = [
    ('CR', EntityType.BCORP.value, RequestAction.NEW_AML.value),
    ('CR', EntityType.BCORP.value, RequestAction.NEW.value),
    ('CCR', EntityType.BCORP.value, RequestAction.CHG.value),
    ('CT', EntityType.BCORP.value, RequestAction.MVE.value),
    ('RCR', EntityType.BCORP.value, RequestAction.REST.value),
    ('XCR', EntityType.XCORP.value, RequestAction.NEW.value),
    ('XCCR', EntityType.XCORP.value, RequestAction.CHG.value),
    ('XRCR', EntityType.XCORP.value, RequestAction.REST.value),
    ('AS', EntityType.XCORP.value, RequestAction.AS.value),
    ('LC', EntityType.XLLC.value, RequestAction.NEW.value),
    ('CLC', EntityType.XLLC.value, RequestAction.CHG.value),
    ('RLC', EntityType.XLLC.value, RequestAction.REST.value),
    ('AL', EntityType.XLLC.value, RequestAction.AS.value),
    ('FR', EntityType.FIRM.value, RequestAction.NEW.value),
    ('CFR', EntityType.FIRM.value, RequestAction.CHG.value),
    ('LL', EntityType.LLP.value, RequestAction.NEW.value),
    ('CLL', EntityType.LLP.value, RequestAction.CHG.value),
    ('XLL', EntityType.XLLP.value, RequestAction.NEW.value),
    ('XCLL', EntityType.XLLP.value, RequestAction.CHG.value),
    ('LP', EntityType.LP.value, RequestAction.NEW.value),
    ('CLP', EntityType.LP.value, RequestAction.CHG.value),
    ('XLP', EntityType.XLP.value, RequestAction.NEW.value),
    ('CXLP', EntityType.XLP.value, RequestAction.CHG.value),
    ('SO', EntityType.SO.value, RequestAction.NEW.value),
    ('ASO', EntityType.SO.value, RequestAction.AML.value),
    ('CSO', EntityType.SO.value, RequestAction.CHG.value),
    ('RSO', EntityType.SO.value, RequestAction.REST.value),
    ('CTSO', EntityType.SO.value, RequestAction.MVE.value),
    ('CSSO', EntityType.SO.value, RequestAction.CNV.value),
    ('XSO', EntityType.XSO.value, RequestAction.NEW.value),
    ('XCSO', EntityType.XSO.value, RequestAction.CHG.value),
    ('XRSO', EntityType.XSO.value, RequestAction.REST.value),
    ('XASO', EntityType.XSO.value, RequestAction.AS.value),
    ('XCASO', EntityType.XSO.value, RequestAction.ACHG.value),
    ('CP', EntityType.CP.value, RequestAction.NEW_AML.value),
    ('CCP', EntityType.CP.value, RequestAction.CHG.value),
    ('CTC', EntityType.CP.value, RequestAction.MVE.value),
    ('RCP', EntityType.CP.value, RequestAction.REST.value),
    ('XCP', EntityType.XCP.value, RequestAction.NEW.value),
    ('XCCP', EntityType.XCP.value, RequestAction.CHG.value),
    ('XRCP', EntityType.XCP.value, RequestAction.REST.value),
    ('CC', EntityType.CCC.value, RequestAction.NEW_AML.value),
    ('CCV', EntityType.CCC.value, RequestAction.CNV.value),
    ('CCC', EntityType.CCC.value, RequestAction.CHG.value),
    ('CCCT', EntityType.CCC.value, RequestAction.MVE.value),
    ('RCC', EntityType.CCC.value, RequestAction.REST.value),
    ('UL', EntityType.ULC.value, RequestAction.NEW.value),
    ('UC', EntityType.ULC.value, RequestAction.CNV.value),
    ('CUL', EntityType.ULC.value, RequestAction.CHG.value),
    ('ULCT', EntityType.ULC.value, RequestAction.MVE.value),
    ('RUL', EntityType.ULC.value, RequestAction.REST.value),
    ('UA', EntityType.XULC.value, RequestAction.AS.value),
    ('XUL', EntityType.XULC.value, RequestAction.NEW.value),
    ('XCUL', EntityType.XULC.value, RequestAction.CHG.value),
    ('XRUL', EntityType.XULC.value, RequestAction.REST.value),
    ('FI', EntityType.FI.value, RequestAction.NEW.value),
    ('CFI', EntityType.FI.value, RequestAction.CHG.value),
    ('RFI', EntityType.FI.value, RequestAction.REST.value),
    ('PA', EntityType.PRIV.value, RequestAction.NEW.value),
    ('PAR', EntityType.PAR.value, RequestAction.NEW.value),
    ('BC',  EntityType.BC.value, RequestAction.NEW.value)
]
