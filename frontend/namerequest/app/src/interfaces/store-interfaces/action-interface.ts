// Interface to define a Vuex Action
export interface ActionIF {
  (x: any, y?: any | null): void
}

export interface ActionBindingIF {
  (x: any | null, y?: any | null): any
}
