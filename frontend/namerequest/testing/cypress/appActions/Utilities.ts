/**
 * Handy utilities for the app
 */
import MD5 from 'crypto-js/md5'

/**
 * Utility class that provides various helper functions.
 */
class Utilities {
  /**
   * Checks if the provided data meets the conditions for running the test.
   * @param data - The data object containing test flags.
   * @return A boolean value indicating whether the test should be run or not.
   */
  runOk(data: any): boolean {
    const isLocalTest = Cypress.env('localtest')
    const isSmokeTest = Cypress.env('smoketest')

    // Directly return the evaluation based on conditions
    if (!isLocalTest && !isSmokeTest) {
      // If neither localtest nor smoketest is set, always return true
      return true
    } else if (isLocalTest && isSmokeTest) {
      // If both flags are set, check corresponding data properties
      return data.localtest && data.smoketest
    } else if (isLocalTest) {
      // If only localtest is set, check the localtest data property
      return data.localtest
    } else if (isSmokeTest) {
      // If only smoketest is set, check the smoketest data property
      return data.smoketest
    }

    // Default return should never be reached due to logic above covering all cases,
    // but it's good practice to have a fallback return in case the function logic evolves.
    return false
  }

  /**
   * Calculates the MD5 hash of the given data.
   *
   * @param data - The data to calculate the MD5 hash for.
   * @return The MD5 hash as a string.
   */
  md5(data: string): string {
    return MD5(data).toString()
  }

  /**
   * Returns the current date in the format "YYYYMMDD".
   *
   * @return The current date in the format "YYYYMMDD".
   */
  getDate(): string {
    let today = new Date()
    let dd: any = today.getDate()
    let mm: any = today.getMonth() + 1 //January is 0!
    let yyyy = today.getFullYear()
    if (dd < 10) {
      dd = '0' + dd
    }
    if (mm < 10) {
      mm = '0' + mm
    }
    return yyyy + mm + dd
  }

  /**
   * Generates a random integer between the specified minimum and maximum values.
   * The maximum value is exclusive and the minimum value is inclusive.
   *
   * @param min - The minimum value of the range (inclusive).
   * @param max - The maximum value of the range (exclusive).
   * @return A random integer between the minimum and maximum values.
   */
  getRandomInt(min: number, max: number): number {
    const minCeiled = Math.ceil(min)
    const maxFloored = Math.floor(max)
    return Math.floor(Math.random() * (maxFloored - minCeiled) + minCeiled)
  }

  /**
   * Retrieves the key from a given object map based on the provided search value.
   * @param map - The object map to search in.
   * @param searchValue - The value to search for.
   * @return The key associated with the search value, or undefined if the value is not found.
   */
  getKeyByValue(
    map: { [key: string]: string },
    searchValue: string // Add JSDoc parameter type for 'searchValue'
  ): string | undefined {
    for (const [key, value] of Object.entries(map)) {
      if (value === searchValue) {
        return key
      }
    }
    return undefined // or return a default value or handle the case when the value is not found
  }
}
export default Utilities
