module.exports = {
  configureWebpack: {
    devtool: 'source-map'
  },
  transpileDependencies: [
    'vuetify',
    'vuex-module-decorators',
    'keycloak-js'
  ],
  publicPath: `${import.meta.env.VUE_APP_PATH}`
}
