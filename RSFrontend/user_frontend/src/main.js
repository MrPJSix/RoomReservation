import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from "./strore"
import VueCookies from 'vue-cookies'

import i18n from './language'

//全局按需引入第三方库
import "./plugins/element.js"
import "./plugins/vant.js"

import "@/assets/icon/download/font_vb48wzgs2j/iconfont.css"
import "@/assets/icon/download1/font_5yhw19mnzql/iconfont.css"

import moment from 'moment/moment'

Vue.use(moment)

Vue.use(VueCookies)

Vue.config.productionTip = false


new Vue({
  render: h => h(App),
  router,
  store,
  i18n,
}).$mount('#app')
