import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import Home from './views/Home.vue'
import Admin from './views/Admin.vue'
import Politica from './views/Politica.vue'
import Economia from './views/Economia.vue'
import Esportes from './views/Esportes.vue'
import Tecnologia from './views/Tecnologia.vue'
import Entretenimento from './views/Entretenimento.vue'
import Mundo from './views/Mundo.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/admin', component: Admin },
  { path: '/politica', component: Politica },
  { path: '/economia', component: Economia },
  { path: '/esportes', component: Esportes },
  { path: '/tecnologia', component: Tecnologia },
  { path: '/entretenimento', component: Entretenimento },
  { path: '/mundo', component: Mundo },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

createApp(App).use(router).mount('#app')
