import Utilities from '../appActions/Utilities'
const util = new Utilities()

/**
 * Represents the stats page of the BC Registry Name Examination application.
 */
class StatsPage {
  path = '/stats'
  title = 'BC Registry: Name Examination'

  hoursTextInput = 'input[data-testid="statsHoursInput"]'
  statsCheckbox = 'input[data-testid="statsCheckbox"]'
  getStatsButton = 'button[data-testid="getStatsBtn"]'
  statsTable = '[data-testid="statsTable"]'

  /**
   * Sets the value of the show my stats checkbox.
   *
   * @param value - The value that the checkbox will be set to.
   */
  setMyStatsCheckBox(value: boolean) {
    cy.get(this.statsCheckbox)
      .then($checkbox => {
        if ($checkbox.prop('checked') !== value) {
          cy.wrap($checkbox)
            .should('be.visible')
            .click({ force: true })
        }
        cy.wrap($checkbox).should('have.prop', 'checked', value)
      })
  }

  /**
   * Sets the value of the hours filter for the stats table.
   *
   * @param numHours - The value that the filter will be set to.
   */
  setHoursFilterText(numHours: number) {
    cy.get(this.hoursTextInput)
    .click()
    .clear()
    .type(String(numHours))
  }
}

export default StatsPage
