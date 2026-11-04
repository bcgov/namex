// Reference to vuetify form api: https://vuetifyjs.com/en/api/v-form/#functions
export interface FormType extends HTMLFormElement {
  reset(): void
  validate(): boolean
  resetValidation(): void
}
