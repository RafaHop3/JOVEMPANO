import './style.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('./views/Home.vue') },
    { path: '/admin', component: () => import('./views/Admin.vue') },
    { path: '/news/:id', component: () => import('./views/NewsDetail.vue') },
    {
      path: '/politica',
      component: () => import('./views/CategoryView.vue'),
      props: { category: 'Politica', slug: 'politica', emoji: '🏛️' }
    },
    {
      path: '/economia',
      component: () => import('./views/CategoryView.vue'),
      props: { category: 'Economia', slug: 'economia', emoji: '📈' }
    },
    {
      path: '/esportes',
      component: () => import('./views/CategoryView.vue'),
      props: { category: 'Esportes', slug: 'esportes', emoji: '⚽' }
    },
    {
      path: '/tecnologia',
      component: () => import('./views/CategoryView.vue'),
      props: { category: 'Tecnologia', slug: 'tecnologia', emoji: '💻' }
    },
    {
      path: '/mundo',
      component: () => import('./views/CategoryView.vue'),
      props: { category: 'Mundo', slug: 'mundo', emoji: '🌐' }
    }
  ]
})

const app = createApp(App)
app.use(router)
app.mount('#app')

console.log('[JovemPano] Boot OK.')
