// Cypress Test: Check for Broken Interactions.
// This spec checks for broken links on the home page, examine page, and search page.
// It also checks basic functionalities such as searching for an NR.
import HomePage from 'cypress/pageObjects/homePage'
import SearchPage from 'cypress/pageObjects/searchPage'
import ExaminePage from 'cypress/pageObjects/examinePage'
import StatsPage from 'cypress/pageObjects/statsPage'
import TransactionsPage from 'cypress/pageObjects/transactionsPage'
import { NRState, SearchFilter } from 'cypress/constants'
const homePage = new HomePage()
const searchPage = new SearchPage()
const examinePage = new ExaminePage()
const statsPage = new StatsPage()
const transactionsPage = new TransactionsPage()

describe('Check for Link Integrity and Core UI Interactions', () => {
  beforeEach(() => {
    cy.cleanGC()
    cy.setid('default')
    cy.login()
  })

  afterEach(() => {
    cy.logout()
  })


  it('Check the static links of the home, examine, and search pages', () => {
    // Iterate through all the links on the home page, examine page, and search page.
    // If the link has a specified URL, check if the link is operational.
    // Does not check if the links are correct.
    cy.linkChecker()

    homePage.examineNamesLink()
    cy.linkChecker()

    homePage.searchLink()
    cy.linkChecker()
  })


  it('Should be able to click the links/items in the header', () => {
    homePage.adminLink()
    homePage.examineNamesLink()
    homePage.searchLink()
    homePage.statsLink()
    homePage.prioritySwitchClick()
  })


  it('Should have status info available on the home page', () => {
    homePage.statusInfo()
  })


  it('Should be able to see the stats on the stats page', () => {
    homePage.statsLink()

    statsPage.setMyStatsCheckBox(false)
    statsPage.setHoursFilterText(50)
    cy.get(statsPage.getStatsButton).click({ force: true })
    cy.waitForSpinner()

    cy.get(statsPage.statsTable)
      .find('tr')
      .then((row) => {
        cy.wrap({ len: row.length }).its('len').should('greaterThan', 0)
      })
  })


  it('Should be able to see the transactions on the transactions page', () => {
    homePage.examineNamesLink()
    examinePage.clickTransactionsLink()

    transactionsPage.setSystemTransactionsCheckBox(true)
    cy.get(transactionsPage.transactionEntry).should('have.length.at.least', 1)
    cy.visit('/')
  })


  it('Should be able to search for an NR in the Search Box', () => {
    const nrNum = '3351228'

    // Enter the NR in the search box.
    cy.get(homePage.searchInputField).should('exist')
    .then(($input) => {
      cy.wrap($input).type(nrNum, { force: true })}
    )

    // Search for the NR.
    cy.intercept('GET', '**/api/v1/requests/NR*').as('searchGetRequest')
    cy.get(homePage.searchButton).should('exist').click({ force: true })
    cy.wait('@searchGetRequest').its('response.statusCode').should('eq', 200)

    cy.contains(examinePage.nrNumberHeader, nrNum).should('exist')
  })


  it('Should be able to search for an NR in the Search Table', () => {
    const nrNum = '3351228'

    // Go to the search page and change the submitted order.
    homePage.searchLink()
    cy.get(searchPage.headerRowSubmittedOrder).click({ force: true })

    // Test all the drop downs.
    searchPage.headerRowDropdownSelect(searchPage.headerRowStatus, NRState.Draft)
    searchPage.headerRowDropdownSelect(searchPage.headerRowConsentRequired, SearchFilter.All)
    searchPage.headerRowDropdownSelect(searchPage.headerRowPriority, SearchFilter.Standard)
    searchPage.headerRowDropdownSelect(searchPage.headerRowNotified, SearchFilter.Notified)
    searchPage.headerRowDropdownSelect(searchPage.headerRowSubmitted, SearchFilter.OneYear)
    searchPage.headerRowDropdownSelect(searchPage.headerRowLastUpdate, SearchFilter.Today)
    searchPage.headerRowDropdownSelect(searchPage.headerRowConsentRequired, SearchFilter.All)
    searchPage.headerRowDropdownSelect(searchPage.headerRowPriority, SearchFilter.All)
    searchPage.headerRowDropdownSelect(searchPage.headerRowNotified, SearchFilter.All)
    searchPage.headerRowDropdownSelect(searchPage.headerRowSubmitted, SearchFilter.All)
    searchPage.headerRowDropdownSelect(searchPage.headerRowLastUpdate, SearchFilter.All)

    // Search for the NR.
    cy.get(searchPage.searchTable).within(() => {
      cy.get(searchPage.headerRowNRNumber).type(nrNum + '{enter}')
      cy.contains('td', 'NR ' + nrNum).should('exist')
      cy.contains('td a', 'NR ' + nrNum).click()
      cy.url().should('include', '/examine?nr=' + nrNum)
    })

    cy.contains(examinePage.nrNumberHeader, nrNum).should('exist')
  })
})
