var searchCommands = {
    navigateToSearchPage: function () {
        return this.waitForElementVisible('@header_search_link')
            .click('@header_search_link');

    },
    searchNR: function (NR_num, browser) {
        var NRColumnValue;
        browser.expect.element(this.elements.loading_overlay.selector).to.have.css('display').which.equals('none').before(5000);

        this.waitForElementVisible('@NR_column')
            .getValue('@NR_column', function (result) {
                NRColumnValue = result.value;
            })
            .perform(function () {
                if (NRColumnValue != NR_num) {
                    browser.setValue('#search-filter-nr-number', NR_num);
                }

            })
            .setValue('@status_column', 'ALL');

        browser.expect.element(this.elements.loading_overlay.selector).to.have.css('display').which.equals('none').before(5000);
        browser.expect.element(this.elements.NR_column.selector).value.to.equal(NR_num).before(5000);
        browser.expect.element(this.elements.status_column.selector).value.to.equal('ALL').before(5000);

        this.click('@NR_column');
        return this.waitForXHR('@search_XHR', 1000, function browserTrigger() {
            browser.keys(browser.Keys.ENTER);
        }, function testCallback(xhrs) {
            browser.assert.equal(xhrs[0].status, "success");
            browser.assert.equal(xhrs[0].httpResponseCode, 200);
        });

    },
    waitForExtractorUpdater: function () {
        return this.pause(180000);
    }
};

module.exports = {
    commands: [searchCommands],
    elements: {
        header_search_link: '#header-search-link',
        loading_overlay: '#loading-overlay',
        status_column: '#search-filter-state',
        NR_column: '#search-filter-nr-number',
        first_row_result_NR: '#search-table > tbody > tr:nth-child(1) > td.text-center.link > a',
        first_row_result_notification: '#search-table > tbody > tr > td:nth-child(7)',
        search_XHR: 'https://namex-test.pathfinder.gov.bc.ca/api/v1/requests'
    }
};