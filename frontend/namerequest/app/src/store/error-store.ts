import { defineStore } from 'pinia'
import { ErrorI } from '@/interfaces'

export const useErrorStore = defineStore('error', {
  state: () => ({
    errors: [] as ErrorI[]
  }),

  getters: {
    hasErrors (): boolean {
      return this.errors.length > 0
    },

    getError () {
      // return a function to allow passing of a parameter
      return (errorId: string) => {
        const error = this.errors.find((item) => item.id === errorId)
        return error || undefined
      }
    },

    // NOTE - there is a different getErrors in the main store
    getErrors (): ErrorI[] {
      return this.errors
    }
  },

  actions: {
    setAppError (err: ErrorI) {
      const existingError = this.errors.find((item) => item.id === err.id)
      if (existingError) {
        this.errors[this.errors.indexOf(existingError)] = existingError
      } else {
        this.errors.push(err)
      }
    },

    setAppErrors (errArr: ErrorI[]) {
      const errors = this.errors
      errArr.map((err) => {
        const existingError = this.errors.find((item) => item.id === err.id)
        if (existingError) {
          this.errors[this.errors.indexOf(existingError)] = existingError
        } else {
          this.errors.push(err)
        }
      })
      this.errors = errors
    },

    clearAppError (id: string) {
      const existingError = this.errors.find((item) => item.id === id)
      if (existingError) {
        delete this.errors[this.errors.indexOf(existingError)]
      }
    },

    clearAppErrors () {
      this.errors = []
    }
  }
})
