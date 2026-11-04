/** Describes an error that occurs during the app's execution that should be showed to the user. */
export interface AppError {
  /** A short title/description for the error. */
  title: string
  /** Message for the error to show the user. */
  message: string
}
