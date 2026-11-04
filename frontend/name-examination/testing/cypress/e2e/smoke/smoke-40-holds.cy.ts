// Cypress Test: Check for ability to put NRs on hold.
// This spec checks that an NR can be put on hold.
import HomePage from 'cypress/pageObjects/homePage'
import SearchPage from 'cypress/pageObjects/searchPage'
import ExaminePage from 'cypress/pageObjects/examinePage'
import { NRState } from 'cypress/constants'
const homePage = new HomePage()
const searchPage = new SearchPage()
const examinePage = new ExaminePage()

describe('Check that putting NRs on hold works', () => {
  beforeEach(() => {
    cy.cleanGC()
    cy.setid('default')
    cy.login()
  })

  afterEach(() => {
    cy.logout()
  })


  it('Should be able to hold a NR from the Search Table', () => {
    // Get the first draft NR from the search table.
    homePage.searchLink()
    searchPage.clickAndRetrieveFirstNR(NRState.Draft)
    cy.get(examinePage.nrStatus).should('have.text', NRState.Draft)

    // Examine the NR.
    examinePage.clickExamineButton()
    cy.get(examinePage.nrStatus).should('have.text', NRState.InProgress)

    // Hold the NR.
    examinePage.clickHoldButton()

    // Verify Hold.
    cy.get(examinePage.nrStatus).should('have.text', NRState.Hold)
    cy.get('@nrNum').then((nrNum) => {
      cy.verifyNRState(nrNum.toString(), NRState.Hold)
    })
  })
})
