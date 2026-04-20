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
    { path: '/', component: Home, meta: { title: 'JovemPano — Início' } },
    { path: '/admin', component: Admin, meta: { title: 'Painel Editorial — JovemPano' } },
    { path: '/news/:id', component: NewsDetail, meta: { title: 'Lendo Notícia — JovemPano' } },
    {
      path: '/politica',
      component: CategoryView,
      props: { category: 'Politica', slug: 'politica', emoji: '🏛️' },
      meta: { title: 'Política — JovemPano' }
    },
    {
      path: '/economia',
      component: CategoryView,
      props: { category: 'Economia', slug: 'economia', emoji: '📈' },
      meta: { title: 'Economia — JovemPano' }
    },
    {
      path: '/esportes',
      component: CategoryView,
      props: { category: 'Esportes', slug: 'esportes', emoji: '⚽' },
      meta: { title: 'Esportes — JovemPano' }
    },
    {
      path: '/tecnologia',
      component: CategoryView,
      props: { category: 'Tecnologia', slug: 'tecnologia', emoji: '💻' },
      meta: { title: 'Tecnologia — JovemPano' }
    },
    {
      path: '/mundo',
      component: CategoryView,
      props: { category: 'Mundo', slug: 'mundo', emoji: '🌐' },
      meta: { title: 'Mundo — JovemPano' }
    }
  ]
})

router.afterEach((to) => {
  const baseTitle = 'JovemPano — Portal de Notícias'
  document.title = to.meta.title || baseTitle
})

const app = createApp(App)
app.use(router)

// Mount directly for maximum stability
app.mount('#app')

console.log('[JovemPano] Boot sequence completed with static imports and SEO title management.')
