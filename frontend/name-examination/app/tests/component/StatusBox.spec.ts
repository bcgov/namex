import { beforeEach, describe, it, expect, vi } from 'vitest'
import { VueWrapper, mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { useStatusStore } from '~/store/status'
import StatusBox from '~/components/StatusBox.vue'
import flushPromises from 'flush-promises'
/* eslint-disable require-jsdoc */

describe('Stats', () => {
  let wrapper: VueWrapper<any, any>
  let status = useStatusStore()

  beforeEach(() => {
    wrapper = mount(StatusBox, {
      global: {
        plugins: [createTestingPinia({ createSpy: vi.fn })],
      },
    })
    status = useStatusStore()
  })

  it('shows the correct date', () => {
    expect(wrapper.find('#date').text()).toBe(status.todayStr)
  })

  it('shows the correct hold number', async () => {
    const expected = 1378
    status.holdNum = expected
    await flushPromises()
    expect(wrapper.find('#hold').text()).toBe(expected.toString())
  })

  it('shows the examined number', async () => {
    const expected = 15691
    status.notExaminedNum = expected
    await flushPromises()
    expect(wrapper.find('#notExamined').text()).toBe(expected.toString())
  })
})
