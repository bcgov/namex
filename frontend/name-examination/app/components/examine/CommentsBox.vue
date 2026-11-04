<template>
  <div 
    class="flex flex-col space-y-2 overflow-auto"
    data-testid="commentsContainer"
  >
    <div
      class="comments-box-child flex flex-col rounded border border-gray-400 bg-white p-2 text-sm"
      v-for="comment in comments"
    >
      <p class="whitespace-pre-wrap">{{ comment.comment }}</p>
      <span class="font-bold">
        {{ comment.examiner }}
      </span>
      <span class="italic">
        {{ getFormattedDateWithTime(comment.timestamp) }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
/** Component for displaying a list of comments */
import type { Comment } from '~/types'
import { getFormattedDateWithTime } from '~/util/date'

defineProps<{
  comments: Array<Comment>
}>()
</script>
