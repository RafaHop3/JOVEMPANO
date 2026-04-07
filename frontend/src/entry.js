console.log('[JOVEMPANO] Instando carregamento seguro...')

async function bootstrap() {
  const appDiv = document.getElementById('app')
  if (!appDiv) {
    console.error('ERRO: Elemento #app não encontrado no DOM.')
    return
  }

  try {
    console.log('[JOVEMPANO] Carregando dependências...')
    
    // Carregamento dinâmico para evitar falhas silenciosas de importação estática
    const [{ createApp }, { createRouter, createWebHistory }, { createHead }] = await Promise.all([
      import('vue'),
      import('vue-router'),
      import('@unhead/vue')
    ])
    
    console.log('[JOVEMPANO] Dependências base OK.')

    const App = (await import('./App.vue')).default
    const Home = (await import('./views/Home.vue')).default
    const Admin = (await import('./views/Admin.vue')).default
    
    console.log('[JOVEMPANO] Componentes OK.')

    const routes = [
      { path: '/', component: Home },
      { path: '/admin', component: Admin },
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
    console.log('[JOVEMPANO] Sucesso total.')
    
  } catch (err) {
    console.error('[JOVEMPANO] Falha crítica:', err)
    appDiv.innerHTML = `
      <div style="background: white; padding: 40px; border: 4px solid #e11d48; border-radius: 20px; color: #e11d48; font-family: sans-serif;">
        <h1 style="font-size: 24px;">Falha Fatal na Inicialização</h1>
        <p>Ocorreu um erro ao carregar os módulos da plataforma.</p>
        <pre style="background: #fff1f2; padding: 15px; border-radius: 10px; font-size: 12px; overflow: auto;">${err.message}\n${err.stack}</pre>
        <button onclick="location.reload()" style="background: #e11d48; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 10px;">Tentar Novamente</button>
      </div>
    `
  }
}

bootstrap()
