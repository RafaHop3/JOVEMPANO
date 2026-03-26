import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createUnhead } from '@unhead/vue'
import './style.css'
import App from './App.vue'
import Home from './views/Home.vue'
import Admin from './views/Admin.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/admin', component: Admin },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const head = createUnhead()

createApp(App).use(router).use(head).mount('#app')
