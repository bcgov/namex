import { defineStore } from 'pinia'
import { getLocalStorageValue } from '~/util'

export const useExaminationOptions = defineStore('examine-options', () => {
  const priorityQueue = ref(getLocalStorageValue('PriorityQueue', false))

  const updatePriority = (newPriority: boolean) => {
    priorityQueue.value = newPriority
    window.localStorage.setItem('PriorityQueue', JSON.stringify(newPriority))
  }

  return { priorityQueue, updatePriority }
})
