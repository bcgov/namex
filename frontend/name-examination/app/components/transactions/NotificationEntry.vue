<template>
  <div class="flex flex-col space-y-4 border-y px-8 py-4 text-sm">
    <div class="grid grid-cols-4 gap-y-1">
      <!-- Date/Time -->
      <span class="font-bold">Date/Time</span>
      <span v-if="!entry.resend_date"
            class="col-span-3">
          {{ eventDate }}
      </span>
      <span v-else> 
          {{ eventDate }}
      </span>
      <span v-if="entry.resend_date" class="font-bold"> Resend Date: </span>
      <span v-if="entry.resend_date">
          {{ entry.resend_date }}
      </span>

      <span class="font-bold">Notification Type</span>
      <span class="col-span-3">{{ entry.option }}</span>

      <!-- Subject -->
      <span class="font-bold">Subject</span>
      <span class="col-span-3">{{ entry.email?.content?.subject || 'N/A' }}</span>

      <!-- Recipients -->
      <span class="font-bold">Recipients</span>
      <span class="col-span-3">{{ entry.email?.recipients || 'N/A' }}</span>

      <!-- Attachments -->
      <span class="font-bold">Attachments</span>
      <span class="col-span-3">
        <span v-if="entry.email?.content.attachments">
          <span v-for="(attachment, index) in entry?.email?.content.attachments" :key="index">
            {{ attachment.fileName }}
          </span>
        </span>
        <span v-else>N/A</span>
      </span>

      <!-- Body (full width, plain text with line breaks) -->
      <span>
        <button
          class="text-blue-500 underline"
          @click="toggleBody"
        >
          {{ isBodyVisible ? 'Hide Email Body' : 'Show Email Body' }}
        </button>
      </span>
      <span class="col-span-3 flex justify-end">
        <button
          class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition"
          @click="onResend"
        >
          Resend
        </button>
      </span>
      <span class="col-span-4">
        <div v-if="isBodyVisible" class="mt-2 w-full break-words">
          <template v-if="entry.email?.content?.body">
            <div v-for="(line, idx) in entry.email.content.body.split('\n')" :key="idx">
              {{ line }}
            </div>
          </template>
          <template v-else>
            N/A
          </template>
        </div>
        <!-- Success popup/message -->
        <div
          v-if="resendSuccess"
          class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 z-50"
        >
          <div class="bg-white p-6 rounded shadow text-center">
            <div class="mb-4 text-black text-lg">
              The <span class="font-bold">{{ entry.option }}</span> notification has been pushed to the email queue successfully.
            </div>
            <button
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              @click="resendSuccess = false"
            >
              OK
            </button>
          </div>
        </div>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { DateTime } from 'luxon'
import { useTransactions } from '~/store/transactions'
import type { TransactionEntry } from '~/types'
import { getFormattedDateWithTimeAndZone } from '~/util/date'
import { resendNotification } from '~/util/namex-api'

const { entry } = defineProps<{
  entry: TransactionEntry
}>()

const transactions = useTransactions()

const eventDate = computed(() =>
  getFormattedDateWithTimeAndZone(DateTime.fromHTTP(entry.eventDate))
)

const isBodyVisible = ref(false)
const resendSuccess = ref(false)

function toggleBody() {
  isBodyVisible.value = !isBodyVisible.value
}

async function onResend() {
  try {
    const response = await resendNotification(entry.id)
    if (response.ok) {
      resendSuccess.value = true
    } else {
      // Try to parse error message from response body
      let errorMsg = 'Unknown error'
      try {
        const data = await response.json()
        errorMsg = data.message || errorMsg
      } catch {}
      alert('The notification resend failed: ' + errorMsg)
    }
  } catch (e) {
    alert('Resend failed!')
  }
}
</script>
