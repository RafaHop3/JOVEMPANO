import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createHead } from '@unhead/vue'
import './style.css'
import App from './App.vue'
import Home from './views/Home.vue'
import Admin from './views/Admin.vue'

console.log('[RECONSTRUCTION] Phase 2/3 main.js starting...')

const routes = [
  { path: '/', component: Home },
  { path: '/admin', component: Admin },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const head = createHead()

try {
  const app = createApp(App)
  app.use(router)
  app.use(head)
  
  console.log('[RECONSTRUCTION] App initialized with Router and Head. Mounting...')
  app.mount('#app')
  console.log('[RECONSTRUCTION] App mounted successfully at #app.')
} catch (error) {
  console.error('[RECONSTRUCTION] Mount error during Phase 2/3:', error)
  const appDiv = document.getElementById('app')
  if (appDiv) {
    appDiv.innerHTML = `<h1 style="color:red">MOUNT FAILED IN PHASE 2/3: ${error.message}</h1>`
  }
}
