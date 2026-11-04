<template>
  <div id="stats-viewer" class="mx-4 mt-4 flex h-[91vh] flex-col space-y-1">
    <div class="stats-header">
      <h1 class="text-2xl font-bold text-gray-700">
        Statistics
      </h1>
    </div>
    <div class="flex items-center justify-between">
      &nbsp;
      <div class="font-semibold text-center">Total Examined Names: {{ numRecords }}</div>
      <div class="flex items-center space-x-2">
        <div class="flex items-center space-x-1">
          <input
            id="stats-checkbox"
            class="h-4 w-4"
            v-model="myStats"
            type="checkbox"
            data-testid="statsCheckbox"
          >
          <label for="stats-checkbox" class="font-bold">My Stats</label>
        </div>
        <div class="timespan-input  align-baseline space-x-1">
          <label for="timespan" class="font-bold align-baseline">Hours:&nbsp;</label>
          <TextInput
            id="timespan"
            ref="numberinput"
            v-model="timespan"
            type="number"
            class="!w-24"
            data-testid="statsHoursInput"
          />
          <IconButton @click="fetchStats" data-testid="getStatsBtn">
            Get Stats
          </IconButton>
        </div>
      </div>
    </div>

    <div class="h-full overflow-x-auto rounded border">
      <table class="min-h-fit min-w-full table-auto" data-testid="statsTable">
        <thead class="sticky top-0">
          <tr class="h-12 bg-bcgov-blue5 text-left text-sm text-white">
            <th v-for="(header, index) in fields" :key="index" class="border-b border-gray-200 px-2 py-1">
              {{ header.label }}
            </th>
          </tr>
        </thead>
        <tbody v-if="!isLoading" class="text-sm">
          <tr v-for="(item, index) in statsData" :key="index"
            class="align-top transition duration-200 ease-in-out border-b border-gray-300 hover:bg-gray-200">
            <td class="whitespace-pre-line border-b border-gray-300 px-2 py-2">
              <span class="container-fluid">
                <span class="layout">
                  <span class="flex my-2 font-bold">
                    {{ item.nrNum }}
                  </span>
                </span>
                <span v-for="(name, i) in item.names" :key="`names-layout-${i}`">
                  <span class="flex font-bold">
                    {{ i + 1 }}. {{ name.name }}
                    <span class="mx-2" :class="getClass(name.state)">
                      {{ name.state }}
                    </span>
                  </span>
                  <span class="layout">
                    <span v-for="(text, j) in name.decision_text" :key="`decision-text-flex-${j}`"
                      class="flex italic mb-2 ml-4">
                      {{ text }}
                    </span>
                  </span>
                </span>
                <span v-if="item.comments.length > 0" class="ml-2 mt-1 font-semibold">
                  LAST COMMENT
                </span>
                <span v-if="item.comments.length > 0" class="dk-grey ml-2 mb-2">
                  <span class="flex indent-10px">
                    {{ item.comments[0].comment }}
                  </span>
                  <span class="flex ft-ital indent-10px">
                    <template v-if="item.comments[0].examiner">
                      <template v-for="(value, name) in item.comments[0].examiner">
                        -{{ name }}: {{ value }},
                      </template>
                    </template>
                    <template v-else>
                      <span class="mr-2">–unknown examiner,</span>
                    </template>
                    {{ item.comments[0].timestamp }}
                  </span>
                </span>
              </span>
            </td>
            <td :class="getClass(item.stateCd)" class="font-semibold">
              {{ item.stateCd }}
            </td>
            <td>{{ item.lastUpdate }}</td>
            <td>{{ item.activeUser }}</td>
            <td>{{ item.furnished }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="isLoading"
           class="absolute bottom-1/2 right-1/2 translate-x-1/2 translate-y-1/2 transform">
        <LoadingSpinner />
      </div>

    </div>
  </div>
</template>

<script>
import { useStatsStore } from '~/store/stats.ts'
import { ref, onMounted } from 'vue'

export default {
  setup() {
    const timespan = ref('24')
    const numberinput = ref(null)
    const numRecords = ref(0)
    const myStats = ref(true)
    const statsData = ref([])
    const isLoading = ref(false)

    const stats = useStatsStore()

    const fields = [
      {
        key: 'nrdetails',
        label: 'Request Details',
        style: { width: '64%' }
      },
      {
        key: 'stateCd',
        label: 'Status',
        style: { width: '7%' }
      },
      {
        key: 'lastUpdate',
        label: 'Last Update',
        style: { width: '14%' }
      },
      {
        key: 'activeUser',
        label: 'Active User',
        style: { width: '10%' }
      },
      {
        key: 'furnished',
        label: 'Back to NRO?',
        style: { width: '5%' }
      }
    ]

    const fetchStats = async () => {
      try {
        isLoading.value = true

        const jsonData = await stats.getPagedStats(timespan.value, myStats.value)
        numRecords.value = jsonData.numRecords
        statsData.value = jsonData.nameRequests

        isLoading.value = false
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }

    onMounted(async () => {
      await fetchStats()
    })

    /**
     * Determines the CSS class based on the provided state.
     * @param {string} state - The state value used to determine the CSS class.
     * @return {string | undefined} Returns the CSS class corresponding to the provided state.
     * If the state does not match any condition, returns undefined.
     */
    function getClass(state) {
      if (state === 'APPROVED') {
        return 'approved'
      }
      if (state === 'REJECTED') {
        return 'rejected'
      }
      if (state === 'CONDITION' || state === 'CONDITIONAL') {
        return 'condition'
      }
    }

    return {
      fields,
      myStats,
      numRecords,
      timespan,
      statsData,
      numberinput,
      isLoading,
      getClass,
      fetchStats
    }
  }
}
</script>

<style scoped>
/* Add your scoped styles here */
.stats-header {
  padding: 3px;
  display: flex;
  align-items: center;
}

.checkbox-wrapper {
  position: relative;
  margin-right: 10px;
}

.timespan-input {
  display: flex;
  align-items: center;
}

.stats-table {
  margin-top: 10px;
}

.custom-button {
  background-color: #007bff;
  /* Blue background color */
  color: #000;
  /* Black text color */
  border: 1px solid #000;
  /* Black border */
  padding: 8px 16px;
  /* Adjust padding as needed */
  border-radius: 4px;
  /* Rounded corners */
  cursor: pointer;
  /* Show pointer cursor on hover */
}

.approved {
  color: #82c545
}

.rejected {
  color: #e01e36
}

.condition {
  color: #fcba19
}

/* Add more styles as needed */
</style>
