// this config is required because Namerequest UI
// uses a different Prod key than the other UIs
const canadaPostAPIKeyDev = 'RH99-RN99-GB72-FW86'
const canadaPostAPIKeyProd = 'EU13-YA15-YH65-GX49'

export default import.meta.env.NODE_ENV === 'development' ? canadaPostAPIKeyDev : canadaPostAPIKeyProd
