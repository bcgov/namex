<template>
  <div class="relative inline-block">
    <!-- Tooltip Trigger -->
    <button
      class="text-blue-500 pl-4"
      @mouseover="showVersionNumbers = true"
      @mouseleave="showVersionNumbers = false"
    >
      ℹ️
    </button>

    <!-- Tooltip Content -->
    <section
      v-show="showVersionNumbers"
      class="absolute z-10 w-56 px-5 py-3 bg-gray-800 rounded-lg -translate-x-full top-[-3.5rem]"
    >
      <div class="text-xs text-white">
        Name Examination: {{ nameExaminationVersion }}
      </div>
      <div class="text-xs text-white">
        NameX: {{ nameXVersion }}
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import packageInfo from '~/package.json'
import { ref, onMounted } from 'vue'
import { getNamexApiVersion } from '~/util/namex-api'

const showVersionNumbers = ref(false)
const nameExaminationVersion = ref('')
const nameXVersion = ref('')

onMounted(async () => {
  nameExaminationVersion.value = packageInfo.version
  nameXVersion.value = await fetchNameXVersion()
})

const fetchNameXVersion = async (): Promise<string> => {
  try {
    const response = await getNamexApiVersion()
    if (!response.ok) throw new Error(`Fetch failed: ${response.statusText}`)

    const { API } = await response.json()
    return API.match(/\d+\.\d+\.\d+/)?.[0] || 'Unknown'

  } catch (error) {
    console.error('Error fetching NameX API version:', error)
    return 'Error'
  }
}

</script>
