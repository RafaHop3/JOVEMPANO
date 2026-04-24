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
    {
      path: '/',
      component: Home,
      meta: {
        title: 'JovemPano — Início',
        description: 'Últimas notícias em tempo real sobre política, economia, esportes, tecnologia e mundo.',
      }
    },
    {
      path: '/admin',
      component: Admin,
      meta: {
        title: 'Painel Editorial — JovemPano',
        description: 'Área administrativa para publicação e curadoria de notícias do JovemPano.',
      }
    },
    {
      path: '/news/:id',
      component: NewsDetail,
      meta: {
        title: 'Lendo Notícia — JovemPano',
        description: 'Leia a notícia completa com atualização em tempo real no portal JovemPano.',
      }
    },
    {
      path: '/politica',
      component: CategoryView,
      props: { category: 'Politica', slug: 'politica', emoji: '🏛️' },
      meta: {
        title: 'Política — JovemPano',
        description: 'Cobertura de política com atualização contínua e curadoria editorial.',
      }
    },
    {
      path: '/economia',
      component: CategoryView,
      props: { category: 'Economia', slug: 'economia', emoji: '📈' },
      meta: {
        title: 'Economia — JovemPano',
        description: 'Notícias de economia, mercado e finanças com atualização em tempo real.',
      }
    },
    {
      path: '/esportes',
      component: CategoryView,
      props: { category: 'Esportes', slug: 'esportes', emoji: '⚽' },
      meta: {
        title: 'Esportes — JovemPano',
        description: 'Acompanhe os principais destaques esportivos nacionais e internacionais.',
      }
    },
    {
      path: '/tecnologia',
      component: CategoryView,
      props: { category: 'Tecnologia', slug: 'tecnologia', emoji: '💻' },
      meta: {
        title: 'Tecnologia — JovemPano',
        description: 'Atualizações sobre tecnologia, inovação, IA e tendências digitais.',
      }
    },
    {
      path: '/mundo',
      component: CategoryView,
      props: { category: 'Mundo', slug: 'mundo', emoji: '🌐' },
      meta: {
        title: 'Mundo — JovemPano',
        description: 'Notícias internacionais e os fatos mais relevantes do mundo em tempo real.',
      }
    }
  ]
})

router.afterEach((to) => {
  const baseTitle = 'JovemPano — Portal de Notícias'
  const baseDescription = 'Portal de notícias em tempo real com curadoria editorial.'
  const title = to.meta.title || baseTitle
  const description = to.meta.description || baseDescription
  const canonical = `${window.location.origin}${to.fullPath}`

  document.title = title

  const setMeta = (name, content, isProperty = false) => {
    const selector = isProperty ? `meta[property="${name}"]` : `meta[name="${name}"]`
    let tag = document.head.querySelector(selector)
    if (!tag) {
      tag = document.createElement('meta')
      if (isProperty) tag.setAttribute('property', name)
      else tag.setAttribute('name', name)
      document.head.appendChild(tag)
    }
    tag.setAttribute('content', content)
  }

  setMeta('description', description)
  setMeta('og:title', title, true)
  setMeta('og:description', description, true)
  setMeta('og:url', canonical, true)
  setMeta('twitter:title', title)
  setMeta('twitter:description', description)

  let canonicalTag = document.head.querySelector('link[rel="canonical"]')
  if (!canonicalTag) {
    canonicalTag = document.createElement('link')
    canonicalTag.setAttribute('rel', 'canonical')
    document.head.appendChild(canonicalTag)
  }
  canonicalTag.setAttribute('href', canonical)
})

const app = createApp(App)
app.use(router)

// Mount directly for maximum stability
app.mount('#app')

console.log('[JovemPano] Boot sequence completed with static imports and SEO title management.')
