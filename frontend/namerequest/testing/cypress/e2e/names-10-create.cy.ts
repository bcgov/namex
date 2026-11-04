import type { LocaleDefinition } from '@faker-js/faker';
import { base, en, Faker, en_CA } from '@faker-js/faker';
const customFaker = new Faker({
    locale: [en, base, en_CA],
});
import HomePage from '../pageObjects/homePageRequest'
const homePage = new HomePage()

describe('names-10-create', () => {
    beforeEach(() => {
        customFaker.seed(Date.now() ^ (Math.random() * 0x100000000));
        cy.login()
    });

    afterEach(() => {
        cy.logout()
    });

    let i = 0;
    while (i < 1) {
    it('should create a new name', () => {
        cy.log('here we go!')
        cy.get(homePage.requestActionSelect).click().then(() => {
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
        cy.get('button.submit-continue-btn').eq(2).click()

        cy.get('div[role="dialog"]').within(() => {
            cy.get('button#confirm-nr-continue-btn').click()
        })

        cy.wait(1000)
        cy.contains('label', 'No Fee').click()
        cy.get('button#confirm-nr-submit-btn').click()


    });
    i++;
    }
});