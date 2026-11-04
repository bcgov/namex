/**
 * Represents the Login Proxy page object.
 */
class LoginProxy {
  path = '/'

  idirButton = '#social-idir' // Define the IDIR button selector
  azidirButton = '#social-azureidir'
  headerWrapper = '#kc-header-wrapper'
  headerText = 'bcregistry'

  /**
   * Check the Login Proxy page.
   */
  checkLoginProxyPage() {
    cy.get(this.headerWrapper).contains(this.headerText).should('be.visible')
  }

  /**
   * Choose IDIR authentication.
   */
  chooseIdir() {
    cy.get(this.idirButton).click()
  }

  /**
   * Choose Azure IDIR authentication.
   */
  chooseAzIdir() {
    cy.get(this.azidirButton).click()
  }
}

export default LoginProxy
