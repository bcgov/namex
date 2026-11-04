import { describe, expect, it } from 'vitest'
import { getVancouverDate } from '~/util/date'

describe('getVancouverDate', () => {
  it.each([
    ['2026-11-15T06:59:00.000Z', '2026-11-14'],
    ['2026-01-16T07:59:00.000Z', '2026-01-15'],
    ['2026-11-15T07:30:00.000Z', '2026-11-15'],
  ])('converts %s to %s', (input, expected) => {
    expect(getVancouverDate(input)).toBe(expected)
  })
})
