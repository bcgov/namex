var examineCommands = {
	clickThenWaitForSolrSearch: function (elementToClick, browser) {
		return this.waitForElementNotVisible('#loading-overlay')
			.waitForXHR('@slowest_solr_search_XHR', 5000, function browserTrigger() {
				browser.click(elementToClick);
			}, function testCallback(xhrs) {
				browser.assert.equal(xhrs[0].status, "success");
				browser.assert.equal(xhrs[0].httpResponseCode, 200);
			});
	},
	loadNRandWait: function (NR_num, browser) {
		return this.waitForElementVisible('@header_load_NR_textbox')
			.setValue('@header_load_NR_textbox', NR_num)
			.clickThenWaitForSolrSearch(this.elements.header_load_NR_button.selector, browser);

	},
	loadNRnoWait: function (NR_num) {
		return this.waitForElementVisible('@header_load_NR_textbox')
			.setValue('@header_load_NR_textbox', NR_num)
			.waitForElementNotVisible('#loading-overlay')
			.click('@header_load_NR_button');
	},
	editNR: function () {
		return this.setValue('@edit_name_choice_1', ' EDIT')
			.setValue('@edit_address_line_1', ' EDIT');
	},
	completeManualSearch: function (searchTerm, browser) {
		return this
			.clearValue('@manual_search_box')
			.setValue('@manual_search_box', searchTerm)
			.clickThenWaitForSolrSearch(this.elements.manual_search_button.selector, browser);

	},
	dismissModal: function () {
		//Shouldn't be needed once test data is well set up
		return this
			.waitForElementVisible('#error-message-modal > div > div')
			.assert.cssClassPresent('body', 'modal-open')
			.assert.cssClassPresent('#error-message-modal', 'modal')
			.assert.cssClassPresent('#error-message-modal', 'fade')
			.assert.cssClassPresent('#error-message-modal', 'show')
			.assert.attributeContains('#error-message-modal', 'style', 'display: block;')
			.waitForElementVisible('#error-message-modal > div > div > div.modal-footer > button')
			.click('#error-message-modal > div > div > div.modal-footer > button')
			.waitForElementNotVisible('#error-message-modal')
			.assert.cssClassNotPresent('body', 'modal-open');
	},
	beginExamining: function () {
		return this
			.click('@examine_button')
			.waitForElementVisible('@decision_button')
	},
	cancelNR: function () {
		return this
			.waitForElementVisible('@cancel_button')
			.click('@cancel_button')
			.waitForElementVisible('@cancel_comment')
			.setValue('@cancel_comment', 'TEST CANCEL TEST CANCEL')
			.click('@confirm_cancel_button');
	}

};

module.exports = {
	commands: [examineCommands],
	elements: {
		header_load_NR_textbox: '#header-search-input',
		header_load_NR_button: '#header-search-button',

		slowest_solr_search_XHR: 'https://namex-test.pathfinder.gov.bc.ca/api/v1/documents:histories',
		requests_XHR: 'https://namex-test.pathfinder.gov.bc.ca/api/v1/requests',

		edit_button: '#nr-details-edit-button',
		edit_save_button: '#nr-details-save-button',
		edit_name_choice_1: '#div2 > div:nth-child(2) > div > table > tr:nth-child(1) > td:nth-child(2) > input',
		edit_address_line_1: '#div3 > div.row.add-bottom-padding-extra > div > div.row.add-bottom-padding > div > span > span > input:nth-child(5)',

		name_choice_1: '#name1',
		current_NR: 'div.nrNum',

		conflicts_recipe_step: '#conflicts-tab',
		condition_recipe_step: '#conditions-tab',
		trademark_recipe_step: '#trademarks-tab',
		history_recipe_step: '#history-tab',

		manual_search_box: '#manual-search > form > div > input',
		manual_search_button: '.btn-search',

		exact_match_result: '#conflict-list > div.conflict-result.conflict-exact-match > div',
		condition_result: '#conditions-wrapper > div > div.-complex-table > div.-table-body > div > table > tbody > tr > td:nth-child(1)',
		trademark_result: '#trademarks-wrapper > p > div > div:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(1)',
		history_result: 'div.row.history-list-view > select > option',

		conflict_details_corp_name: '#currentConflictName',

		examine_button: '#examine-button',
		decision_button: '#examine-decide-button',
		reject_distinctive_button: '#examine-reject-distinctive-button',
		reopen_button: '#examine-re-open-button',

		cancel_button: '#examine-cancel-button',
		cancel_comment: '#cancel-comment-text',
		confirm_cancel_button: '#cancel-nr-after-comment-button'
	}
};