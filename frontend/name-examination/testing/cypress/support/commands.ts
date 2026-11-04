/**
 * This file contains custom Cypress commands used in the tests.
 */

/// <reference types="@testing-library/cypress" />

/**
 * Making common libraries available to the scripts
 */
import 'cypress-plugin-api'
import 'cypress-real-events'
import '@testing-library/cypress/add-commands'

import HomePage from '../pageObjects/homePage'
import SearchPage from '../pageObjects/searchPage'
import LoginProxy from '../pageObjects/loginProxy'

const homePage = new HomePage()
const searchPage = new SearchPage()
const loginProxy = new LoginProxy()

/**
 * Custom Cypress command to perform login.
 *
 * @param username - The username for login. If not provided, it uses the value from Cypress environment variables.
 * @param password - The password for login. If not provided, it uses the value from Cypress environment variables.
 * @param host - The host URL to visit. If not provided, it uses an empty string.
 * @param siteminder - The Siteminder value. Not used in the code.
 */
Cypress.Commands.add(
  'login',
  (
    username?: string,
    password?: string,
    host?: string,
    siteminder?: string
  ) => {
    // Go to the host
    cy.visit(host || '')

    loginProxy.checkLoginProxyPage()
    loginProxy.chooseIdir()

    // Validate siteminder and login
    cy.get('#login-to')
      .contains('Log in to ')
      .should('be.visible')
    cy.get('#user').type(
      username || Cypress.env('username')
    )
    cy.get('#password').type(
      password || Cypress.env('password'),
      { log: false }
    )
    cy.get('input[name=btnSubmit]').click()
  }
)


/**
 * Custom Cypress command to perform logout.
 */
Cypress.Commands.add('logout', () => {
  // If an error popup panel exists, close it.
  cy.get('body').then(($body) => {
    if ($body.find(homePage.popupPanel).length) {
      cy.get(homePage.popupPanel).find('button').contains('Close').click({ force: true })
      cy.wait(3000)
    }
  })

  // Proceed with logout.
  cy.get(homePage.logOut).should('be.visible').click({ force: true })
  cy.clearCookies()
  cy.clearLocalStorage()
})


/**
 * Custom Cypress command to set the ID/PW Env vars.
 *
 * @param type - The type of ID/PW to set. If not provided, it uses the default type.
 */
Cypress.Commands.add('setid', (type: string) => {
  // Set the ID/PW Env vars to default if type not passed in
  if (!type) {
    type = 'default'
  }
  const data = Cypress.env('users')
  const foundItem = data.find((item: any) => item.type === type)
  Cypress.env('username', foundItem.username)
  Cypress.env('password', foundItem.password)
  Cypress.env('type', foundItem.type)
  if (foundItem.otpsecret) {
    Cypress.env('otpsecret', foundItem.otpsecret)
  }
})


/**
 * Custom Cypress command to clean up memory by triggering Garbage Collection.
 */
Cypress.Commands.add('cleanGC', () => {
  // Clean up memory by triggering Garbage Collection
  cy.window().then((win) => {
    // window.gc is enabled with --js-flags=--expose-gc chrome flag
    if (typeof win.gc === 'function') {
      // run gc multiple times in an attempt to force a major GC between tests
      win.gc()
      win.gc()
      win.gc()
      win.gc()
      win.gc()
    }
  })
})


/**
 * Custom Cypress command to check all links on the page.
 */
Cypress.Commands.add('linkChecker', () => {
  cy.get('a').each((link) => {
    if (
      link.prop('href') &&
      link.prop('href').startsWith('mailto', 0) === false
    ) {
      cy.request({
        url: link.prop('href'),
        failOnStatusCode: false,
      }).as('links')
    }

    cy.get('@links').should((response) => {
      expect((response as any).status).to.eq(200)
    })

    // Log the link text and the url. This is useful for debugging.
    cy.log(link.prop('innerText') + ': ' + link.prop('href'))
  })
})


/**
 * Custom Cypress command to wait until loading spinner is gone.
 */
Cypress.Commands.add('waitForSpinner', () => {
  cy.get('[data-testid="loadingSpinner"]', { timeout: 30000 }).should('not.exist')
})


/**
 * Custom Cypress command to verify the contents of an input element's text.
 *
 * @param selector - The selector for the text element.
 * @param expectedText - The text the selected element is to be compared with. .
 */
Cypress.Commands.add('verifyTextContent', (selector: string, expectedText: string) => {
  cy.get(selector).invoke('text').then((text) => {
    expect(text.trim()).to.eq(expectedText)
  })
})


/**
 * Custom Cypress command to type the contents of text into an input element.
 *
 * @param selector - The selector for the input element.
 * @param text - The text to type into the input element.
 */
Cypress.Commands.add('typeInField', (selector: string, text: string) => {
  cy.get(selector)
    .click()
    .clear()
    .type(text)
})


/**
 * Custom Cypress command to verify the state of an NR with a given state.
 * This command searches the search table with the given state and confirms
 * the NR exists.
 *
 * @param nrNum - The NR number of the NR to verify.
 * @param state - The state the NR number is to be verified with.
 */
Cypress.Commands.add('verifyNRState', (nrNum: string, state: string) => {
  homePage.searchLink()
  searchPage.headerRowDropdownSelect(searchPage.headerRowStatus, state)
  cy.waitForSpinner()

  cy.get(searchPage.searchTable).within(() => {
    cy.get(searchPage.headerRowNRNumber).type(nrNum + '{enter}')
    cy.waitForSpinner()
    cy.contains('td', nrNum).should('exist')
  })
})
