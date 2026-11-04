import { beforeEach, describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { useSearchStore } from '~/store/search'
import { clickDropdownOption } from '../util'
import SearchResultsControl from '~/components/search/ResultsControl.vue'
import { createTestingPinia } from '@pinia/testing'
import ListSelect from '~/components/ListSelect.vue'
import { ListboxButton } from '@headlessui/vue'
import IconButton from '~/components/IconButton.vue'
import ComboSelect from '~/components/ComboSelect.vue'

describe('Search Page', () => {
  let wrapper: any
  let search: any

  beforeEach(() => {
    const pinia = createTestingPinia({
      stubActions: false,
      createSpy: vi.fn,
    })
    wrapper = mount(SearchResultsControl, {
      global: {
        plugins: [pinia],
      },
    })
    search = useSearchStore()
  })

  it('resets the filters', async () => {
    search.resetFilters = vi.fn()
    search.resetDisplayAndPage = vi.fn()

    await wrapper
      .findWithText((wrapper.vm as any).CLEAR_FILTERS_TEXT)
      .trigger('click')
    expect(search.resetFilters).toHaveBeenCalled()
    expect(search.resetDisplayAndPage).toHaveBeenCalled()
  })

  it('sets the selected columns correctly when they are changed', async () => {
    const columnsDropdown = wrapper.findAllComponents(ListSelect)[0]
    expect(columnsDropdown).toBeDefined()

    await columnsDropdown.findComponent(ListboxButton).trigger('click')

    // Gradually disable every column and check if the selected columns are updated accordingly.
    const excluded = []
    for (const column of search.fixedColumns) {
      await columnsDropdown.findWithText(column).trigger('click')
      excluded.push(column)
      expect(
        excluded.every((c) => !search.selectedColumns.includes(c))
      ).toBeTruthy()
    }
  })

  it('sets the display count', async () => {
    const displayDropdown = wrapper.findAllComponents(ListSelect)[1]
    expect(displayDropdown.exists()).toBe(true)

    await clickDropdownOption(displayDropdown, '10')
    expect(search.selectedDisplay).toBe(10)
  })

  it('has a page number combo select', async () => {
    const pageDropdown = wrapper.findComponent(ComboSelect)
    expect(pageDropdown.exists()).toBe(true)

    search.selectedDisplay = 10
    search.resultNum = 100

    const expectedOptions = Array.from({ length: 10 }, (_, key) => key + 1)
    expect(pageDropdown.vm.filteredOptions).toEqual(expectedOptions)
  })

  it('goes to the previous page when the previous button is pressed', async () => {
    search.goToPreviousPage = vi.fn()

    const previousPageButton = wrapper.findAllComponents(IconButton)[0]
    await previousPageButton.trigger('click')
    expect(search.goToPreviousPage).toHaveBeenCalled()
  })

  it('goes to the next page when the next button is pressed', async () => {
    search.goToNextPage = vi.fn()

    const nextPageButton = wrapper.findAllComponents(IconButton)[1]
    await nextPageButton.trigger('click')
    expect(search.goToNextPage).toHaveBeenCalled()
  })
})
