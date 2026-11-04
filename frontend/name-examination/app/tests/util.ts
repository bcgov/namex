import { DOMWrapper, VueWrapper } from '@vue/test-utils'
import flushPromises from 'flush-promises'
import { vi } from 'vitest'

const namexApiModule = await import('~/util/namex-api')

/**
 * Click the given dropdown and choose a given option
 */
export async function clickDropdownOption(
  dropdown: DOMWrapper<any> | VueWrapper<any>,
  option: string
) {
  const dropdownButton = dropdown.find('button')
  await dropdownButton.trigger('click')

  const dropdownOption = dropdown.findWithText(option)
  await dropdownOption.trigger('click')

  await flushPromises()
}

/**
 * Set the return value of the next call to backend api call helper.
 * This can be used to simulate the return value from an api call.
 */
export function mockNextApiHelperResponse(data: any) {
  namexApiModule.getNamexObject = vi.fn().mockResolvedValueOnce(data)
}

export function setApiHelperImpl(callback: (url: URL) => Promise<any>) {
  namexApiModule.getNamexObject = vi.fn().mockImplementation(callback)
}
