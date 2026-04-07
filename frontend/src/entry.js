console.log('[JOVEMPANO] Instando carregamento seguro (entry.js)...')

async function bootstrap() {
  const appDiv = document.getElementById('app')
  if (!appDiv) return

  try {
    console.log('[JOVEMPANO] Carregando dependências...')
    
    // Carregamento dinâmico para evitar falhas silenciosas
    const [{ createApp }, { createRouter, createWebHistory }, { createHead }] = await Promise.all([
      import('vue'),
      import('vue-router'),
      import('@unhead/vue')
    ])
    
    const App = (await import('./App.vue')).default
    const Home = (await import('./views/Home.vue')).default
    const Admin = (await import('./views/Admin.vue')).default
    
    const routes = [
      { path: '/', component: Home },
      { path: '/admin', component: Admin },
      { path: '/politica', component: Home }, // Categorias temporariamente roteadas para Home
      { path: '/economia', component: Home },
      { path: '/esportes', component: Home }
    ]

    const router = createRouter({
      history: createWebHistory(),
      routes
    })

    const head = createHead()

    const app = createApp(App)
    app.use(router)
    app.use(head)
    
    console.log('[JOVEMPANO] Montando App...')
    app.mount('#app')
    console.log('[JOVEMPANO] Sucesso na restauração.')
    
  } catch (err) {
    console.error('[JOVEMPANO] Falha crítica:', err)
    appDiv.innerHTML = `
      <div style="background: white; padding: 40px; border: 4px solid #e11d48; border-radius: 20px; color: #e11d48; font-family: sans-serif;">
        <h1 style="font-size: 24px;">Falha na Restauração</h1>
        <p>Ocorreu um erro ao carregar os módulos da plataforma pós-restauração.</p>
        <pre style="background: #fff1f2; padding: 15px; border-radius: 10px; font-size: 12px; overflow: auto;">${err.message}</pre>
        <button onclick="location.reload()" style="background: #e11d48; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 10px;">Tentar Novamente</button>
      </div>
    `
  }
}

bootstrap()
