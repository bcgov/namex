export enum RequestActionCode {
  /** new request*/
  NEW = 'NEW',
  /** move request */
  MVE = 'MVE',
  /** restore or reinstate request */
  REH = 'REH',
  /** amalgamate request */
  AML = 'AML',
  /** change name request */
  CHG = 'CHG',
  /** conversion request */
  CNV = 'CNV',
  /** doing business as request */
  DBA = 'DBA',
  /** assumed name request */
  ASSUMED = 'ASSUMED',
  /** restore with new name request (renew) */
  REN = 'REN',
  /** special value for sub-menu */
  INFO = 'INFO',
  /** restore */
  REST = 'REST',
}

export enum RequestTypeCode {
  /** new request for a BC Company */
  CR = 'CR',
  /** amalgamation request for a BC.Company **NOT YET SUPPORTED EXTERNALLY** */
  ACR = 'ACR',
  /** new request for an Extra-provincial Corporation */
  XCR = 'XCR',
  /** amalgamation request for a Extra-provincial Corporation **NOT YET SUPPORTED EXTERNALLY** */
  XACR = 'XACR',
  /** new request for a Cooperative */
  CP = 'CP',
  /** amalgamation request for a Cooperative */
  ACP = 'ACP',
  /** new request for a CCC */
  CC = 'CC',
  /** amalgamation request for a CCC */
  ACC = 'ACC',
  /** new request for a Sole Prop */
  FR = 'FR',
  /** change of name request for a Sole Prop */
  CFR = 'CFR',
  /** new request for a general partnership */
  GP = 'GP',
  /** change of name request for a general partnership */
  CGP = 'CGP',
  /** B.C. Company - Change of Name */
  CCR = 'CCR',
  /** B.C. Company - Continuation In */
  CT = 'CT',
  /** B.C. Company - Restore */
  RCR = 'RCR',
  /** Corporation (Foreign) - Extraprovincial Change of Name */
  XCCR = 'XCCR',
  /** Corporation (Foreign) - Extraprovincial Reinstatement */
  XRCR = 'XRCR',
  /** Corporation (Foreign) - Extraprovincial Assumed Name */
  AS = 'AS',
  /** LLC - Extraprovincial Registration */
  LC = 'LC',
  /** LLC - Extraprovincial Change of Name */
  CLC = 'CLC',
  /** LLC - Extraprovincial Reinstatement */
  RLC = 'RLC',
  /** LLC - Extraprovincial Assumed Name */
  AL = 'AL',
  /** Limited Liability Partnership - Registration */
  LL = 'LL',
  /** Limited Liability Partnership - Change of Name */
  CLL = 'CLL',
  /** Limited Liability Partnership - Extraprovincial Registration */
  XLL = 'XLL',
  /** Limited Liability Partnership - Extraprovincial Change of Name */
  XCLL = 'XCLL',
  /** Limited Partnership - Registration */
  LP = 'LP',
  /** Limited Partnership - Change of Name */
  CLP = 'CLP',
  /** Extraprovincial Limited Partnership */
  XLP = 'XLP',
  /** Limited Partnership - Extraprovincial Change of Name */
  XCLP = 'XCLP',
  /** Society - Incorporation */
  SO = 'SO',
  /** Society - Amalgamation */
  ASO = 'ASO',
  /** Society - Change of Name */
  CSO = 'CSO',
  /** Society - Restore */
  RSO = 'RSO',
  /** Society - Continuation In */
  CTSO = 'CTSO',
  /** Society - Extraprovincial */
  XSO = 'XSO',
  /** Society - Extraprovincial Change of Name */
  XCSO = 'XCSO',
  /** Society - Extraprovincial Restoration */
  XRSO = 'XRSO',
  /** Society - Extraprovincial Non-Share Corporation Assumed Name */
  XASO = 'XASO',
  /** Society - Extraprovincial Non-Share Corporation Change Assumed Name */
  XCASO = 'XCASO',
  /** Society - Conversion of a Special Act */
  CSSO = 'CSSO',
  /** Cooperative - Change of Name */
  CCP = 'CCP',
  /** Cooperative - Continuation In */
  CTC = 'CTC',
  /** Cooperative - Restore */
  RCP = 'RCP',
  /** Cooperative - Extraprovincial */
  XCP = 'XCP',
  /** Cooperative - Extraprovincial Change of Name */
  XCCP = 'XCCP',
  /** Cooperative - Extraprovincial Restoration */
  XRCP = 'XRCP',
  /** CCC - BC to CCC Conversion */
  CCV = 'CCV',
  /** CCC - Change of Name */
  CCC = 'CCC',
  /** CCC - Continuation In */
  CCCT = 'CCCT',
  /** CCC - Restore */
  RCC = 'RCC',
  /** Unlimited Liability Company */
  UL = 'UL',
  /** BC to Unlimited Liability Company Conversion */
  UC = 'UC',
  /** Change of Name of Unlimited Liability Company */
  CUL = 'CUL',
  /** ULC - Continuation In */
  ULCT = 'ULCT',
  /** ULC - Restore */
  RUL = 'RUL',
  /** ULC - Extraprovincial Assumed Name */
  UA = 'UA',
  /** ULC - Extraprovincial Registration */
  XUL = 'XUL',
  /** Change of Name of Extrapro Unlimited Liability Company */
  XCUL = 'XCUL',
  /** ULC - Extraprovincial Reinstatement */
  XRUL = 'XRUL',
  /** Financial Institution (BC) - Incorporation */
  FI = 'FI',
  /** Financial Institution (BC) - Change of Name */
  CFI = 'CFI',
  /** Financial Institution (BC) - Restore */
  RFI = 'RFI',
  /** Private Act */
  PA = 'PA',
  /** Cemetery */
  CEM = 'CEM',
  /** Library */
  LIB = 'LIB',
  /** NON */
  NON = 'NON',
  /** Parish */
  PAR = 'PAR',
  /** Railway */
  RLY = 'RLY',
  /** Tramway */
  TMY = 'TMY',
  /** BC Benefit Company - Incorporation */
  BC = 'BC',
  /** BC Benefit Company - Amalgamation */
  BEAM = 'BEAM',
  /** BC Benefit Company - Change of Name */
  BEC = 'BEC',
  /** BC Benefit Company - Continuation In */
  BECT = 'BECT',
  /** BC Benefit Company - Restoration */
  BERE = 'BERE',
  /** BC Benefit Company - BC to Benefit Conversion */
  BECV = 'BECV',
  /** BC Benefit Company - Community Contribution Company Conversion */
  BECC = 'BECC',
  /** Unlimited Liability Company - BC Limited Conversion */
  ULCB = 'ULCB',
  /** Unlimited Liability Company - Benefit Company Conversion */
  ULBE = 'ULBE',
  /** BC Benefit Company - Benefit to BC Conversion */
  BECR = 'BECR',
}

export enum EntityTypeCode {
  /** General Partnership */
  GP = 'GP',
  CR = 'CR',
  XCR = 'XCR',
  RLC = 'RLC',
  FR = 'FR',
  LL = 'LL',
  XLL = 'XLL',
  LP = 'LP',
  XLP = 'XLP',
  CP = 'CP',
  XCP = 'XCP',
  CC = 'CC',
  UL = 'UL',
  UC = 'UC',
  XUL = 'XUL',
  FI = 'FI',
  PA = 'PA',
  PAR = 'PAR',
  BC = 'BC',
  BECV = 'BECV',
  BECR = 'BECR',
}

export enum ClassTypeCode {
  CORP = 'CORP',
  FIRM = 'FIRM',
  MISC = 'MISC',
}

export enum RefundStatus {
  Refunded = 'REFUNDED',
  Credited = 'CREDITED',
  Cancelled = 'CANCELLED',
  RefundRequested = 'REFUND_REQUESTED',
}

export enum RefundMessage {
  Requested = 'Refund has been requested',
  NotProcessed = 'Refund not processed',
  Processed = 'Refund request processed',
  Cancelled = 'Payment cancelled',
  Credited = 'Funds have been credited',
  Completed = 'Refund process is completed',
}

export enum PaymentMethod {
  Pad = 'PAD',
  Internal = 'INTERNAL',
  DirectPay = 'DIRECT_PAY',
  DrawDown = 'DRAWDOWN',
}

export enum ConsentFlag {
  Required = 'Y',
  Received = 'R',
  Waived = 'N',
}
