/** Copyright (C) <2021>  <Kody Moodley and Walter Simoncini> **/
/** License: https://www.gnu.org/licenses/agpl-3.0.txt **/

import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/Main.vue'),
    children: [
      {
        path: '',
        name: 'graph-browser',
        component: () => import('@/views/GraphBrowser.vue')
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  routes: routes
})

export default router