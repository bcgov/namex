module.exports = {
    before: function (browser) {
        var options = {
            method: 'POST',
            uri: browser.globals.keycloakAuthURL,
            body: browser.globals.keycloakAuthBody,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
        };

        browser.apiPost(options, function (response) {
            var jsonResp = response.toJSON();
            var access_token = JSON.parse(jsonResp.body);
            browser.globals.token = access_token.access_token;
        });



        browser
            .url(browser.globals.NamexPath, function () {
                var cookie = {
                    'name': 'tester',
                    'value': browser.globals.token
                };
                browser.setCookie(cookie);

            });
    },

    'Step 1: Navigate to public NRO': function (browser) {
        browser
            .url(browser.globals.NROPath)
            .maximizeWindow()
            .waitForElementVisible('img[src="images/step3.gif"]')
            .click('img[src="images/step3.gif"]')
            .waitForElementVisible('input[name="_eventId_next"]')
            .click('input[name="_eventId_next"]');

    },

    'Step 2: NRO - Applicant Info': function (browser) {
        browser
            .waitForElementVisible('input[name="lastName"]')
            .setValue('input[name="lastName"]', 'TEST')
            .setValue('input[name="firstName"]', 'TEST')
            .click('#notifyMethod2')
            .setValue('input[name="address1"]', 'TEST 940 Blanshard Street')
            .setValue('input[name="city"]', 'TEST Victoria')
            .setValue('input[name="postalCode"]', 'V8W 2H3')
            .setValue('input[name="phoneNum"]', '5555555555')
            .click('img[alt="Next"]');
    },

    'Step 3: NRO - Select NR Type': function (browser) {
        browser
            .waitForElementVisible('#requestType1')
            .click('#requestType1')
            .click('img[alt="Next"]');
    },

    'Step 4: NRO - Enter Name Choices': function (browser) {
        browser
            .waitForElementVisible('input[name="nameOneText"]')
            .setValue('input[name="nameOneText"]', 'ZZZZZZZ 1 TEST NAME DO NOT EXAMINE')
            .setValue('input[name="nameTwoText"]', 'ZZZZZZZ 2 TEST NAME DO NOT EXAMINE')
            .setValue('input[name="nameThreeText"]', 'ZZZZZZZ 3 TEST NAME DO NOT EXAMINE')
            .setValue('#natureOfBusiness', 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST ')
            .setValue('#additionalInformation', 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST ')
            .click('img[alt="Next"]');
    },

    'Step 5: NRO - Confirmation Screen': function (browser) {
        browser
            .waitForElementVisible('input[name="cardHolderName"]')
            .setValue('input[name="cardHolderName"]', 'TEST')
            .setValue('input[name="phoneNumber"]', '5555555555')
            .click('#agree1')
            .click('#publicPay');
    },

    'Step 6: NRO - Beanstream CC page': function (browser) {
        browser
            .waitForElementVisible('input[name="trnCardNumber"]')
            .setValue('input[name="trnCardNumber"]', browser.globals.TestCC)
            .setValue('input[name="trnCardCvd"]', browser.globals.TestCVD)
            .click('input[name="submitButton"]');
    },

    'Step 6: NRO - Receipt Screen': function (browser) {
        browser.waitForElementVisible('#content');
        browser.getText("#command > table > tbody > tr:nth-child(7) > td > strong", function (result) {
            browser.globals.smokeTestNR.NR_num = result.value;
        });
    },

    'Step 7: Navigate to NameX landing page then log in': function (browser) {
        var options = {
            method: 'POST',
            uri: browser.globals.keycloakAuthURL,
            body: browser.globals.keycloakAuthBody,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
        };

        browser.apiPost(options, function (response) {
            var jsonResp = response.toJSON();
            var access_token = JSON.parse(jsonResp.body);
            browser.globals.token = access_token.access_token;
        });

        browser
            .url(browser.globals.NamexPath, function () {
                var cookie = {
                    'name': 'tester',
                    'value': browser.globals.token
                };
                browser.setCookie(cookie);

            })
            .url(browser.globals.NamexPath)
            .click('#header-login-button');
    },

    'Step 8:  NameX - wait for extractor to run': function (browser) {
        var searchPage = browser.page.namexSearch();

        searchPage
            .navigateToSearchPage()
            .searchNR(browser.globals.smokeTestNR.NR_num, browser)
            .waitForAttribute('#search-table > tbody > tr', 'class', function (result) {
                return result !== 'b-table-empty-row';
            }, 240000);
    },

    'Step 9:  NameX - Load NR': function (browser) {
        var examinePage = browser.page.namexExamination();

        examinePage
            .loadNRandWait(browser.globals.smokeTestNR.NR_num, browser)
            .assert.containsText('@name_choice_1', browser.globals.smokeTestNR.name_choice1)
            .assert.containsText('@current_NR', browser.globals.smokeTestNR.NR_num);
    },

    'Step 10:  NameX - Edit NR': function (browser) {
        var examinePage = browser.page.namexExamination();

        examinePage
            .waitForElementVisible('@edit_button')
            .waitForXHR('https://namex-test.pathfinder.gov.bc.ca/api/v1/requests', 5000, function browserTrigger() {
                browser.click('#nr-details-edit-button');
            }, function testCallback(xhrs) {
                browser.assert.equal(xhrs[0].method, "PATCH");
                browser.assert.equal(xhrs[0].status, "success");
                browser.assert.equal(xhrs[0].httpResponseCode, 200);
                browser.assert.equal(xhrs[1].method, "GET");
                browser.assert.equal(xhrs[1].status, "success");
                browser.assert.equal(xhrs[1].httpResponseCode, 200);
            });

        browser.expect.element('#firstName1').to.have.css('background-color').which.equals('rgba(255, 255, 255, 1)');

        examinePage
            .editNR()
            .clickThenWaitForSolrSearch('#nr-details-save-button', browser)
            .click('@conflicts_recipe_step');
    },

    'Step 11:  NameX - Enter exact match and check corp details pane': function (browser) {
        var examinePage = browser.page.namexExamination();

        examinePage
            .completeManualSearch(browser.globals.exactMatch, browser)
            .assert.containsText('@exact_match_result', browser.globals.exactMatch)
            .assert.containsText('@conflict_details_corp_name', browser.globals.exactMatch);
    },

    'Step 12:  NameX - Check Condition Recipe Step': function (browser) {
        var examinePage = browser.page.namexExamination();

        examinePage.completeManualSearch(browser.globals.conditionExample, browser)
            .click('@condition_recipe_step')
            .assert.containsText('@condition_result', browser.globals.conditionExample);
    },

    'Step 13:  NameX - Check Trademarks Recipe Step': function (browser) {
        var examinePage = browser.page.namexExamination();
        examinePage
            .click('@trademark_recipe_step')
            .assert.containsText('@trademark_result', browser.globals.trademarkResult);
    },

    'Step 14:  NameX - Check History Recipe Step': function (browser) {
        var examinePage = browser.page.namexExamination();

        examinePage
            .completeManualSearch(browser.globals.historyExample, browser)
            .click('@history_recipe_step')
            .assert.containsText('@history_result', browser.globals.historyExample);
    },

    'Step 15: NameX - Reject all 3 names': function (browser) {
        var examinePage = browser.page.namexExamination();

        examinePage
            .click('@conflicts_recipe_step')
            .beginExamining()
            .clickThenWaitForSolrSearch('#examine-reject-distinctive-button', browser)
            .waitForElementVisible('@decision_button')
            .clickThenWaitForSolrSearch('#examine-reject-distinctive-button', browser)
            .waitForElementVisible('@decision_button')
            .click('@reject_distinctive_button')
            .waitForElementVisible('@reopen_button');
    },

    'Step 16: NameX - Confirm Client Notification is complete': function (browser) {
        var searchPage = browser.page.namexSearch();

        searchPage
            .navigateToSearchPage()
            .searchNR(browser.globals.smokeTestNR.NR_num, browser)
            .waitForText('#search-table > tbody > tr > td:nth-child(7)', function (result) {
                return result === 'Notified';
            }, 240000)
            .assert.containsText('@first_row_result_NR', browser.globals.smokeTestNR.NR_num)
            .assert.containsText('@first_row_result_notification', 'Notified');
    },

    'Step 17: NRO - Check all updates complete': function (browser) {
        browser
            .url(browser.globals.NROPath)
            .maximizeWindow()
            .waitForElementVisible('img[src="images/step4.gif"]')
            .click('img[src="images/step4.gif"]')
            .waitForElementVisible('#nameRequestNum')
            .setValue('#nameRequestNum', browser.globals.smokeTestNR.NR_num)
            .setValue('#contactNumber', '5555555555')
            .click('img[alt="Get Name Request"]')
            .waitForElementVisible('#monitorStatusAnon');

        browser.expect.element('#monitorStatusAnon > table > tbody > tr:nth-child(9) > td > h3').text.to.contain(browser.globals.smokeTestNR.NR_num);
        browser.expect.element('#monitorStatusAnon > table > tbody > tr:nth-child(14) > td:nth-child(2)').text.to.contain('EDIT');

        browser
            .click('input[name="_eventId_veiwDetails"]')
            .waitForElementVisible('#applicantInfo');

        browser.expect.element('#applicantInfo > table > tbody > tr:nth-child(17) > td > table > tbody > tr:nth-child(2) > td:nth-child(3)').text.to.contain('EDIT');
        browser.expect.element('#monitorStatusAnon > table > tbody > tr:nth-child(14) > td:nth-child(2)').text.to.contain('Rejected');
        browser.expect.element('#monitorStatusAnon > table > tbody > tr:nth-child(20) > td:nth-child(2)').text.to.contain('Rejected');
        browser.expect.element('#monitorStatusAnon > table > tbody > tr:nth-child(26) > td:nth-child(2)').text.to.contain('Rejected');
    },

    'Step 18: Namex - log back into NameX': function (browser) {
        //var examinePage = browser.page.namexExamination();

        browser.url(browser.globals.NamexPath);
        browser.maximizeWindow();
        browser
            .click('#header-login-button')
            .waitForElementVisible('#header-search-input');
    },

    'Step 19: NameX - Cancel NR': function (browser) {
        var examinePage = browser.page.namexExamination();

        examinePage
            .loadNRnoWait(browser.globals.smokeTestNR.NR_num)
            .waitForElementVisible('@current_NR')
            .assert.containsText('@current_NR', browser.globals.smokeTestNR.NR_num)
            .cancelNR();
    },
    'Step 20: NRO - Confirm Cancel is complete': function (browser) {
        browser
            .url(browser.globals.NROPath)
            .maximizeWindow()
            .waitForElementVisible('img[src="images/step4.gif"]')
            .click('img[src="images/step4.gif"]')
            .waitForElementVisible('#nameRequestNum')
            .setValue('#nameRequestNum', browser.globals.smokeTestNR.NR_num)
            .setValue('#contactNumber', '5555555555')
            .click('img[alt="Get Name Request"]')
            .waitForElementVisible('#monitorStatusAnon');
            
        browser.expect.element('#monitorStatusAnon > table > tbody > tr:nth-child(11) > td:nth-child(2) > h3').text.to.contain('Cancelled');

        browser.end();

    }

};