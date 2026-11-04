<template>
  <div class="sm:px-0">
    <TabGroup @change="onChangeTab">
      <ExamineRecipeTabsHeader />

      <TabPanels
        ref="panels"
        class="mt-2 h-[29rem] overflow-auto rounded border border-gray-300 bg-white"
      >
        <!-- Conflicts tab -->
        <TabPanel class="h-full" ref="conflicts" :unmount="false">
          <ExamineRecipeConflicts />
        </TabPanel>

        <!-- Conditions tab -->
        <TabPanel ref="conditions" :unmount="false">
          <ExamineRecipeConditions />
        </TabPanel>

        <!-- Trademarks tab -->
        <TabPanel ref="trademarks" :unmount="false">
          <ExamineRecipeTrademarks />
        </TabPanel>

        <!-- History tab -->
        <TabPanel ref="history" :unmount="false">
          <ExamineRecipeHistory />
        </TabPanel>

        <!-- Compare tab -->
        <TabPanel class="h-full" ref="compare" :unmount="false">
          <ExamineRecipeCompare />
        </TabPanel>
      </TabPanels>
    </TabGroup>
  </div>
</template>

<script setup lang="ts">
import { TabGroup, TabPanels, TabPanel } from '@headlessui/vue'
import { emitter } from '~/util/emitter';

const conflicts = ref<InstanceType<typeof TabPanel>>()
const conditions = ref<InstanceType<typeof TabPanel>>()
const trademarks = ref<InstanceType<typeof TabPanel>>()
const history = ref<InstanceType<typeof TabPanel>>()
const compare = ref<InstanceType<typeof TabPanel>>()
const panels = ref<InstanceType<typeof TabPanels>>()

const tabs = [conflicts, conditions, trademarks, history, compare]
const lastIndex = ref(0)

const scrollPositions: Array<number> = new Array(5).fill(0)

type TabElementRef =
  | Ref<InstanceType<typeof TabPanel> | undefined>
  | Ref<InstanceType<typeof TabPanels> | undefined>

function getTop(elem: TabElementRef) {
  return (elem.value?.$el.getBoundingClientRect().top as number) ?? 0
}

function setTop(elem: TabElementRef, top: number) {
  setTimeout(() => {
    elem.value?.$el.scrollTo({ top, behavior: 'instant' })
  }, 1)
}

function onChangeTab(index: number) {
  emitter.emit('recipeTabChanged', index)
  setTop(panels, scrollPositions[index])
  const panelTop = getTop(panels)
  scrollPositions[lastIndex.value] = panelTop - getTop(tabs[lastIndex.value])
  lastIndex.value = index
}
</script>
