/** These are request type codes for extraprovincial/assumed name companies. */
export enum XproNameType {
  /** Extraprovincial Limited Liability Company - Extraprovincial Assumed Name */
  AL = 'AL',

  /** Extraprovincial Registration (Foreign Corporation) - Extraprovincial Assumed Name */
  AS = 'AS',

  /** Extraprovincial Registration (Foreign Corporation) - Extraprovincial Name */
  CO = 'CO',

  /** Extraprovincial Unlimited Liability Company - for AS or RESUBMIT */
  UA = 'UA',

  /** (Legacy Type) Extraprovincial Society - for AS or RESUBMIT */
  XASO = 'XASO',

  /** (Legacy Type) Extraprovincial Society - for ACHG or RESUBMIT */
  XCASO = 'XCASO'
}
