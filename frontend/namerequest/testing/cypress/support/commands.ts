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

import LoginProxy from '../pageObjects/loginProxy'

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

    cy.get('#loginBtn').click().then(() => {
      cy.get('div[role="menu"', { timeout: 1000 }).within(() => {
          cy.contains('div', 'IDIR').click();
      });

      cy.setid('default').then(() => {
          // Validate siteminder and login
          cy.get('#login-to', { timeout: 10000 })
              .contains('Log in to ')
              .should('be.visible')
          cy.get('#user', { timeout: 10000 }).type(
              Cypress.env('username')
          )
          cy.get('#password', { timeout: 10000 }).type(
              Cypress.env('password'),
              { log: false }
          )

          cy.get('div.login-form-action > input', { timeout: 10000 }).click()
          cy.wait(3000)
      });
    });
  }
)

/**
 * Custom Cypress command to perform logout.
 */
Cypress.Commands.add('logout', () => {
  // Make sure you are on page with log out and logout
  cy.get('button.user-account-btn').click().then(() => {
    cy.contains('div', 'Log out').click();
  })
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
    const href = link.prop('href');
    if (href) {
      cy.request({
        url: href,
        failOnStatusCode: false,
      }).then((response) => {
        expect(response.status).to.eq(200);
        cy.log(link.prop('innerText') + ': ' + href);
      })
    }
  })
})
