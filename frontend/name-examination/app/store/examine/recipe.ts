import type { ConflictList, ConflictListItem } from '~/types'
import { useConflicts } from './conflicts'
import { emitter } from '~/util/emitter'
import { clamp, isConflictList, isConflictListItem } from '~/util'

export const useExaminationRecipe = defineStore('examine-recipe', () => {
  const CAPTURED_KEYS = [
    'ArrowDown',
    'ArrowUp',
    'ArrowRight',
    'ArrowLeft',
    'Space',
    'Enter',
  ]

  const CONFLICTS_AREA_ID = 'conflicts-tab'

  const conflicts = useConflicts()

  /** Index of currently selected tab in the recipe area. */
  const currentRecipeTabIndex = ref(0)

  /** The object which is currently being focused in the recipe area */
  const focused = ref<ConflictListItem | ConflictList>()

  /** Object that was being focused before focus was lost */
  const savedFocus = ref<ConflictListItem | ConflictList>()

  /** Return all non-empty `ConflictList`s and `ConflictListItem`s in one flattened list, in order. */
  const allObjects = computed<Array<ConflictListItem | ConflictList>>(() => {
    return [
      ...conflicts.exactMatches,
      ...conflicts.nonEmptyLists.map((list) => [list, ...list.children]).flat(),
    ]
  })

  /** Array of objects that contains all exact matched `ConflictListItem`s as well as all non-empty conflict lists.  */
  const topLevelObjects = computed<Array<ConflictListItem | ConflictList>>(
    () => [...conflicts.exactMatches, ...conflicts.nonEmptyLists]
  )

  /** Maps every `ConflictListItem` to its parent `ConflictList` if it exists. */
  const conflictListMap = computed<
    Map<ConflictListItem, ConflictList | undefined>
  >(() => {
    const map = new Map<ConflictListItem, ConflictList | undefined>()
    let currentList: ConflictList | undefined = undefined
    for (const obj of allObjects.value) {
      if (isConflictList(obj)) {
        currentList = obj
      } else {
        map.set(obj, currentList)
      }
    }
    return map
  })

  /** Initialize focus for the entire recipe area */
  function focusArea() {
    document.getElementById(CONFLICTS_AREA_ID)?.focus({ preventScroll: true })
    if (focused.value) {
      return
    } else if (savedFocus.value) {
      setNewFocus(savedFocus.value)
      savedFocus.value = undefined
    } else {
      setNewFocus(conflicts.firstConflictItem)
    }
  }

  /** Unfocus the entire recipe area */
  function unfocusArea() {
    savedFocus.value = focused.value
    setNewFocus(undefined)
  }

  /** Simulate clicking the given conflict object in the conflict area.
   * This method is usually only called externally when the user clicks a list/item.
   * @param toggleOpen whether the object should only be focused, or if it's `open` state should be toggled as well. Defaults to `true`. */
  function clickObject(
    obj: ConflictListItem | ConflictList,
    toggleOpen = true
  ) {
    if (savedFocus.value) setNewFocus(savedFocus.value)
    focusArea()
    if (obj !== focused.value) collapseFocusedIfConflictItem()
    setNewFocus(obj)
    if (!toggleOpen) return
    if (obj.ui.open) {
      collapseFocused()
    } else {
      expandFocused(false)
    }
  }

  /** Expand the currently focused object.
   * @param scrollInstant whether to scroll to the expanded object instantly. Defaults to `true`.
   */
  function expandFocused(scrollInstant = true) {
    if (!focused.value) return
    if (isConflictList(focused.value)) {
      collapseAllLists()
    }
    focused.value.ui.open = true
    scrollToFocused(scrollInstant)
  }

  function collapseAllLists() {
    conflicts.nonEmptyLists.forEach((list) => (list.ui.open = false))
  }

  /** Collapse the given object.
   * If the focused object is a `ConflictList`, then all other conflict lists will also be collapsed.*/
  function collapseObject(obj: ConflictListItem | ConflictList) {
    if (isConflictList(obj)) {
      collapseAllLists()
    } else {
      obj.ui.open = false
    }
  }

  /** Collapse the currently focused object.
   * If the focused object is a `ConflictList`, then all other conflict lists will also be collapsed.*/
  function collapseFocused() {
    if (focused.value) collapseObject(focused.value)
  }

  /** Handle the user requesting the current object to be collapsed. */
  function handleCollapse() {
    if (!focused.value) return
    if (!focused.value.ui.open && isConflictListItem(focused.value)) {
      if (conflicts.exactMatches.includes(focused.value)) return
      const parentConflictList = conflictListMap.value.get(focused.value)
      setNewFocus(parentConflictList)
    }
    collapseFocused()
    scrollToFocused()
  }

  /** If the current focused object is a `ConflictListItem`, collapse it. */
  function collapseFocusedIfConflictItem() {
    if (focused.value && isConflictListItem(focused.value)) {
      collapseFocused()
    }
  }

  /** Selects the currently focused object if it's a `ConflictListItem`. Otherwise, does nothing. */
  function selectFocusedConflict() {
    if (focused.value && isConflictListItem(focused.value)) {
      conflicts.toggleConflict(focused.value)
    }
  }

  /** Scroll to the focused element
   * @param instant whether to scroll to the focused object instantly
   */
  function scrollToFocused(instant: boolean = false) {
    if (focused.value) {
      emitter.emit('scrollToConflictObject', { obj: focused.value, instant })
    }
  }

  /** Get the next/previous non-empty `ConflictList` or exact match `ConflictListItem` relative
   * to the given conflict object. */
  function getRelativeTopLevelObject(
    obj: ConflictList | ConflictListItem,
    delta: number
  ) {
    const currentIndex = topLevelObjects.value.indexOf(obj)
    const maxIndex = topLevelObjects.value.length - 1
    const newIndex = clamp(currentIndex + delta, 0, maxIndex)
    return topLevelObjects.value[newIndex]
  }

  function setNewFocus(focus: ConflictList | ConflictListItem | undefined) {
    if (focused.value) {
      focused.value.ui.focused = false
    }
    focused.value = focus
    if (focused.value) {
      focused.value.ui.focused = true
    }
  }

  /** Focus a new object relative to the currently focused element.
   * If no object is currently focused, a default item will be selected. */
  function focusRelative(delta: number) {
    if (!focused.value) {
      setNewFocus(conflicts.firstConflictItem)
      return
    }
    collapseFocusedIfConflictItem()
    if (
      isConflictList(focused.value) &&
      (!focused.value.ui.open || delta < 0)
    ) {
      setNewFocus(getRelativeTopLevelObject(focused.value, delta))
    } else {
      const currIndex = allObjects.value.indexOf(focused.value)
      const maxIndex = allObjects.value.length - 1
      const newIndex = clamp(currIndex + delta, 0, maxIndex)
      setNewFocus(allObjects.value[newIndex])
    }
    collapseFocused()
    scrollToFocused()
  }

  /** Handle a keydown keyboard event in the recipe area. */
  function handleKeyDown(event: KeyboardEvent) {
    switch (event.code) {
      case 'ArrowDown':
        focusRelative(1)
        break
      case 'ArrowUp':
        focusRelative(-1)
        break
      case 'ArrowRight':
        expandFocused()
        break
      case 'ArrowLeft':
        handleCollapse()
        break
      case 'Space':
        selectFocusedConflict()
        break
    }
    if (CAPTURED_KEYS.includes(event.code)) {
      event.preventDefault()
    }
  }

  /** Reset this store's state */
  function reset() {
    focused.value = undefined
    savedFocus.value = undefined
  }

  emitter.on('recipeTabChanged', (newIndex) => {
    currentRecipeTabIndex.value = newIndex
  })

  return {
    CONFLICTS_AREA_ID,
    currentRecipeTabIndex,
    focused,
    focusArea,
    unfocusArea,
    clickObject,
    handleKeyDown,
    reset,
  }
})
