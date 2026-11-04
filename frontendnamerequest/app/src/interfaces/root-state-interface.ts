/** The ROOT state model interface. */
export interface RootStateIF {
  auth: {
    token: string,
    idToken: string,
    refreshToken: string
  }
}
