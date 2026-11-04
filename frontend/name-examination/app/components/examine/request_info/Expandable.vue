<template>
  <div class="rounded text-sm">
    <!-- Editable state -->
    <div class="space-y-1" v-if="examine.isEditing">
      <h2 class="font-bold">{{ title }}</h2>
      <slot name="editable"><slot></slot></slot>
    </div>

    <div class="space-y-1" v-else-if="examine.isHeaderShown">
      <h2 class="font-bold">{{ title }}</h2>
      <slot name="maximized"><slot></slot></slot>
    </div>

    <ExamineRequestInfoPopover :title="title" v-else>
      <template #minimized>
        <slot name="minimized"><slot></slot></slot>
      </template>
      <template #expanded>
        <slot name="popup"><slot></slot></slot>
      </template>
    </ExamineRequestInfoPopover>
  </div>
</template>

<script setup lang="ts">
/** A component that displays content in three different states (editable, maximized, minimzed)
 * depending on the global UI state. If a default template is passed in, it will be used for all states.
 */
import { useExamination } from '~/store/examine'
const examine = useExamination()

defineProps<{
  title: string
}>()
</script>
