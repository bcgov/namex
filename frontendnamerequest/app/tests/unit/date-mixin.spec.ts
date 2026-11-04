import Vue from 'vue'
import { shallowMount } from '@vue/test-utils'
import MixinTester from '../mixin-tester.vue'

describe('Date Mixin', () => {
  let vm: any

  beforeAll(async () => {
    // mount the component and wait for everything to stabilize
    const wrapper = shallowMount(MixinTester, {
      computed: {
        getCurrentJsDate: () => new Date('2021-01-20')
      }
    })
    vm = wrapper.vm
    await Vue.nextTick()
  })

  it('returns correct values for createUtcDate()', () => {
    expect(vm.createUtcDate(2021, 0, 1, 0, 0).toISOString()).toBe('2021-01-01T08:00:00.000Z')
    expect(vm.createUtcDate(2021, 6, 1, 0, 0).toISOString()).toBe('2021-07-01T07:00:00.000Z')
    expect(vm.createUtcDate(2026, 0, 15, 0, 0).toISOString()).toBe('2026-01-15T08:00:00.000Z')
    expect(vm.createUtcDate(2026, 10, 2, 0, 0).toISOString()).toBe('2026-11-02T07:00:00.000Z')
  })

  it('returns correct values for dateToYyyyMmDd()', () => {
    expect(vm.dateToYyyyMmDd(null)).toBeNull()
    expect(vm.dateToYyyyMmDd(new Date('not a date'))).toBeNull()
    // verify that GMT/UTC is correctly converted to Pacific
    expect(vm.dateToYyyyMmDd(new Date('2021-01-01 07:00:00 GMT'))).toBe('2020-12-31') // Standard Time
    expect(vm.dateToYyyyMmDd(new Date('2021-01-01 08:00:00 GMT'))).toBe('2021-01-01') // Standard Time
    expect(vm.dateToYyyyMmDd(new Date('2021-07-01 06:00:00 GMT'))).toBe('2021-06-30') // Daylight Time
    expect(vm.dateToYyyyMmDd(new Date('2021-07-01 07:00:00 GMT'))).toBe('2021-07-01') // Daylight Time
    expect(vm.dateToYyyyMmDd(new Date('2026-11-02T00:30:00Z'))).toBe('2026-11-01')
    expect(vm.dateToYyyyMmDd(new Date('2026-01-16T00:30:00Z'))).toBe('2026-01-15')
    expect(vm.dateToYyyyMmDd(new Date('2026-11-15T06:59:00Z'))).toBe('2026-11-14')
    // verify that Pacific is correctly converted to Pacific
    expect(vm.dateToYyyyMmDd(new Date('2021-01-01 00:00:00 PST'))).toBe('2021-01-01')
    expect(vm.dateToYyyyMmDd(new Date('2021-01-01 23:59:59 PST'))).toBe('2021-01-01')
    expect(vm.dateToYyyyMmDd(new Date('2021-07-01 00:00:00 PDT'))).toBe('2021-07-01')
    expect(vm.dateToYyyyMmDd(new Date('2021-07-01 23:59:59 PDT'))).toBe('2021-07-01')
    // verify that Eastern is correctly converted to Pacific
    expect(vm.dateToYyyyMmDd(new Date('2021-01-01 02:00:00 EST'))).toBe('2020-12-31')
    expect(vm.dateToYyyyMmDd(new Date('2021-01-01 03:00:00 EST'))).toBe('2021-01-01')
    expect(vm.dateToYyyyMmDd(new Date('2021-07-01 02:00:00 EDT'))).toBe('2021-06-30')
    expect(vm.dateToYyyyMmDd(new Date('2021-07-01 03:00:00 EDT'))).toBe('2021-07-01')
  })

  it('returns correct values for dateToPacificTime()', () => {
    expect(vm.dateToPacificTime(null)).toBeNull()
    expect(vm.dateToPacificTime(new Date('not a date'))).toBeNull()
    // verify that GMT/UTC is correctly converted to Pacific
    expect(vm.dateToPacificTime(new Date('2021-01-01 07:00:00 GMT'))).toBe('11:00 pm') // Standard Time
    expect(vm.dateToPacificTime(new Date('2021-01-01 08:00:00 GMT'))).toBe('12:00 am') // Standard Time
    expect(vm.dateToPacificTime(new Date('2021-07-01 06:00:00 GMT'))).toBe('11:00 pm') // Daylight Time
    expect(vm.dateToPacificTime(new Date('2021-07-01 07:00:00 GMT'))).toBe('12:00 am') // Daylight Time
    // verify that Pacific is correctly converted to Pacific
    expect(vm.dateToPacificTime(new Date('2021-01-01 00:00:00 PST'))).toBe('12:00 am')
    expect(vm.dateToPacificTime(new Date('2021-01-01 23:59:59 PST'))).toBe('11:59 pm')
    expect(vm.dateToPacificTime(new Date('2021-07-01 00:00:00 PDT'))).toBe('12:00 am')
    expect(vm.dateToPacificTime(new Date('2021-07-01 23:59:59 PDT'))).toBe('11:59 pm')
    // verify that Eastern is correctly converted to Pacific
    expect(vm.dateToPacificTime(new Date('2021-01-01 02:00:00 EST'))).toBe('11:00 pm')
    expect(vm.dateToPacificTime(new Date('2021-01-01 03:00:00 EST'))).toBe('12:00 am')
    expect(vm.dateToPacificTime(new Date('2021-07-01 02:00:00 EDT'))).toBe('11:00 pm')
    expect(vm.dateToPacificTime(new Date('2021-07-01 03:00:00 EDT'))).toBe('12:00 am')
  })

  it('returns correct values for dateToPacificDate()', () => {
    expect(vm.dateToPacificDate(null)).toBeNull()
    expect(vm.dateToPacificDate(new Date('not a date'))).toBeNull()
    // verify that GMT/UTC is correctly converted to Pacific
    expect(vm.dateToPacificDate(new Date('2021-01-01 07:00:00 GMT'))).toBe('December 31, 2020') // Standard Time
    expect(vm.dateToPacificDate(new Date('2021-01-01 08:00:00 GMT'))).toBe('January 1, 2021') // Standard Time
    expect(vm.dateToPacificDate(new Date('2021-07-01 06:00:00 GMT'))).toBe('June 30, 2021') // Daylight Time
    expect(vm.dateToPacificDate(new Date('2021-07-01 07:00:00 GMT'))).toBe('July 1, 2021') // Daylight Time
    // verify that Pacific is correctly converted to Pacific
    expect(vm.dateToPacificDate(new Date('2021-01-01 00:00:00 PST'))).toBe('January 1, 2021')
    expect(vm.dateToPacificDate(new Date('2021-01-01 23:59:59 PST'))).toBe('January 1, 2021')
    expect(vm.dateToPacificDate(new Date('2021-07-01 00:00:00 PDT'))).toBe('July 1, 2021')
    expect(vm.dateToPacificDate(new Date('2021-07-01 23:59:59 PDT'))).toBe('July 1, 2021')
    // verify that Eastern is correctly converted to Pacific
    expect(vm.dateToPacificDate(new Date('2021-01-01 02:00:00 EST'))).toBe('December 31, 2020')
    expect(vm.dateToPacificDate(new Date('2021-01-01 03:00:00 EST'))).toBe('January 1, 2021')
    expect(vm.dateToPacificDate(new Date('2021-07-01 02:00:00 EDT'))).toBe('June 30, 2021')
    expect(vm.dateToPacificDate(new Date('2021-07-01 03:00:00 EDT'))).toBe('July 1, 2021')
  })

  it('returns correct values for dateToPacificDateTime()', () => {
    expect(vm.dateToPacificDateTime(null)).toBeNull()
    expect(vm.dateToPacificDateTime(new Date('not a date'))).toBeNull()
    // verify some Standard times
    expect(vm.dateToPacificDateTime(new Date('2021-01-01 07:00:00 GMT')))
      .toBe('December 31, 2020 at 11:00 pm Pacific time')
    expect(vm.dateToPacificDateTime(new Date('2021-01-01 08:00:00 GMT')))
      .toBe('January 1, 2021 at 12:00 am Pacific time')
      // verify some Daylight times
    expect(vm.dateToPacificDateTime(new Date('2021-07-01 06:00:00 GMT')))
      .toBe('June 30, 2021 at 11:00 pm Pacific time')
    expect(vm.dateToPacificDateTime(new Date('2021-07-01 07:00:00 GMT')))
      .toBe('July 1, 2021 at 12:00 am Pacific time')
  })

  // FUTURE: this works locally but not in GHA; fix later
  it.skip('returns correct values for daysFromToday()', () => {
    expect(vm.daysFromToday(null)).toBeNaN()
    expect(vm.dateToPacificDateTime(new Date('not a date'))).toBeNaN()
    expect(vm.daysFromToday(new Date('2021-01-19'))).toBe(-1) // yesterday
    expect(vm.daysFromToday(new Date('2021-01-20'))).toBe(0) // today
    expect(vm.daysFromToday(new Date('2021-01-21'))).toBe(1) // tomorrow
  })
})
