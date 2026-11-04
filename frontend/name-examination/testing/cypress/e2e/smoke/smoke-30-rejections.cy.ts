// Cypress Test: Check for ability to reject NRs.
// This spec checks that NRs can be rejected with the rejection button,
// quick reject distinctive button, and quick reject descriptive button.
import HomePage from 'cypress/pageObjects/homePage'
import SearchPage from 'cypress/pageObjects/searchPage'
import ExaminePage from 'cypress/pageObjects/examinePage'
import { NRState, DecisionText } from 'cypress/constants'
const homePage = new HomePage()
const searchPage = new SearchPage()
const examinePage = new ExaminePage()
const nameChoices = [
  examinePage.choice1Txt,
  examinePage.choice2Txt,
  examinePage.choice3Txt,
]

describe('Check that rejecting NRs works', () => {
  beforeEach(() => {
    cy.cleanGC()
    cy.setid('default')
    cy.login()
  })

  afterEach(() => {
    cy.logout()
  })


  it('Should be able to reject a NR from the Search Table', () => {
    // Get the first draft NR from the search table.
    homePage.searchLink()
    searchPage.clickAndRetrieveFirstNR(NRState.Draft)
    cy.get(examinePage.nrStatus).should('have.text', NRState.Draft)

    // Examine the NR.
    examinePage.clickExamineButton()
    cy.get(examinePage.nrStatus).should('have.text', NRState.InProgress)

    // Reject the NR (all 3 choices if available).
    nameChoices.forEach((choice, i) => {
      cy.get(choice, { timeout: 0 }).then($el => {
        if ($el.is(':visible')) {
          examinePage.clickRejectButton()
          cy.get(examinePage[`choice${i + 1}XMark`]).should('be.visible')
        }
      })
    })

    // Verify Rejection.
    cy.get(examinePage.nrStatus).should('have.text', NRState.Rejected)
    cy.get('@nrNum').then((nrNum) => {
      cy.verifyNRState(nrNum.toString(), NRState.Rejected)
    })
  })


  it('Should be able to reject a NR with the Quick Reject Distinctive button', () => {
    // Get the first NR from the Examine Names button.
    homePage.examineNamesLink()
    examinePage.retrieveCurrentNr()
    cy.get(examinePage.nrStatus).should('have.text', NRState.InProgress)

    // Reject the NR (all 3 choices if available).
    nameChoices.forEach((choice, i) => {
      cy.get(choice, { timeout: 0 }).then($el => {
        if ($el.is(':visible')) {
          examinePage.clickQuickRejectDistButton()
          cy.get(examinePage[`choice${i + 1}XMark`]).should('be.visible')
          cy.get(examinePage[`choice${i + 1}DecisionTxt`])
            .invoke('text')
            .should('eq', DecisionText.RejectDist)
        }
      })
    })

    // Verify rejection.
    cy.get(examinePage.nrStatus).should('have.text', NRState.Rejected)
    cy.get('@nrNum').then((nrNum) => {
      cy.verifyNRState(nrNum.toString(), NRState.Rejected)
    })
  })


  it('Should be able to reject a NR with the Quick Reject Descriptive button', () => {
    // Get the first NR from the Examine Names button.
    homePage.examineNamesLink()
    examinePage.retrieveCurrentNr()
    cy.get(examinePage.nrStatus).should('have.text', NRState.InProgress)

    // Reject the NR (all 3 choices if available).
    nameChoices.forEach((choice, i) => {
      cy.get(choice, { timeout: 0 }).then($el => {
        if ($el.is(':visible')) {
          examinePage.clickQuickRejectDescButton()
          cy.get(examinePage[`choice${i + 1}XMark`]).should('be.visible')
          cy.get(examinePage[`choice${i + 1}DecisionTxt`])
            .invoke('text')
            .should('eq', DecisionText.RejectDesc)
        }
      })
    })

    // Verify rejection.
    cy.get(examinePage.nrStatus).should('have.text', NRState.Rejected)
    cy.get('@nrNum').then((nrNum) => {
      cy.verifyNRState(nrNum.toString(), NRState.Rejected)
    })
  })
})
