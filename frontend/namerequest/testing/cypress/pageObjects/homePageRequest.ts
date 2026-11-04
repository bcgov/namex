/**
 * Represents the home page of the BC Registry Name Request application.
 */

import Utilities from '../appActions/Utilities'
const util = new Utilities()

/**
 * Represents the home page of the BC Registry Name Examination application.
 */
class HomePage {
  url = 'https://test.names.bcregistry.gov.bc.ca'
  path = '/'
  title = 'Name Request'

  affiliationErrorDialog = '#affiliation-error-dialog'
  appTitle = '#app-title'
  app = '#app'
  appHeader = '#appHeader'
  breadcrumbBackBtn = '#breadcrumb-back-btn'
  breadcrumb = '#breadcrumb'
  dummyInputBox = '#dummy-input-box'
  exampleName = '#example-name'
  existingTab = '#existing-tab'
/*   input-55 = '#input-55'
  input-59 = '#input-59' */
  landingContainer = '#landing-container'
  linkRow = '#link-row'
  loginBtn = '#loginBtn'
  lowerContainer = '#lower-container'
  lowerRow = '#lower-row'
  mainColumn = '#main-column'
  mrasSearchInfoModal = '#mras-search-info-modal'
  nameBuildInfo = '#name-build-info'
  namerequestSbcHeader = '#namerequest-sbc-header'
  newandBetterWay = '#new-and-better-way'
  newTab = '#new-tab'
  requestActionSelect = '#request-action-select'
  requestAction = '#request-action'
  searchContainer = '#search-container'
  statsContentOuter3 = '#stats-content-outer-3'
  tabsLandingComp = '#tabs-landing-comp'
  upperRow = '#upper-row'
  vuetifyThemeStylesheet = '#vuetify-theme-stylesheet'
  warningBar = '#warning-bar'
  warningModal = '#warning-modal'
}
export default HomePage
