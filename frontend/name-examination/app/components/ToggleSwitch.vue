<template>
  <SwitchGroup>
    <div class="flex items-center">
      <Switch :modelValue="modelValue" @update:modelValue="updateModelValue">
        <button
          class="relative inline-flex h-6 w-11 items-center rounded-full transition"
          :class="
            modelValue ? 'bg-bcgov-blue5 hover:opacity-90' : 'bg-gray-200'
          "
        >
          <span
            :class="modelValue ? 'translate-x-6' : 'translate-x-1'"
            class="inline-block h-4 w-4 transform rounded-full bg-white transition"
          />
        </button>
      </Switch>
      <SwitchLabel class="ml-1">{{ label }}</SwitchLabel>
    </div>
  </SwitchGroup>
</template>

<script setup lang="ts">
/** Input for choosing between an on/off state. */
import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'

defineProps<{
  /** Switch's true/false state*/
  modelValue: boolean
  /** Text shown next to switch */
  label: string
}>()

const emit = defineEmits()
const updateModelValue = (newValue: any) => {
  emit('update:modelValue', newValue)
}
</script>
