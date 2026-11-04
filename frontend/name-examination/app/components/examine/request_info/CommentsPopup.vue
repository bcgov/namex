<template>
  <div class="w-full max-w-sm">
    <Popover v-slot="{ open }" class="relative">
      <PopoverButton
        ref="popoverButton"
        :class="open ? '' : 'text-opacity-90'"
        class="group inline-flex w-full items-center space-x-2 rounded border border-gray-300 bg-white px-3 py-1.5 font-bold text-black transition hover:bg-gray-200"
        data-testid="commentsPopupBtn"
      >
        <ChatBubbleLeftIcon class="h-5 w-5" />
        <span class="grow text-left">
          {{ comments.length }} C<u>o</u>mment{{
            comments.length > 1 ? 's' : ''
          }}
        </span>
        <ChevronDownIcon
          :class="open ? 'rotate-180' : ''"
          class="h-5 w-5 transition duration-150 ease-in-out group-hover:text-opacity-80"
          aria-hidden
        />
      </PopoverButton>

      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="translate-y-1 opacity-0"
        enter-to-class="translate-y-0 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="translate-y-0 opacity-100"
        leave-to-class="translate-y-1 opacity-0"
      >
        <PopoverPanel
          v-slot="{ close }"
          class="absolute z-10 mt-3 h-fit w-80 max-w-sm transform px-4 sm:px-0 lg:max-w-3xl"
        >
          <div
            class="h-full overflow-auto rounded border border-gray-400 shadow-xl"
          >
            <div
              class="flex h-full flex-col space-y-1 divide-y-2 divide-gray-300 bg-gray-100 p-3"
            >
              <div>
                <EditableTextBox
                  class="h-48"
                  v-model="commentText"
                  placeholder="Create a new comment..."
                  submit-mnemonic="v"
                  text-required
                  @submit="onSubmit"
                  @cancel="onCancel(close)"
                  testID="commentEditableTxtBox"
                >
                  <template #submitText>
                    <span>Sa<u>v</u>e</span>
                  </template>
                  <template #errorText>A comment is required</template>
                </EditableTextBox>
              </div>

              <ExamineCommentsBox
                v-if="comments.length > 0"
                class="max-h-72 pt-1"
                :comments="comments"
              />
            </div>
          </div>
        </PopoverPanel>
      </transition>
    </Popover>
  </div>
</template>

<script setup lang="ts">
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'
import { ChatBubbleLeftIcon } from '@heroicons/vue/24/outline'
import { useExamination } from '~/store/examine'
import { parseDate } from '~/util/date'

const examine = useExamination()

const popoverButton = ref<HTMLButtonElement | null>(null)
const buttonElem = computed(
  () => (popoverButton.value as any).el as HTMLButtonElement
)
useMnemonic('o', () => buttonElem.value.click())

const commentText = ref('')

const comments = computed(() =>
  examine.comments.sort(
    (a, b) =>
      parseDate(b.timestamp).toMillis() - parseDate(a.timestamp).toMillis()
  )
)

async function onSubmit(text: string) {
  await examine.postComment(text)
  commentText.value = ''
}

function onCancel(closeFunction: () => void) {
  closeFunction()
  commentText.value = ''
}
</script>
