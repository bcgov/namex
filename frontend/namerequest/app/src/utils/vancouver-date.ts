import { isDate } from 'lodash'

const ZONE = 'America/Vancouver'

export function dateToYyyyMmDd (date: Date): string | null {
  if (!isDate(date) || isNaN(date.getTime())) return null

  const [mm, dd, yyyy] = date.toLocaleDateString('en-US', {
    timeZone: ZONE,
    month: 'numeric',
    day: 'numeric',
    year: 'numeric'
  }).split('/')

  return `${yyyy}-${mm.padStart(2, '0')}-${dd.padStart(2, '0')}`
}

export function vancouverWallTimeToUtc (year: number, month: number, day: number, hours = 0, minutes = 0): Date {
  const guess = new Date(Date.UTC(year, month, day, hours, minutes))
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: ZONE,
    hourCycle: 'h23',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).formatToParts(guess)
  const field = (type: string) => Number(parts.find(part => part.type === type).value)
  const asUtc = Date.UTC(
    field('year'),
    field('month') - 1,
    field('day'),
    field('hour') % 24,
    field('minute'),
    field('second')
  )

  return new Date(guess.getTime() - (asUtc - guess.getTime()))
}
