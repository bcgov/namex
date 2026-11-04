import { Component, Vue } from 'vue-property-decorator'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'
import { isDate } from 'lodash'
import { dateToYyyyMmDd as formatVancouverDate, vancouverWallTimeToUtc } from '@/utils/vancouver-date'

/**
 * Mixin that provides some useful date utilities.
 * Ref: https://github.com/bcgov/business-edit-ui/blob/master/src/mixins/date-mixin.ts
 */
@Component({})
export class DateMixin extends Vue {
  readonly MS_IN_A_DAY = (1000 * 60 * 60 * 24)

  @Getter(useStore) getCurrentJsDate!: Date

  /**
   * Fetches and returns the web server's current date (in UTC).
   * Used to bypass the user's local clock/timezone.
   * Ref: https://www.npmjs.com/package/serverdate
   * @returns a promise to return a Date object
   */
  async getServerDate (): Promise<Date> {
    const input = `${window.location.origin}${import.meta.env.VUE_APP_PATH}/`
    const init: RequestInit = { cache: 'no-store', method: 'HEAD' }

    try {
      const { headers, ok, statusText } = await fetch(input, init)
      if (!ok) throw new Error(statusText)
      return new Date(headers.get('Date'))
    } catch {
      // eslint-disable-next-line no-console
      console.warn('Unable to get server date - using browser date instead')
      // fall back to local date
      // NB: filing may contain invalid dates/times
      return new Date()
    }
  }

  /**
   * Creates and returns a new Date object in UTC, given parameters in Pacific timezone.
   * (This works regardless of user's local clock/timezone.)
   * @example "2021, 0, 1, 0, 0" -> "2021-01-01T08:00:00.000Z"
   * @example "2021, 6, 1, 0, 0" -> "2021-07-01T07:00:00.000Z"
   */
  createUtcDate (year: number, month: number, day: number, hours = 0, minutes = 0): Date {
    return vancouverWallTimeToUtc(year, month, day, hours, minutes)
  }

  /**
   * Converts a Date object to a date string (Month Day, Year) in Pacific timezone.
   * @example "2021-01-01 07:00:00 GMT" -> "December 31, 2020"
   * @example "2021-01-01 08:00:00 GMT" -> "January 1, 2021"
   */
  dateToPacificDate (date: Date): string {
    // safety check
    if (!isDate(date) || isNaN(date.getTime())) return null

    // NB: some versions of Node have only en-US locale
    // so use that and convert results accordingly
    let dateStr = date.toLocaleDateString('en-US', {
      timeZone: 'America/Vancouver',
      month: 'long', // December
      day: 'numeric', // 31
      year: 'numeric' // 2020
    })

    // remove period after month
    dateStr = dateStr.replace('.', '')
    return dateStr
  }

  /**
   * Converts a Date object to a time string (HH:MM am/pm) in Pacific timezone.
   * @example "2021-01-01 07:00:00 GMT" -> "11:00 pm"
   * @example "2021-01-01 08:00:00 GMT" -> "12:00 am"
   */
  dateToPacificTime (date: Date): string {
    // safety check
    if (!isDate(date) || isNaN(date.getTime())) return null

    // NB: some versions of Node have only en-US locale
    // so use that and convert results accordingly
    let timeStr = date.toLocaleTimeString('en-US', {
      timeZone: 'America/Vancouver',
      hour: 'numeric', // 11
      minute: '2-digit', // 00
      hour12: true // a.m./p.m.
    })

    // replace AM with am and PM with pm
    timeStr = timeStr.replace('AM', 'am').replace('PM', 'pm')

    return timeStr
  }

  /**
   * Converts a Date object to a date and time string (Month Day, Year at HH:MM am/pm Pacific time).
   * @example "2020-10-27T18:45:00Z" -> "October 27, 2020 at 11:45 am Pacific time"
   */
  dateToPacificDateTime (date: Date): string {
    // safety check
    if (!isDate(date) || isNaN(date.getTime())) return null

    const dateStr = this.dateToPacificDate(date)
    const timeStr = this.dateToPacificTime(date)

    return `${dateStr} at ${timeStr} Pacific time`
  }

  /**
   * The number of days that 'date' is from today (in Pacific tz).
   * @param date the Date object to compare
   * @returns -1 for yesterday
   * @returns 0 for today
   * @returns +1 for tomorrow
   * @returns NaN in case of error
   */
  daysFromToday (date: Date): number {
    // safety check
    if (!isDate(date) || isNaN(date.getTime())) return NaN

    // convert Dates to dates to Pacific tz
    const todayPacific = this.dateToYyyyMmDd(this.getCurrentJsDate)
    const datePacific = this.dateToYyyyMmDd(date)

    // get milliseconds for start of "today" and start of "date"
    const todayPacificMs = new Date(todayPacific).setHours(0, 0, 0, 0)
    const datePacificMs = new Date(datePacific).setHours(0, 0, 0, 0)

    // return diff in days
    return Math.round((datePacificMs - todayPacificMs) / this.MS_IN_A_DAY)
  }

  /**
   * Converts a Date object to a date string (YYYY-MM-DD) in Pacific timezone.
   * @example "2021-01-01 07:00:00 GMT" -> "2020-12-31"
   * @example "2021-01-01 08:00:00 GMT" -> "2021-01-01"
   * @example "2021-01-01 00:00:00 PST" -> "2021-01-01"
   * @example "2021-01-01 23:59:59 PST" -> "2021-01-01"
   */
  dateToYyyyMmDd (date: Date): string {
    return formatVancouverDate(date)
  }

  /**
   * Converts an API datetime string to a date and time string (YYYY-MM-DD at HH:MM am/pm)
   * in Pacific timezone.
   * @example "2021-01-01T00:00:00.000000+00:00" -> "2020-12-31 at 04:00 pm" (PST example)
   * @example "2021-07-01T00:00:00.000000+00:00" -> "2021-06-30 at 05:00 pm" (PDT example)
   */
  apiToDateString (dateString: string): string {
    if (!dateString) return null // safety check

    // convert to ISO format
    // then create a Date object
    // eg, 2021-03-04T04:41:00Z
    dateString = dateString.slice(0, 19) + 'Z'
    const utc = new Date(dateString)

    // build date string, eg, "2021-03-03"
    const dateStr = this.dateToYyyyMmDd(utc)

    return `${dateStr}`
  }
}
