// Cypress Test: Check for ability to edit NRs.
// This spec checks that all of the edits in the show details section
// are functional.
import HomePage from 'cypress/pageObjects/homePage'
import ExaminePage from 'cypress/pageObjects/examinePage'
import testData from 'cypress/fixtures/smoke-test-data.json'
const homePage = new HomePage()
const examinePage = new ExaminePage()

describe('Check that editing an NR works', () => {
  beforeEach(() => {
    cy.cleanGC()
    cy.setid('default')
    cy.login()
  })

  afterEach(() => {
    cy.logout()
  })


  it('Should be able to edit an NR', () => {
    const data = testData.testEditNRData

    // Examine an NR and press the edit button.
    homePage.examineNamesLink()
    examinePage.clickEditButton()

    // Make a change on every available option.
    cy.get(examinePage.editNRTypeDropdownBtn).click()
    cy.contains('li', data.companytype).click()
    cy.typeInField(examinePage.editAdditionalInfoTxtBox, data.additionalInfo)
    cy.typeInField(examinePage.editClientFirstNameText, data.clientFirstName)
    cy.typeInField(examinePage.editClientLastNameText, data.clientLastName)
    cy.typeInField(examinePage.editApplicantFirstNameText, data.applicantFirstName)
    cy.typeInField(examinePage.editApplicantMiddleNameText, data.applicantMiddleName)
    cy.typeInField(examinePage.editApplicantLastNameText, data.applicantLastName)
    cy.typeInField(examinePage.editApplicantAddressText1, data.addressLine1)
    cy.typeInField(examinePage.editApplicantAddressText2, data.addressLine2)
    cy.typeInField(examinePage.editApplicantAddressText3, data.addressLine3)
    cy.typeInField(examinePage.editApplicantCityText, data.city)
    cy.typeInField(examinePage.editApplicantProvinceText, data.province)
    cy.typeInField(examinePage.editApplicantPostalCodeText, data.postalCode)
    cy.typeInField(examinePage.editApplicantCountryText, data.country)
    cy.typeInField(examinePage.editApplicantPhoneText, data.phone)
    cy.typeInField(examinePage.editApplicantFaxText, data.fax)
    cy.typeInField(examinePage.editApplicantEmailText, data.email)
    cy.typeInField(examinePage.editApplicantContactText, data.contact)
    cy.typeInField(examinePage.editNameChoiceText1, data.firstChoice)
    cy.typeInField(examinePage.editNameChoiceText2, data.secondChoice)
    cy.typeInField(examinePage.editNameChoiceText3, data.thirdChoice)
    // Add a comment.
    cy.get(examinePage.commentsPopupBtn).click()
    cy.typeInField(examinePage.commentEditableTxtBox, data.comment)
    cy.get(examinePage.commentEditableTxtBoxSaveBtn).click()

    // Save the Edits.
    examinePage.clickSaveEditsButton()
    cy.wait(1000)

    // Verify all of the edits persisted.
    cy.verifyTextContent(examinePage.nrType, data.companytype)
    cy.verifyTextContent(examinePage.additionalInfo, data.additionalInfo)
    cy.verifyTextContent(examinePage.clientName, `${data.clientFirstName} ${data.clientLastName}`)
    cy.verifyTextContent(examinePage.applicantName, `${data.applicantFirstName} ${data.applicantLastName}`)
    cy.verifyTextContent(examinePage.addressLine1, data.addressLine1)
    cy.verifyTextContent(examinePage.addressLine2, data.addressLine2)
    cy.verifyTextContent(examinePage.addressLine3, data.addressLine3)
    cy.verifyTextContent(examinePage.addressCityProvince, `${data.city} ${data.province}`)
    cy.verifyTextContent(examinePage.addressPostalCode, data.postalCode)
    cy.verifyTextContent(examinePage.addressCountry, data.country)
    cy.verifyTextContent(examinePage.phone, data.phone)
    cy.verifyTextContent(examinePage.fax, data.fax)
    cy.verifyTextContent(examinePage.email, data.email)
    cy.verifyTextContent(examinePage.contact, data.contact)
    cy.verifyTextContent(examinePage.choice1Txt, data.firstChoice.toUpperCase())
    cy.verifyTextContent(examinePage.choice2Txt, data.secondChoice.toUpperCase())
    cy.verifyTextContent(examinePage.choice3Txt, data.thirdChoice.toUpperCase())
    // Verify the comment persisted.
    cy.get(examinePage.commentsPopupBtn).click()
    cy.get(examinePage.commentsContainer).within(() => {
      cy.contains('p', data.comment).should('be.visible')
    })
    cy.get(examinePage.commentEditableTxtBoxCancelBtn).click()

    examinePage.toggleDetails(false)
  })
})
