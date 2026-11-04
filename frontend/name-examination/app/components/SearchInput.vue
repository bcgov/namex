<template>
  <form ref="searchForm" class="flex items-center" role="search">
    <div class="relative flex w-full">
      <input
        :id="inputId"
        ref="searchTextField"
        type="text"
        class="w-full rounded-l border border-gray-300 px-2 py-1 text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-blue-500"
        :placeholder="placeholder"
        :value="modelValue"
        @input="onInput"
        autocorrect="off"
        :required="inputRequired"
        aria-label="Search"
      />
      <IconButton
        v-if="showClear"
        type="button"
        @click="onClear"
        white
        class="absolute right-1 top-[2.5px] border-0 !p-1"
        aria-label="Reset search input"
      >
        <ArrowUturnLeftIcon class="h-5 w-5" />
      </IconButton>
    </div>
    <IconButton
      class="rounded-none rounded-r !border border-bcgov-blue5 !p-1.5"
      aria-label="Submit search"
    >
      <MagnifyingGlassIcon class="h-5 w-5 stroke-2" />
    </IconButton>
  </form>
</template>

<script setup lang="ts">
/** Component for inputting a search query. */
import {
  ArrowUturnLeftIcon,
  MagnifyingGlassIcon,
} from '@heroicons/vue/24/outline'

const props = defineProps<{
  modelValue: string
  placeholder?: string
  /** Mnemonic letter for focusing the search's input field. */
  focusMnemonic?: string
  /** Show clear buttons in the search input if the input text does not match the given string. */
  clear?: string
  /** Whether the search input is required (non-empty) for submitting. */
  inputRequired?: boolean
  /** Value for the id attribute for the actual `input` element */
  inputId?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', newValue: any): void
}>()

const searchTextField = ref<HTMLInputElement | null>(null)
const searchForm = ref<HTMLFormElement | null>(null)

const showClear = ref(false)

function onInput(event: Event) {
  const text = (event.target as HTMLInputElement).value
  emit('update:modelValue', text)
  showClear.value = props.clear !== undefined && text !== props.clear
}

function onClear() {
  emit('update:modelValue', props.clear)
  searchForm.value?.requestSubmit()
  showClear.value = false
}

onMounted(() => {
  if (props.focusMnemonic) {
    useMnemonic(props.focusMnemonic, () => searchTextField.value?.focus())
  }
})
</script>
