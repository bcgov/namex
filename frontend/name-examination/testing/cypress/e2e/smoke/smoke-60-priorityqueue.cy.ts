// Cypress Test: Check for ability of priority queue to work as expected.
// This spec checks that the priority queue properly grabs NRs of the correct
// priority from both the Examine Names button and the Get Next button.
import HomePage from 'cypress/pageObjects/homePage'
import ExaminePage from 'cypress/pageObjects/examinePage'
import { NRState } from 'cypress/constants'
const homePage = new HomePage()
const examinePage = new ExaminePage()

describe('Check that the priority queue works', () => {
  beforeEach(() => {
    cy.cleanGC()
    cy.setid('default')
    cy.login()
  })

  afterEach(() => {
    cy.logout()
  })

  it('should correctly select a priority or non-priority NR using the examine names button', () => {
    // Examine a nmae in case there is alreay one in progress
    homePage.examineNamesLink()
    cy.get(examinePage.nrStatus).should('have.text', NRState.InProgress)
    examinePage.clickHoldButton()
    cy.get(examinePage.nrStatus).should('have.text', NRState.Hold)

    // Go back to the home page
    homePage.homeLink()

    // Turn the priority queue off, fetch NR using examine names button, and verify
    homePage.setPrioritySwitch(false)
    homePage.examineNamesLink()
    cy.get(examinePage.nrStatus).should('have.text', NRState.InProgress)
    cy.get(examinePage.priorityLabel).should('not.exist')
    examinePage.clickHoldButton()
    cy.get(examinePage.nrStatus).should('have.text', NRState.Hold)

    // Go back to the home page
    homePage.homeLink()

    // Turn the priority queue on, fetch NR using the examine names button, and verify
    homePage.setPrioritySwitch(true)
    homePage.examineNamesLink()
    cy.get(examinePage.nrStatus).should('have.text', NRState.InProgress)
    cy.get(examinePage.priorityLabel).should('be.visible')
    examinePage.clickHoldButton()
    cy.get(examinePage.nrStatus).should('have.text', NRState.Hold)
  })

  it('should correctly select a priority or non-priority NR using the get next button', () => {
    // Examine a nmae in case there is alreay one in progress
    homePage.examineNamesLink()
    cy.get(examinePage.nrStatus).should('have.text', NRState.InProgress)
    examinePage.clickHoldButton()
    cy.get(examinePage.nrStatus).should('have.text', NRState.Hold)

    // Test with priority queue off
    homePage.setPrioritySwitch(false)
    for (let i = 0; i < 2; i++) {
      examinePage.clickNextButton()
      cy.get(examinePage.nrStatus).should('have.text', NRState.InProgress)
      cy.get(examinePage.priorityLabel).should('not.exist')
      examinePage.clickHoldButton()
      cy.get(examinePage.nrStatus).should('have.text', NRState.Hold)
    }

    // Test with priority queue on
    homePage.setPrioritySwitch(true)
    for (let i = 0; i < 2; i++) {
      examinePage.clickNextButton()
      cy.get(examinePage.nrStatus).should('have.text', NRState.InProgress)
      cy.get(examinePage.priorityLabel).should('be.visible')
      examinePage.clickHoldButton()
      cy.get(examinePage.nrStatus).should('have.text', NRState.Hold)
    }
  })
})
