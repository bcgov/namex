var loginCommands = {

	login: function () {
		return this.waitForElementNotVisible('@loading_overlay', 5000)
			.waitForElementVisible('@login_button', 5000)
			.click('@login_button')
			.waitForElementVisible('@keycloak_logo', 5000)
			.setValue('@keycloak_username', 'names-examiner')
			.setValue('@keycloak_password', 'WhatEver1')
			.click('@keycloak_login_button')
			.waitForElementVisible('@app_container', 5000);

	},
	checkIfLandingPageIsUp: function () {
		return this.waitForElementVisible('@app_container', 5000)
			.assert.containsText('@missing_auth_h2', 'Your authorization is missing or has expired. Please login.')
	}
};

module.exports = {
	commands: [loginCommands],
	url: function () {
		return this.api.globals.NamexPath;
	},
	elements: {
		missing_auth_h2: 'h2',
		login_button: '#header-login-button',
		loading_overlay: '#loading-overlay',
		keycloak_logo: '#kc-logo-wrapper',
		keycloak_username: '#username',
		keycloak_password: '#password',
		keycloak_login_button: '#kc-login',
		app_container: '#app'
	}
};