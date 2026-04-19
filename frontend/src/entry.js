import './style.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createHead } from '@unhead/vue'
import App from './App.vue'

const routes = [
  {
    path: '/',
    component: () => import('./views/Home.vue'),
  },
  {
    path: '/admin',
    component: () => import('./views/Admin.vue'),
  },
  {
    path: '/news/:id',
    component: () => import('./views/NewsDetail.vue'),
  },
  {
    path: '/politica',
    component: () => import('./views/CategoryView.vue'),
    props: { category: 'Política', slug: 'politica', emoji: '🏛️', catColor: 'var(--cat-politica)' },
  },
  {
    path: '/economia',
    component: () => import('./views/CategoryView.vue'),
    props: { category: 'Economia', slug: 'economia', emoji: '📈', catColor: 'var(--cat-economia)' },
  },
  {
    path: '/esportes',
    component: () => import('./views/CategoryView.vue'),
    props: { category: 'Esportes', slug: 'esportes', emoji: '⚽', catColor: 'var(--cat-esportes)' },
  },
  {
    path: '/tecnologia',
    component: () => import('./views/CategoryView.vue'),
    props: { category: 'Tecnologia', slug: 'tecnologia', emoji: '💻', catColor: 'var(--cat-tecnologia)' },
  },
  {
    path: '/mundo',
    component: () => import('./views/CategoryView.vue'),
    props: { category: 'Mundo', slug: 'mundo', emoji: '🌐', catColor: 'var(--cat-mundo)' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const head = createHead()
const app = createApp(App)

app.use(router)
app.use(head)

app.mount('#app')

console.log('[JovemPano] Aplicação inicializada com sucesso.')
