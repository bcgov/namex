import { Route } from '~/enums/routes'
import { useExamination } from '.'
import { useExaminationRecipe } from './recipe'
import { getCircularIndex } from '~/util'

/** Handles tabbing through elements in the Examine page. */
export const useExaminationTabCyle = defineStore('examine-tab-cycle', () => {
  /** Array of element ids */
  const elements = ref<Array<string>>([])
  const focused = ref(-1)
  const examine = useExamination()

  /** Register an element to be a part of the tab cycle. */
  function register(index: number, elementId: string) {
    if (index > elements.value.length - 1) {
      elements.value.length = index + 1
    }
    if (elements.value[index] && elements.value[index] !== elementId) {
      console.warn(
        `Overwriting previously registered tab cycle item '${elements.value[index]}' with '${elementId}' at index ${index}`
      )
    }
    elements.value[index] = elementId
  }

  /** Returns whether the given `KeyboardEvent` should be handled or not. */
  function shouldHandleKeyEvent(event: KeyboardEvent) {
    const route = useRoute().path.toString().toLowerCase()
    return (
      route === Route.Examine &&
      useExaminationRecipe().currentRecipeTabIndex === 0 && // if the conflicts tab is not selected, do not handle any key presses
      event.code === 'Tab' &&
      !examine.isEditing
    )
  }

  /** Update the focused element if it was changed through some means other than the tab key. */
  function syncFocusedElement() {
    const activeElemId = document.activeElement?.id || ''
    const activeElemIndex = elements.value.indexOf(activeElemId)
    if (activeElemIndex !== -1) {
      focused.value = activeElemIndex
    }
  }

  /** Focus the next element relative to the currently focused element. */
  function focusNext(delta: number) {
    focused.value = getCircularIndex(
      focused.value + delta,
      elements.value.length
    )
    document
      .getElementById(elements.value[focused.value])
      ?.focus({ preventScroll: true })
  }

  function handleKeyUp(event: KeyboardEvent) {
    if (!shouldHandleKeyEvent(event)) return
    syncFocusedElement()
    focusNext(event.shiftKey ? -1 : 1)
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (!shouldHandleKeyEvent(event)) return
    event.preventDefault()
  }

  document.addEventListener('keyup', handleKeyUp)
  document.addEventListener('keydown', handleKeyDown)

  return { register }
})
