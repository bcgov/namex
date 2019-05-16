var loginCommands = {

	login: function (KeycloakCredU, KeycloakCredP) {
		return this.waitForElementNotVisible('@loading_overlay')
			.waitForElementVisible('@login_button')
			.click('@login_button')
			.waitForElementVisible('@keycloak_logo')
			.setValue('@keycloak_username', KeycloakCredU)
			.setValue('@keycloak_password', KeycloakCredP)
			.click('@keycloak_login_button');

	},
	checkIfLandingPageIsUp: function () {
		return this.waitForElementVisible('@app_container')
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
		idir_button: '#zocial-idir',
		loading_overlay: '#loading-overlay',
		siteminder_user: '#user',
		siteminder_pw: '#password',
		siteminder_continue_button: 'input[value="Continue"]',
		app_container: '#app',
		keycloak_logo: '#kc-logo-wrapper',
		keycloak_username: '#username',
		keycloak_password: '#password',
		keycloak_login_button: '#kc-login'
	}
};