import { DateTime } from 'luxon'

export const TIMESTAMP_FORMAT = 'yyyy-MM-dd, h:mm a'

/**
 * @param input An ISO-formatted date string
 * @returns a formatted date string, ex: 2023-01-15
 */
export function getFormattedDate(input: string) {
  return DateTime.fromISO(input).toISODate()
}

/**
 * @param input An ISO-formatted date string
 * @returns a formatted date with time, ex: 2023-01-15, 9:00am
 */
export function getFormattedDateWithTime(input: string): string {
  return DateTime.fromISO(input).toFormat(TIMESTAMP_FORMAT)
}

/**
 * @param input A luxon `DateTime` object
 * @returns a formatted date, ex: 2023-01-15
 */
export function getDateFromDateTime(input: DateTime): string | null {
  return input.toISODate()
}

/**
 * @param input A luxon `DateTime` object
 * @returns a formatted date with time, ex: 2023-01-15, 9:00am
 */
export function getDateWithTimeFromDateTime(input: DateTime): string {
  return input.toFormat(TIMESTAMP_FORMAT)
}

/**
 * @param input A luxon `DateTime` object
 * @returns a formatted date with time and timezone, ex: 2023-01-15, 9:00am PST
 */
export function getFormattedDateWithTimeAndZone(input: DateTime): string {
  return input.toFormat(`${TIMESTAMP_FORMAT} ZZZZ`)
}

/** Parse a date string into a `luxon` `DateTime` object.
 * @param input A date string from a NameX API object (ISO format).
 */
export function parseDate(input: string) {
  return DateTime.fromISO(input)
}

export function getVancouverDate(input: string): string | null {
  return DateTime.fromISO(input).setZone('America/Vancouver').toISODate()
}
