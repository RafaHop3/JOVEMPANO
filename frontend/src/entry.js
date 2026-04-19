import './style.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// STATIC IMPORTS for all components to avoid dynamic import binding errors in production
import Home from './views/Home.vue'
import Admin from './views/Admin.vue'
import NewsDetail from './views/NewsDetail.vue'
import CategoryView from './views/CategoryView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/admin', component: Admin },
    { path: '/news/:id', component: NewsDetail },
    {
      path: '/politica',
      component: CategoryView,
      props: { category: 'Politica', slug: 'politica', emoji: '🏛️' }
    },
    {
      path: '/economia',
      component: CategoryView,
      props: { category: 'Economia', slug: 'economia', emoji: '📈' }
    },
    {
      path: '/esportes',
      component: CategoryView,
      props: { category: 'Esportes', slug: 'esportes', emoji: '⚽' }
    },
    {
      path: '/tecnologia',
      component: CategoryView,
      props: { category: 'Tecnologia', slug: 'tecnologia', emoji: '💻' }
    },
    {
      path: '/mundo',
      component: CategoryView,
      props: { category: 'Mundo', slug: 'mundo', emoji: '🌐' }
    }
  ]
})

const app = createApp(App)
app.use(router)

// Mount directly for maximum stability
app.mount('#app')

console.log('[JovemPano] Boot sequence completed with static imports.')
