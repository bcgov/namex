<template>
  <Popover v-slot="{ open }" class="relative">
    <div class="flex">
      <span class="inline-flex items-center font-bold">{{ title }}</span>
      <PopoverButton
        :class="open ? '' : 'text-opacity-90'"
        class="group ml-auto inline-flex rounded border border-gray-300 bg-white px-2 py-1 font-bold transition hover:bg-gray-200"
      >
        <PlusIcon
          :class="open ? 'rotate-45' : ''"
          class="h-5 w-5 transition duration-150 ease-in-out group-hover:text-opacity-80"
          aria-hidden="true"
        />
        <span>Show</span>
      </PopoverButton>
    </div>

    <transition
      enter-active-class="transition duration-50 ease-out"
      enter-from-class="translate-y-1 absolute opacity-0"
      enter-to-class="translate-y-0 absolute opacity-100"
      leave-active-class="transition duration-10 ease-in"
      leave-from-class="translate-y-0 absolute opacity-100"
      leave-to-class="translate-y-1 absolute opacity-0"
    >
      <div class="line-clamp-3" v-if="!open">
        <slot name="minimized"></slot>
      </div>
    </transition>

    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="translate-y-1 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-50 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-1 opacity-0"
    >
      <PopoverPanel
        class="relative z-10 mt-2 max-h-[60vh] w-full max-w-sm overflow-auto px-4 sm:px-0 lg:max-w-3xl"
      >
        <div
          class="h-full overflow-auto rounded border border-gray-400 bg-gray-50 p-3 shadow-xl"
        >
          <slot name="expanded"></slot>
        </div>
      </PopoverPanel>
    </transition>
  </Popover>
</template>

<script setup lang="ts">
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { PlusIcon } from '@heroicons/vue/24/outline'

defineProps<{
  title: string
}>()
</script>
