// import Vue from "/node_modules/vue/index.js"
import { createRouter, createWebHistory } from "/node_modules/vue-router"

import index from '../views/index.vue'



// Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'index',
    component: index
  }
]

const router = createRouter({
    // 使用hash(createWebHashHistory)模式，(createWebHistory是HTML5历史模式，支持SEO)
    history: createWebHistory(),
    routes: routes,
})

export default router
