<template>
  <nav
    id="app-header"
    class="sticky top-0 z-50 h-16 border-b border-gray-300 bg-white"
  >
  <div class="flex h-full w-full items-center justify-between">
      <div class="hidden h-full lg:block">
        <nuxt-link :to="Route.Home" data-testid="homeLink">
          <img
            src="/images/top-nav.png"
            class="min-w-8 h-full"
            alt="Name Examination"
          />
        </nuxt-link>
      </div>

      <div class="text-bcgov-blue5 ml-3 flex gap-10">
        <AppHeaderNavLink
          text="Admin"
          :route="adminURL"
          target="_blank"
          data-testid="adminLink"
        />
        <AppHeaderNavLink
          text="Examine Names"
          :route="Route.Examine"
          data-testid="examineLink"
        />
        <AppHeaderNavLink
          text="Search"
          :route="Route.Search"
          data-testid="searchLink"
        />
        <AppHeaderNavLink
          text="Stats"
          :route="Route.Stats"
          data-testid="statsLink"
        />
      </div>

      <div class="ml-auto flex items-center">
        <SearchInput
          v-model="searchText"
          class="mx-3"
          data-testid="searchNRNumberField"
          placeholder="Search NR Number"
          input-required
          @submit.prevent="onSearchSubmit"
        />

        <div class="flex space-x-2 px-3">
          <ToggleSwitch
            label="Priority Queue"
            data-testid="prioritySwitch"
            :modelValue="queueToggleVal"
            @update:modelValue="togglePriorityQueue"
          />
        </div>

        <div class="flex flex-col border-l-2 border-gray-300 px-3">
          <span class="text-sm">{{ $userProfile.username }}</span>
          <a
            class="text-sm text-blue-800"
            href="#"
            data-testid="logOut"
            @click="$auth.logout()"
          >
            Log Out
          </a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { Route } from '~/enums/routes'
import { useExamination } from '~/store/examine'
import { emitter } from '~/util/emitter'
import { useExaminationOptions } from '~/store/examine/options'

const { $auth, $userProfile } = useNuxtApp()

const config = useRuntimeConfig()
const adminURL = config.public.namexAdminURL

const examine = useExamination()

const searchText = ref('')

const examineOptions = useExaminationOptions()
const { priorityQueue, updatePriority } = examineOptions
const queueToggleVal = ref(priorityQueue)

/** Parse the input as an NR number, tries to return a string in the form 'NR x' where 'x' is a number. */
function parseNrNumber(input: string) {
  const regex = /(^|\D)(\d{7})(\D|$)/ // any 7 digit number not in another number
  const match = regex.exec(input)?.at(2)
  if (!match) return undefined
  return `NR ${match}`
}

async function onSearchSubmit(_: Event) {
  const nrNumber = parseNrNumber(searchText.value)
  try {
    if (!nrNumber) throw new Error('Failed to parse NR number from input')
    searchText.value = ''
    await examine.initialize(nrNumber)
  } catch (e: any) {
    emitter.emit('error', {
      title: 'Failed to search NR',
      message: e,
    })
  }
}

function togglePriorityQueue(newValue: boolean) {
  queueToggleVal.value = newValue
  updatePriority(newValue)
}
</script>
