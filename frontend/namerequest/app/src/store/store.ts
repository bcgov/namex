import { defineStore } from 'pinia'
import { state } from './state'
import * as Getters from './getters'
import * as Actions from './actions'

/** Combine state, getters, and actions into main store. */
export const useStore = defineStore('store', {
  state: () => state,
  getters: { ...Getters },
  actions: { ...Actions }
})
