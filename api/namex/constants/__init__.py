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

        # Indicates the source application

class ValidSources(Enum):
    NAMEX = 'NAMEX'
    NAMEREQUEST = 'NAMEREQUEST'
    NRO = 'NRO'
    SO = 'SO'

# Request Action for name request and namex (includes legacy)
class RequestAction(Enum):
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

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values


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

    @classmethod
    def list(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values

# Request types (legacy) used in search conflicts
class EntityTypeBCORP(Enum):
    CCR = 'CCR'
    CT = 'CT'
    RCR = 'RCR'


class EntityTypeULC(Enum):
    UC = 'UC'
    CUL = 'CUL'
    ULCT = 'ULCT'
    RUL = 'RUL'



class EntityTypeCP(Enum):
    CCP = 'CCP'
    CTC = 'CTC'
    RCP = 'RCP'

class EntityTypeCCC(Enum):
    CCV = 'CCV'
    CC = 'CCC'
    CCCT = 'CCCT'
    RCC = 'RCC'

class EntityTypeSO(Enum):
     ASO = 'ASO'
     CSO = 'CSO'
     RSO = 'RSO'
     CTSO = 'CTSO'
     CSSO = 'CSSO'

class EntityTypeFI(Enum):
     CFI = 'CFI'
     RFI = 'RFI'

class EntityTypeXCORP(Enum):
     XCCR = 'XCCR'
     XRCR = 'XRCR'
     AS = 'AS'

class EntityTypeXULC(Enum):
     UA = 'UA'
     XCUL = 'XCUL'
     XRUL = 'XRUL'

class EntityTypeXCP(Enum):
     XCCP = 'XCCP'
     XRCP = 'XRCP'

class EntityTypeXSO(Enum):
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
            ('PAR', EntityType.PAR.value, RequestAction.NEW.value)
        ]
