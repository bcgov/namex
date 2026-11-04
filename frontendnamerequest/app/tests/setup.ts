import Vue from 'vue'
import Vuetify from 'vuetify'

Vue.use(Vuetify)

Vue.config.devtools = false
Vue.config.productionTip = false

// mock global Vuex store and attach to Vue instance
Vue.prototype.$store = {
  getters: {},
  state: {}
}
