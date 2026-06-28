import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

// createApp(App).mount('#app')
import { createMemoryHistory, createRouter, createWebHistory } from 'vue-router'

import GoodsReceipt from '@/pages/GoodsReceipt.vue'
import Home from '@/pages/Home.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const routes = [
  { path: "/", redirect: "/goods-receipt" },
  { path: "/home", component: Home },
  { path: '/goods-receipt', component: GoodsReceipt },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App).use(router).use(ElementPlus).mount('#app')