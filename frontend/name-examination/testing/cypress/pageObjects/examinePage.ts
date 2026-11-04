import Utilities from '../appActions/Utilities'
const util = new Utilities()

/**
 * Represents the examine page of the BC Registry Name Examination application.
 */
class ExaminePage {
  path = '/examine'
  title = 'BC Registry: Name Examination'

  // Header and transactions link
  nrNumberHeader = 'div[data-testid="nrNumberHeader"]'
  openTransactionsLink = 'a[data-testid="openTransactionsLink"]'
  priorityLabel = 'p[data-testid="priorityLabel"]'

  // Action butttons
  actionNextBtn = 'button[data-testid="actionNextBtn"]'
  actionExamineBtn = 'button[data-testid="actionExamineBtn"]'
  actionHoldBtn = 'button[data-testid="actionHoldBtn"]'
  actionEditBtn = 'button[data-testid="actionEditBtn"]'
  actionCancelBtn = 'button[data-testid="actionCancelBtn"]'
  actionSaveBtn = 'button[data-testid="actionSaveBtn"]'
  actionShowDetailsBtn = 'button[data-testid="actionShowDetailsBtn"]'
  actionHideDetailsBtn = 'button[data-testid="actionHideDetailsBtn"]'

  // Quick Decision Buttons
  quickApproveBtn = 'button[data-testid="quickApproveBtn"]'
  quickRejectDistBtn = 'button[data-testid="quickRejectDistBtn"]'
  quickRejectDescBtn = 'button[data-testid="quickRejectDescBtn"]'

  // Bottom of page primary approval/ rejection Buttons
  primaryApproveBtn = 'button[data-testid="primaryApprovalBtn"]'
  primaryRejectBtn = 'button[data-testid="primaryRejectionBtn"]'

  // NR Information
  nrType = 'p[data-testid="nrType"]'
  nrStatus = 'p[data-testid="nrStatus"]'
  nrExaminer = 'p[data-testid="nrExaminer"]'
  submitDate = 'span[data-testid="submitDate"]'
  consumedDate = 'span[data-testid="consumedDate"]'
  expiryDate = 'span[data-testid="expiryDate"]'
  consumedBy = 'span[data-testid="consumedBy"]'
  additionalInfo = 'p[data-testid="additionalInfo"]'

  // Contact Information
  clientName = 'p[data-testid="clientName"]'
  applicantName = 'p[data-testid="applicantName"]'
  phone = 'p[data-testid="phone"]'
  fax = 'p[data-testid="fax"]'
  email = 'p[data-testid="email"]'
  contact = 'p[data-testid="contact"]'
  addressLine1 = 'p[data-testid="addressLine1"]'
  addressLine2 = 'p[data-testid="addressLine2"]'
  addressLine3 = 'p[data-testid="addressLine3"]'
  addressCityProvince = 'p[data-testid="addressCityProvince"]'
  addressPostalCode = 'p[data-testid="addressPostalCode"]'
  addressCountry = 'p[data-testid="addressCountry"]'

  // Names Choices Information
  choice1Txt = 'span[data-testid="choice1-text"]'
  choice2Txt = 'span[data-testid="choice2-text"]'
  choice3Txt = 'span[data-testid="choice3-text"]'
  choice1CheckMark = 'span[data-testid="choice1-checkmark"]'
  choice2CheckMark = 'span[data-testid="choice2-checkmark"]'
  choice3CheckMark = 'span[data-testid="choice3-checkmark"]'
  choice1XMark = 'span[data-testid="choice1-xmark"]'
  choice2XMark = 'span[data-testid="choice2-xmark"]'
  choice3XMark = 'span[data-testid="choice3-xmark"]'
  choice1DecisionTxt = 'span[data-testid="choice1-decisiontxt"]'
  choice2DecisionTxt = 'span[data-testid="choice2-decisiontxt"]'
  choice3DecisionTxt = 'span[data-testid="choice3-decisiontxt"]'

  // Comments
  commentsPopupBtn = 'button[data-testid="commentsPopupBtn"]'
  commentsContainer = 'div[data-testid="commentsContainer"]'

  // Decision Information
  consentCheckbox = 'input[data-testid="consentCheckbox"]'

  /******** Editing ********/

  // Edit NR Information
  editNRTypeDropdownBtn = 'button[data-testid="editCompanyTypeDropdown"]'
  editAdditionalInfoTxtBox = 'textarea[data-testid="editAdditionalInfoTxtBox"]'

  // Edit Contact Information
  editClientFirstNameText = 'input[data-testid="editClientFirstNameTxt"]'
  editClientLastNameText = 'input[data-testid="editClientLastNameTxt"]'
  editApplicantFirstNameText = 'input[data-testid="editApplicantFirstNameTxt"]'
  editApplicantMiddleNameText = 'input[data-testid="editApplicantMiddleNameTxt"]'
  editApplicantLastNameText = 'input[data-testid="editApplicantLastNameTxt"]'
  editApplicantPhoneText = 'input[data-testid="editApplicantPhoneTxt"]'
  editApplicantFaxText = 'input[data-testid="editApplicantFaxTxt"]'
  editApplicantEmailText = 'input[data-testid="editApplicantEmailTxt"]'
  editApplicantContactText = 'input[data-testid="editApplicantContactTxt"]'
  editApplicantAddressText1 = 'input[data-testid="editApplicantAddressTxt1"]'
  editApplicantAddressText2 = 'input[data-testid="editApplicantAddressTxt2"]'
  editApplicantAddressText3 = 'input[data-testid="editApplicantAddressTxt3"]'
  editApplicantCityText = 'input[data-testid="editApplicantCityTxt"]'
  editApplicantProvinceText = 'input[data-testid="editApplicantProvinceTxt"]'
  editApplicantPostalCodeText = 'input[data-testid="editApplicantPostalCodeTxt"]'
  editApplicantCountryText = 'input[data-testid="editApplicantCountryTxt"]'

  // Edit Names Choices Information
  editNameChoiceText1 = 'input[data-testid="editNameChoiceTxt1"]'
  editNameChoiceText2 = 'input[data-testid="editNameChoiceTxt2"]'
  editNameChoiceText3 = 'input[data-testid="editNameChoiceTxt3"]'

  // Edit Comments
  commentEditableTxtBox = 'textarea[data-testid="commentEditableTxtBox"]'
  commentEditableTxtBoxSaveBtn = 'button[data-testid="commentEditableTxtBox-save"]'
  commentEditableTxtBoxCancelBtn = 'button[data-testid="commentEditableTxtBox-cancel"]'

  /**
   * Stores the current NR number by reading from the header. The NR will
   * be available through cypress as nrNum.
   */
  retrieveCurrentNr() {
    cy.get(this.nrNumberHeader)
      .should('be.visible')
      .invoke('text')
      .should('not.be.empty')
      .then((text) => {
        cy.wrap(text.trim()).as('nrNum')
    })
  }

  /**
   * Navigates to the transactions page by clicking the transactions icon.
   */
  clickTransactionsLink() {
    cy.get(this.openTransactionsLink)
      .should('be.visible')
      .invoke('removeAttr', 'target').click({ force: true }) // Stay on the same page
    cy.url().should('include', '/transactions')
  }

  /**
   * Examine an NR by clicking the "Examine Names" button
   * and then waits until the page is stable.
   */
  clickExamineButton() {
    cy.intercept('PATCH', '**/api/v1/requests/NR*').as('examinePatchRequest')
    cy.get(this.actionExamineBtn).should('be.visible').click({ force: true })
    cy.wait('@examinePatchRequest').its('response.statusCode').should('eq', 200)
    cy.wait(1000)
  }

  /**
   * Retrieves the next NR by clicking the "Get Next" button
   * and then waits until the page is stable.
   */
  clickNextButton() {
    cy.intercept('GET', '**/api/v1/requests/NR*').as('nextGetRequest')
    cy.get(this.actionNextBtn).should('exist').click({ force: true })
    cy.wait('@nextGetRequest').its('response.statusCode').should('eq', 200)
    cy.waitForSpinner()
    cy.wait(1000)
  }

  /**
   * Puts the current NR on hold by clicking the "Hold Request" button
   * and then waits until the page is stable.
   */
  clickHoldButton() {
    cy.intercept('PATCH', '**/api/v1/requests/NR*').as('holdPatchRequest')
    cy.get(this.actionHoldBtn).should('be.visible').click({ force: true })
    cy.wait('@holdPatchRequest').its('response.statusCode').should('eq', 200)
    cy.wait(1000)
  }

  /**
   * Approves the current name by clicking the "Approve Name" button
   * and then waits until the page is stable.
   */
  clickApproveButton() {
    cy.intercept('PATCH', '**/api/v1/requests/NR*').as('approvePatchRequest')
    cy.get(this.primaryApproveBtn).should('be.visible').click({ force: true })
    cy.wait('@approvePatchRequest').its('response.statusCode').should('eq', 200)
    cy.wait(1000)
  }

  /**
   * Approves the current name by clicking the "Quick Approve" button
   * and then waits until the page is stable.
   */
  clickQuickApproveButton() {
    cy.intercept('PATCH', '**/api/v1/requests/NR*').as('quickApprovePatchRequest')
    cy.get(this.quickApproveBtn).should('be.visible').click({ force: true })
    cy.wait('@quickApprovePatchRequest').its('response.statusCode').should('eq', 200)
    cy.wait(1000)
  }

  /**
   * Rejects the current name by clicking the "Reject Name" button
   * and then waits until the page is stable.
   */
  clickRejectButton() {
    cy.intercept('PUT', '**/api/v1/requests/NR*/names/*').as('rejectPutRequest')
    cy.get(this.primaryRejectBtn).should('be.visible').click({ force: true })
    cy.wait('@rejectPutRequest').its('response.statusCode').should('eq', 200)
    cy.wait(1000)
  }

  /**
   * Rejects the current name by clicking the "Reject Distincitve" button
   * and then waits until the page is stable.
   */
  clickQuickRejectDistButton() {
    cy.intercept('PUT', '**/api/v1/requests/NR*/names/*').as('rejectDistPutRequest')
    cy.get(this.quickRejectDistBtn).click({ force: true })
    cy.wait('@rejectDistPutRequest').its('response.statusCode').should('eq', 200)
    cy.wait(1000)
  }

  /**
   * Rejects the current name by clicking the "Reject Descriptive" button
   * and then waits until the page is stable.
   */
  clickQuickRejectDescButton() {
    cy.intercept('PUT', '**/api/v1/requests/NR*/names/*').as('rejectDescPutRequest')
    cy.get(this.quickRejectDescBtn).click({ force: true })
    cy.wait('@rejectDescPutRequest').its('response.statusCode').should('eq', 200)
    cy.wait(1000)
  }

  /**
   * Brings up the editable details for the NR by clicking the
   * "Edit Request" button.
   */
  clickEditButton() {
    cy.get(this.actionEditBtn).click({ force: true })
  }

  /**
   * Saves the edits for an NR by clicking the "Save Edits" button
   * and then waits until the page is stable.
   */
  clickSaveEditsButton() {
    cy.intercept('GET', '**/api/v1/requests/NR*').as('saveEditsGetRequest')
    cy.get(this.actionSaveBtn).click({ force: true })
    cy.wait('@saveEditsGetRequest').its('response.statusCode').should('eq', 200)
    cy.wait(1000)
  }

  /**
   * Cancels the edits for an NR by clicking the "Cancel" button
   * and then waits until the page is stable.
   */
  clickCancelEditsButton() {
    cy.intercept('GET', '**/api/v1/requests/NR*').as('cancelEditsGetRequest')
    cy.get(this.actionCancelBtn).click({ force: true })
    cy.wait('@cancelEditsGetRequest').its('response.statusCode').should('eq', 200)
    cy.wait(1000)
  }

  /**
   * Toggles the details by clicking the "Show Details" button if showDetails
   * is true, else it clicks the "Hide Details" button.
   *
   * @param showDetails - The value if details should be shown.
   */
  toggleDetails(showDetails: boolean) {
    const buttonSelector = showDetails ? this.actionShowDetailsBtn : this.actionHideDetailsBtn
    cy.get(buttonSelector)
      .should('be.visible')
      .click({ force: true })
    cy.get(showDetails ? this.actionHideDetailsBtn : this.actionShowDetailsBtn)
      .should('be.visible')
    cy.wait(1000)
  }

  /**
  * Toggles the consent checkbox on or off.
  * @param shouldCheck - If true, the checkbox will be checked; if false, it will be unchecked.
  */
  toggleConsentCheckbox(shouldCheck: boolean) {
    cy.get(this.consentCheckbox).then($checkbox => {
      if ($checkbox.is(':checked') !== shouldCheck) {
        cy.wrap($checkbox).click()
      }
    })
  }
}

export default ExaminePage
