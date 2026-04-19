import './style.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// Import views
const Home = () => import('./views/Home.vue')
const Admin = () => import('./views/Admin.vue')
const NewsDetail = () => import('./views/NewsDetail.vue')
const CategoryView = () => import('./views/CategoryView.vue')

const routes = [
  { path: '/', component: Home },
  { path: '/admin', component: Admin },
  { path: '/news/:id', component: NewsDetail },
  {
    path: '/politica',
    component: CategoryView,
    props: { category: 'Política', slug: 'politica', emoji: '🏛️', catColor: 'var(--cat-politica)' },
  },
  {
    path: '/economia',
    component: CategoryView,
    props: { category: 'Economia', slug: 'economia', emoji: '📈', catColor: 'var(--cat-economia)' },
  },
  {
    path: '/esportes',
    component: CategoryView,
    props: { category: 'Esportes', slug: 'esportes', emoji: '⚽', catColor: 'var(--cat-esportes)' },
  },
  {
    path: '/tecnologia',
    component: CategoryView,
    props: { category: 'Tecnologia', slug: 'tecnologia', emoji: '💻', catColor: 'var(--cat-tecnologia)' },
  },
  {
    path: '/mundo',
    component: CategoryView,
    props: { category: 'Mundo', slug: 'mundo', emoji: '🌐', catColor: 'var(--cat-mundo)' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(router)

// Mount app when DOM is ready
window.addEventListener('load', () => {
  app.mount('#app')
})
