/** Copyright (C) <2021>  <Kody Moodley and Walter Simoncini> **/
/** License: https://www.gnu.org/licenses/agpl-3.0.txt **/

import Vue from 'vue'

import App from './App.vue'

// Polyfill for older browsers. The import must
// be before any Vuex usage
import 'es6-promise/auto'
import Vuex from 'vuex'

import Buefy from 'buefy'
import 'buefy/dist/buefy.css'

import '@/assets/style.css'

import router from './router'
const axios = require('axios')

Vue.config.productionTip = false;

Vue.use(Buefy);
Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    api: axios.create({
      baseURL: process.env.VUE_APP_API_ROOT,
      headers: {
        "Api-Key": process.env.VUE_APP_API_KEY
      }
    }),
    maxDistance: 2
  },
  mutations: {
    updateMaxDistance(state, value) {
      state.maxDistance = value;
    }
  }
})

new Vue({
  router,
  render: h => h(App),
  store: store
}).$mount('#app');
