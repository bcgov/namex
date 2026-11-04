<template>
  <div>
    <Listbox
      :modelValue="modelValue"
      @update:modelValue="updateModelValue"
      :multiple="multiple"
      :disabled="disabled"
      v-slot="{ open }"
    >
      <div class="relative w-full">
        <ListboxButton
          ref="listboxButton"
          class="relative w-full rounded border border-gray-300 bg-white py-1.5 pl-3 pr-10 text-left transition sm:text-sm"
          :class="{
            'hover:bg-gray-100': !disabled,
            'pointer-events-none text-gray-400': disabled,
            'border-2 border-red-600': errorStyle,
          }"
          :data-testid="testID"
        >
          <span class="block"><slot>Select</slot></span>
          <span class="absolute inset-y-0 right-0 flex items-center pr-3">
            <ChevronDownIcon
              class="mt-0.5 h-5 transition"
              :class="open ? 'rotate-180' : ''"
              aria-hidden
            />
          </span>
        </ListboxButton>

        <transition
          leave-active-class="transition duration-100 ease-in"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
          enter-active-class="transition duration-50 ease-in"
          enter-from-class="opacity-0"
          enter-to-class="opacity-100"
        >
          <ListboxOptions
            class="absolute z-20 mt-1 max-h-[50vh] w-fit overflow-auto rounded bg-white py-1 text-left text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
            :class="optionsStyle"
          >
            <ListboxOption
              v-slot="{ active, selected }"
              v-for="option in options"
              v-if="options.length > 0"
              :key="option"
              :value="option"
              as="template"
            >
              <li
                :class="[
                  active ? 'bg-amber-100 text-amber-900' : 'text-gray-900',
                  'relative w-full cursor-default select-none truncate py-2 pl-10 pr-4',
                ]"
              >
                <span>
                  {{ optionsDisplay ? optionsDisplay(option) : option }}
                </span>
                <span
                  v-if="selected"
                  class="absolute inset-y-0 left-0 flex items-center pl-3 text-amber-600"
                >
                  <CheckIcon class="h-5" />
                </span>
              </li>
            </ListboxOption>

            <div v-else class="px-2 py-1">
              <slot name="no-data">Nothing found</slot>
            </div>
          </ListboxOptions>
        </transition>
      </div>
    </Listbox>
  </div>
</template>

<script setup lang="ts">
/**
 * A dropdown menu to select an item from a list of options.
 */
import {
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
} from '@headlessui/vue'
import { ChevronDownIcon, CheckIcon } from '@heroicons/vue/24/outline'

type ModelValueType = any
const props = defineProps<{
  modelValue: ModelValueType | Array<ModelValueType>
  options: Array<any>
  /** Whether multiple options can be selected */
  multiple?: boolean
  /** Only applies if `multiple` prop is also passed in. Close the `ListSelect` when an option is [de]selected.*/
  closeOnSelect?: boolean
  /** Whether the component is disabled (can't be clicked, grayed out) */
  disabled?: boolean
  optionsStyle?: string
  /** Function called for getting a display string for a given option */
  optionsDisplay?: (option: ModelValueType) => string
  /** Style this input to indicate an error, useful to indicate invalid inputs */
  errorStyle?: boolean
  testID?: string
}>()

const emit = defineEmits<{
  (e: 'change', option: any): void
  (e: 'update:modelValue', newValue: any): void
}>()

const listboxButton = ref<InstanceType<typeof ListboxButton>>()

const updateModelValue = (newValue: any) => {
  emit('update:modelValue', newValue)
  emit('change', newValue)
  // close the listbox when an option is selected/deselected even when multiple options can be selected
  if (props.multiple && props.closeOnSelect) {
    listboxButton.value?.$el.click()
  }
}
</script>
