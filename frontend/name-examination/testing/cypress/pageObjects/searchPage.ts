import Utilities from '../appActions/Utilities'
const util = new Utilities()

/**
 * Represents the search page of the BC Registry Name Examination application.
 */
class SearchPage {
  path = '/search'
  title = 'BC Registry: Name Examination - Search Name Requests'

  searchTable = '[data-testid="searchTable"]'
  headerRowStatus = 'th[id="status"] button'
  headerRowNRNumber = '#nrnumber input'
  headerRowApplicantFirstName = 'input[type="text"][id="applicantfirstname"]'
  headerRowApplicantLastName = 'input[type="text"][id="applicantlastname"]'
  headerRowModifiedBy = 'input[type="text"][id="modifiedby"]'
  headerRowNames = 'input[type="text"][id="names"]'
  headerRowConsentRequired = 'th[id="consentrequired"] button'
  headerRowPriority = 'th[id="priority"] button'
  headerRowNotified = 'th[id="notified"] button'
  headerRowSubmitted = 'th[id="submitted"] button'
  headerRowLastUpdate = 'th[id="lastupdate"] button'
  headerRowSubmittedOrder = 'a[id="submittedOrder"]'

  /**
   * Selects an option from a dropdown in the header row.
   *
   * @param dropDown - The selector for the dropdown element.
   * @param option - The text of the option to select.
   */
  headerRowDropdownSelect(dropDown: string, option: string) {
    cy.get(dropDown)
      .click()
      .then(() => {
        cy.get('[role="listbox"]')
          .find(`[role="option"]:contains(${option})`)
          .eq(0) // Select the first option that matches
          .click()
      })
    }

  /**
   * Selects the first NR from the search table with the specified state.
   * Also stores the NR number as 'nrNum' for later use.
   *
   * @param state - The state of the NR desired (Draft, Hold, etc.).
   */
  clickAndRetrieveFirstNR(state: string) {
    // Select the appropriate filter.
    this.headerRowDropdownSelect(this.headerRowStatus, state)
    cy.waitForSpinner()

    // Select the first one, store the NR number, and wait for the request to complete.
    cy.intercept('GET', '**/api/v1/requests/NR*').as('searchGetRequest')
    cy.get(this.searchTable).within(() => {
      cy.get('tbody tr:first-child td:nth-child(3) a')
        .should('be.visible')
        .invoke('text')
        .should('not.be.empty')
        .then((text) => {
          cy.wrap(text.trim()).as('nrNum')
        })
      cy.get('tbody tr:first-child td:nth-child(3) a').click({ force: true })
    })
    cy.wait('@searchGetRequest').its('response.statusCode').should('eq', 200)
    cy.waitForSpinner()
    cy.wait(1000)
  }
}

export default SearchPage
