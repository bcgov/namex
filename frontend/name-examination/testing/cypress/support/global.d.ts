declare namespace Cypress {
  interface Chainable<Subject> {
    login(
      username?: string,
      password?: string,
      host?: string,
      siteminder?: string
    ): Chainable<any>

    logout(): void

    setid(type: string): Chainable<any>

    cleanGC(): Chainable<any>

    linkChecker(): Chainable<any>

    waitForSpinner(): Chainable<any>

    verifyTextContent(selector: string, expectedText: string): Chainable<any>

    typeInField(inputSelector: string, text: string): Chainable<any>

    verifyNRState(nrNum: string, state: string): Chainable<any>
  }
}
