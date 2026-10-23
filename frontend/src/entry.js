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
        title: 'Orbe News — JovemPano | Central de Notícias Orbe Systems',
        description: 'Últimas notícias e radar tecnológico em tempo real sobre política, economia, esportes, tecnologia e mundo.',
      }
    },
    {
      path: '/admin',
      component: Admin,
      meta: {
        title: 'Terminal Editorial — Orbe Systems News',
        description: 'Área administrativa para publicação e curadoria de notícias do ecossistema Orbe Systems.',
      }
    },
    {
      path: '/news/:id',
      component: NewsDetail,
      meta: {
        title: 'Radar Editorial — Orbe Systems News',
        description: 'Leia a notícia completa com atualização em tempo real no portal Orbe News.',
      }
    },
    {
      path: '/politica',
      component: CategoryView,
      props: { category: 'Política', slug: 'politica', voidShape: 'shield', catColor: '#f43f5e' },
      meta: {
        title: 'Política — Orbe News',
        description: 'Cobertura de política com atualização contínua e curadoria editorial.',
      }
    },
    {
      path: '/economia',
      component: CategoryView,
      props: { category: 'Economia', slug: 'economia', voidShape: 'pix-dre', catColor: '#10b981' },
      meta: {
        title: 'Economia & Negócios — Orbe News',
        description: 'Notícias de economia, mercado, INHO Business e finanças em tempo real.',
      }
    },
    {
      path: '/esportes',
      component: CategoryView,
      props: { category: 'Esportes', slug: 'esportes', voidShape: 'daw', catColor: '#f59e0b' },
      meta: {
        title: 'Esportes — Orbe News',
        description: 'Acompanhe os principais destaques esportivos nacionais e internacionais.',
      }
    },
    {
      path: '/tecnologia',
      component: CategoryView,
      props: { category: 'Tecnologia', slug: 'tecnologia', voidShape: 'nvme', catColor: '#00fff5' },
      meta: {
        title: 'Tecnologia & Orbe Systems — Orbe News',
        description: 'Inovações em cibersegurança, Voids 3D WebGL, IA, INHO Business e arquitetura de software.',
      }
    },
    {
      path: '/mundo',
      component: CategoryView,
      props: { category: 'Mundo', slug: 'mundo', voidShape: 'globe', catColor: '#3b82f6' },
      meta: {
        title: 'Mundo — Orbe News',
        description: 'Notícias internacionais e os fatos mais relevantes do planeta em tempo real.',
      }
    },
    {
      path: '/positivas',
      component: CategoryView,
      props: { category: 'Boas Notícias', slug: 'positivas', voidShape: 'positive', catColor: '#10b981' },
      meta: {
        title: 'Boas Notícias — Orbe News',
        description: 'Notícias positivas e de impacto social filtradas pelo algoritmo de curadoria.',
      }
    }
  ]
})

router.afterEach((to) => {
  const baseTitle = 'Orbe News — JovemPano | Central de Notícias Orbe Systems'
  const baseDescription = 'Portal oficial de notícias em tempo real e radar de inovação tecnológica do ecossistema Orbe Systems.'
  const title = to.meta.title || baseTitle
  const description = to.meta.description || baseDescription
  const canonical = `https://news.orbesystems.com.br${to.fullPath}`

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
app.mount('#app')

console.log('[Orbe News] Boot sequence completed with Cyber Terminal identity and Void engine.')
