import Utilities from '../appActions/Utilities'
const util = new Utilities()

/**
 * Represents the transactions page of the BC Registry Name Examination application.
 */
class TransactionsPage {
  path = '/transactions'
  title = 'BC Registry: Name Examination - Transactions'

  showSystemTransactionsCheckbox = 'input[data-testid="showSystemTransactionsCheckbox"]'
  transactionEntry = 'div[data-testid="transactionEntry"]'

  /**
   * Sets the value of the show system transactions checkbox.
   *
   * @param value - The value that the checkbox will be set to.
   */
  setSystemTransactionsCheckBox(value: boolean) {
    cy.get(this.showSystemTransactionsCheckbox)
      .then($checkbox => {
        if ($checkbox.prop('checked') !== value) {
          cy.wrap($checkbox)
            .should('be.visible')
            .click({ force: true })
        }
        cy.wrap($checkbox).should('have.prop', 'checked', value)
      })
  }
}

export default TransactionsPage
