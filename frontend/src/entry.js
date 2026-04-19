import './style.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createHead } from '@unhead/vue'
import App from './App.vue'

console.log('[JovemPano] Iniciando aplicação...')

const appDiv = document.getElementById('app')

try {
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

  const router = createRouter({ history: createWebHistory(), routes })
  const head = createHead()

  const app = createApp(App)
  app.use(router)
  app.use(head)
  app.mount('#app')

  console.log('[JovemPano] Pronto.')
} catch (err) {
    console.error('[JovemPano] Falha crítica:', err)
    appDiv.innerHTML = `
      <div style="background:#06060e;min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:sans-serif;padding:2rem;">
        <div style="max-width:480px;text-align:center;">
          <div style="font-size:3rem;margin-bottom:1rem;">⚠️</div>
          <h1 style="color:#e11d48;font-size:1.5rem;margin-bottom:.5rem;">Erro ao carregar</h1>
          <p style="color:#94a3b8;margin-bottom:1rem;">Houve uma falha ao inicializar a plataforma.</p>
          <pre style="background:#0d0d18;padding:12px;border-radius:8px;font-size:11px;color:#475569;text-align:left;overflow:auto;border:1px solid rgba(255,255,255,0.06);">${err.message}\n\n${err.stack || ''}</pre>
          <button onclick="location.reload()" style="background:#e11d48;color:#fff;border:none;padding:10px 24px;border-radius:8px;cursor:pointer;font-weight:700;margin-top:1rem;">
            Recarregar
          </button>
        </div>
      </div>
    `
  }
}

bootstrap()
