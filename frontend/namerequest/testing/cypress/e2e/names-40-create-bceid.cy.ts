import type { LocaleDefinition } from '@faker-js/faker';
import { base, en, Faker, en_CA } from '@faker-js/faker';
const customFaker = new Faker({
    locale: [en, base, en_CA],
});

describe('names-40-create', () => {
    beforeEach(() => {
        customFaker.seed(Date.now() ^ (Math.random() * 0x100000000));
        cy.visit('https://dev.names.bcregistry.gov.bc.ca');
        cy.get("#loginBtn").click().then(() => {
            cy.get('div[role="menu"', { timeout: 1000 }).within(() => {
                cy.contains('div', 'BC Services Card').click();
            });

            cy.setid('bceid').then(() => {

                    cy.get('#tile_test_with_username_password_device_div_id').click({ force: true })
                    cy.wait(3000)

                    // Validate siteminder and login
                    cy.contains('h1', 'Log in to: BC Registries', { timeout: 10000 }).should('be.visible')

                    cy.get('input#username', { timeout: 10000 }).type(
                        Cypress.env('username')
                    )
                    cy.get('input#password', { timeout: 10000 }).type(
                        Cypress.env('password'),
                        { log: false }
                    )

                    cy.get('button#submit-btn', { timeout: 10000 }).click()
                    cy.wait(3000)
            });
        });
    });

    afterEach(() => {
        cy.get('button.user-account-btn').click().then(() => {
            cy.contains('div', 'Log out').click();
        })
    });

    let i = 0;
    while (i < 20) {
    it('should create a new name', () => {
        cy.log('here we go!')
        cy.get('#request-action-select').click().then(() => {
            cy.contains('span', 'For businesses that do not exist yet').click()
            cy.contains('div', 'Start a new BC-based business').click()
            cy.get('#entity-type-options-select').click().then(() => {
                cy.contains('span', 'Limited Company').click()
            })
        });

        cy.get('div#company-type').next().within(() => {
            cy.get('#name-input-component').type(customFaker.company.name())
        });

        cy.get('div#designation').click().then(() => {
            cy.contains('div.v-list-item__title', 'INC.').eq(0).click({ force: true })
        })

        cy.get('#search-name-btn').click()

        cy.get('#name-check-submit-btn').click()
        cy.get('button.submit-continue-btn').click()

        /*         firstname: string = 'input[type="text"][id="firstname"]'
        middlename: string = 'input[type="text"][id="middlename"]'
        lastname: string = 'input[type="text"][id="lastname"]'
        line1: string = 'input[type="text"][id="line1"]'
        1ine2: string = 'input[type="text"][id="1ine2"]'
        city: string = 'input[type="text"][id="city"]'
        province: string = 'input[type="text"][id="province"]'
        country: string = 'input[type="text"][id="country"]'
        postalcode: string = 'input[type="text"][id="postalcode"]' */

        cy.get('input[type="text"][id="firstname"]').type(customFaker.person.firstName())
        cy.get('input[type="text"][id="middlename"]').type(customFaker.person.middleName())
        cy.get('input[type="text"][id="lastname"]').type(customFaker.person.lastName())
        cy.get('input[type="text"][id="line1"]').focus().type(customFaker.number.int({ min: 10, max: 9000 }).toString())

        /*         cy.get('input[type="text"][id="line2"]').type(customFaker.location.streetAddress())
                cy.get('input[type="text"][id="city"]').type(customFaker.location.city())
                cy.get('input[type="text"][id="province"]').type(customFaker.location.state())
                cy.get('input[type="text"][id="country"]').type(customFaker.location.country())
                cy.get('input[type="text"][id="postalcode"]').type(customFaker.location.zipCode()) */

        cy.get('div[role="menu"]').within(() => {
            cy.get('a.link-sm-dk-text').eq(0).click({ force: true })
        });
        cy.get('input[role="checkbox"]').click({ force: true })

        cy.get('button.submit-continue-btn').eq(1).click()

        cy.get('input[type="text"][id="emailAddress"]').type('roland.stens@gov.bc.ca')
        cy.get('input[type="tel"][id="phoneNumber"]').type('123')
        cy.get('input[type="text"][id="faxNumber"]').type(customFaker.phone.number())
        cy.get('textarea[id="natureBusinessInfo"]').type(customFaker.lorem.sentence())
        cy.get('textarea[id="additionalInfo"]').type(customFaker.lorem.sentence())

        // Select Urgent
        // cy.get('input[type="checkbox"][role="checkbox"]').eq(1).click({ force: true })

        cy.get('button.submit-continue-btn').eq(2).click()

        cy.get('div[role="dialog"]').within(() => {
            cy.get('button#confirm-nr-continue-btn').click()
        })


        cy.get('#existing-request-display').should('exist') // Shows details of the request
        // cy.pause() // to copy down the NR number

        cy.get('#back-to-search-btn').click()
        cy.get('#tabs-landing-comp').should('exist') // back to landing page
    });
    i++;
}
});