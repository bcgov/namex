import Utilities from '../appActions/Utilities'
const util = new Utilities()

/**
 * Represents the home page of the BC Registry Name Examination application.
 */
class HomePage {
  path = '/'
  title = 'BC Registry: Name Examination - Home'

  // Error Popup panel
  popupPanel = 'div[data-testid="popupPanel"]'

  // Top Level Links
  homeLinkID = 'a[data-testid="homeLink"]'
  adminLinkID = 'a[data-testid="adminLink"]'
  examineLinkID = 'a[data-testid="examineLink"]'
  searchLinkID = 'a[data-testid="searchLink"]'
  statsLinkID = 'a[data-testid="statsLink"]'

  // Link bar
  searchInputField = 'form[data-testid="searchNRNumberField"] input'
  searchButton = 'form[data-testid="searchNRNumberField"] button'
  prioritySwitch = 'div[data-testid="prioritySwitch"] button[role="switch"]'
  logOut = 'a[data-testid="logOut"]'

  // Status info
  displayDate = 'span[data-testid="displayDate"]'
  notExamined = 'span[data-testid="notExamined"]'
  hold = 'span[data-testid="numHold"]'

  /**
   * Retrieves the status information from the home page.
   */
  statusInfo() {
    cy.get(this.displayDate).should('exist')
    cy.get(this.notExamined).should('exist')
    cy.get(this.hold).should('exist')
    cy.get(this.displayDate)
      .invoke('text')
      .then(($text) => {
        const date = util.getDate()
        expect($text.trim()).to.include(date)
        cy.log($text)
      })
    }

  /**
   * Navigates to the home page by clicking the NameX Icon in the header.
   */
  homeLink() {
    cy.intercept('GET', '**/api/v1/requests*').as('homeLinkRequest')
    cy.get(this.homeLinkID).should('be.visible').click( { force: true } )
    cy.wait('@homeLinkRequest').its('response.statusCode').should('eq', 200)
    cy.url().should('eq', Cypress.config().baseUrl + '/')
  }

  /**
   * Navigates to the admin page by clicking the "Admin" link.
   */
  adminLink() {
    // Remove the target to stay in the same window for Cypress' sake.
    cy.get(this.adminLinkID).should('be.visible').invoke('removeAttr', 'target').click()
    cy.url().should('include', 'namex-solr-dev.apps.silver.devops.gov.bc.ca')
    cy.contains('a', 'Login to administration.').click()
    cy.url().then(($url) => {
      expect($url).to.contain('/admin/synonym')
    })
    cy.visit('/')
  }

  /**
   * Navigates to the examine names page by clicking the "Examine Names" link.
   */
  examineNamesLink() {
    cy.intercept('GET', '**/api/v1/requests/NR*').as('examineGetRequest')
    cy.get(this.examineLinkID).should('be.visible').click( { force: true } )
    cy.wait('@examineGetRequest').its('response.statusCode').should('eq', 200)
    cy.waitForSpinner()
    cy.url().should('include', '/examine')
  }

  /**
   * Navigates to the search page by clicking the "Search" link.
   */
  searchLink() {
    cy.intercept('GET', '**/api/v1/requests?*').as('searchGetRequest')
    cy.get(this.searchLinkID).should('be.visible').click({ force: true })
    cy.wait('@searchGetRequest').its('response.statusCode').should('eq', 200)
    cy.waitForSpinner()
    cy.url().should('include', '/search')
  }

  /**
   * Navigates to the stats page by clicking the "Stats" link.
   */
  statsLink() {
    cy.get(this.statsLinkID).should('be.visible').click({ force: true })
    cy.waitForSpinner()
    cy.url().should('include', '/stats')
  }

  /**
   * Toggles the priority switch by clicking on it.
   */
  prioritySwitchClick() {
    cy.get(this.prioritySwitch)
      .invoke('attr', 'aria-checked')
      .then((checked) => {
        cy.get(this.prioritySwitch).click()

        if (checked === 'true') {
          cy.get(this.prioritySwitch)
            .invoke('attr', 'aria-checked')
            .should('eq', 'false')
        } else {
          cy.get(this.prioritySwitch)
            .invoke('attr', 'aria-checked')
            .should('eq', 'true')
        }
      })
  }

  /**
   * Sets the value of the priority queue.
   *
   * @param value - The value that the queue will be set to.
   */
  setPrioritySwitch(value: boolean) {
    cy.get(this.prioritySwitch)
      .invoke('attr', 'aria-checked')
      .then((checked) => {
        const shouldBeChecked = value ? 'true' : 'false'

        if (checked !== shouldBeChecked) {
          cy.get(this.prioritySwitch)
            .should('be.visible')
            .click({ force: true })

          cy.get(this.prioritySwitch)
            .invoke('attr', 'aria-checked')
            .should('eq', shouldBeChecked)
        }
      })
  }
}

export default HomePage
