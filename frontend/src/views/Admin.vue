<template>
  <div>
    <!-- Login -->
    <div v-if="!token" class="max-w-md mx-auto bg-white p-8 rounded-xl shadow-lg border border-slate-200 mt-12">
      <h2 class="text-2xl font-bold mb-6 text-slate-900 text-center">Login Administrativo</h2>
      <form @submit.prevent="login" class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-slate-500 mb-1">Usuário</label>
          <input v-model="username" type="text" required class="w-full bg-slate-50 border border-slate-200 rounded px-3 py-2 text-slate-900 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-500 mb-1">Senha</label>
          <input v-model="password" type="password" required class="w-full bg-slate-50 border border-slate-200 rounded px-3 py-2 text-slate-900 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500" />
        </div>
        <div v-if="loginError" class="text-rose-500 text-sm font-bold">{{ loginError }}</div>
        <button type="submit" class="mt-4 w-full bg-rose-600 hover:bg-rose-700 text-white font-bold py-2 px-4 rounded transition-colors" :disabled="loginLoading">
          {{ loginLoading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>
    </div>

    <!-- Dashboard -->
    <div v-else class="flex flex-col gap-10">
      <!-- Header -->
      <div class="flex justify-between items-center pb-4 border-b border-slate-200">
        <h2 class="text-3xl font-bold text-slate-900 flex items-center gap-3">
          <span class="w-3 h-8 bg-rose-600 rounded"></span>
          Painel do Admin
        </h2>
        <button @click="logout" class="text-slate-400 font-medium hover:text-rose-600 transition-colors">Sair</button>
      </div>

      <!-- TABS -->
      <div class="flex gap-2 border-b border-slate-200">
        <button 
          v-for="tab in tabs" :key="tab.id"
          @click="activeTab = tab.id"
          :class="['px-5 py-2.5 text-sm font-bold rounded-t-lg transition-all', activeTab === tab.id ? 'bg-rose-600 text-white' : 'text-slate-400 hover:text-slate-900 hover:bg-slate-50']"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- TAB: Publicar Notícia -->
      <section v-if="activeTab === 'news'" class="bg-white border border-slate-200 rounded-xl p-8 shadow-sm">
        <h3 class="text-xl font-bold text-slate-900 mb-6">📰 Publicar Nova Matéria</h3>
        <form @submit.prevent="createNews" class="flex flex-col gap-5">
          <div>
            <label class="block text-sm font-bold text-slate-600 mb-2">Manchete (Título)*</label>
            <input v-model="newsForm.title" type="text" placeholder="Ex: Governo anuncia novas medidas..." required class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-slate-900 text-lg focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500" />
          </div>
          
          <div>
            <label class="block text-sm font-bold text-slate-600 mb-2">URL da Imagem de Capa</label>
            <input v-model="newsForm.image_url" type="url" placeholder="https://exemplo.com/imagem.jpg ou /images/news_politica.png" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-slate-900 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500" />
            
            <div class="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-bold text-slate-600 mb-2">Categoria*</label>
                <select v-model="newsForm.category" required class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-slate-900 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500">
                  <option value="Geral">Geral</option>
                  <option value="Política">Política</option>
                  <option value="Economia">Economia</option>
                  <option value="Esportes">Esportes</option>
                  <option value="Tecnologia">Tecnologia</option>
                  <option value="Entretenimento">Entretenimento</option>
                  <option value="Mundo">Mundo</option>
                </select>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-bold text-slate-600 mb-2">Corpo da Matéria*</label>
            <div id="editor-container" class="bg-white h-80 rounded-b-lg border border-slate-200"></div>
          </div>

          <div v-if="newsMsg" :class="['p-4 rounded-lg font-bold text-sm', newsSuccess ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-600 border border-rose-200']">
            {{ newsMsg }}
          </div>

          <button type="submit" class="self-start bg-rose-600 hover:bg-rose-500 text-white font-bold py-3 px-8 rounded-lg shadow-lg hover:shadow-rose-500/20 transition-all" :disabled="newsPosting">
            {{ newsPosting ? 'Publicando...' : '🚀 Publicar Agora' }}
          </button>
        </form>
      </section>

      <!-- TAB: Banners / Destaque -->
      <section v-if="activeTab === 'banners'" class="bg-white border border-slate-200 rounded-xl p-8 shadow-sm">
        <h3 class="text-xl font-bold text-slate-900 mb-6">🖼️ Gerenciar Banners de Destaque</h3>
        <form @submit.prevent="createBanner" class="flex flex-col gap-5">
          <div>
            <label class="block text-sm font-bold text-slate-600 mb-2">Título do Banner*</label>
            <input v-model="bannerForm.title" type="text" placeholder="Ex: Eleições 2026..." required class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-slate-900 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500" />
          </div>
          <div>
            <label class="block text-sm font-bold text-slate-600 mb-2">URL da Imagem*</label>
            <input v-model="bannerForm.image_url" type="text" placeholder="/images/hero_banner.png" required class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-slate-900 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500" />
          </div>
          <button type="submit" class="self-start bg-rose-600 hover:bg-rose-500 text-white font-bold py-3 px-8 rounded-lg transition-all" :disabled="bannerPosting">
            {{ bannerPosting ? 'Publicando...' : ' Adicionar Banner' }}
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

// API
const API_BASE = 'http://localhost:8000'

// Auth
const token = ref('')
const username = ref('')
const password = ref('')
const loginError = ref('')
const loginLoading = ref(false)

// Tabs
const activeTab = ref('news')
const tabs = [
  { id: 'news', label: '📰 Notícias' },
  { id: 'banners', label: '🖼️ Banners Destaque' },
]

// Forms
const newsForm = ref({ title: '', content: '', image_url: '', category: 'Geral' })
const newsPosting = ref(false)
const newsMsg = ref('')
const newsSuccess = ref(false)

const bannerForm = ref({ title: '', subtitle: '', image_url: '', link_url: '', is_active: true })
const bannerPosting = ref(false)

let quill = null
const initEditor = () => {
  if (quill) return
  setTimeout(() => {
    const container = document.getElementById('editor-container')
    if (container) {
      quill = new Quill('#editor-container', {
        theme: 'snow',
        placeholder: 'Escreva o conteúdo da notícia aqui...',
        modules: {
          toolbar: [
            [{ 'header': [1, 2, 3, false] }],
            ['bold', 'italic', 'underline'],
            ['link', 'image'],
            ['clean']
          ]
        }
      })
    }
  }, 100)
}

watch(activeTab, (newTab) => {
  if (newTab === 'news') initEditor()
})

onMounted(() => {
  const saved = localStorage.getItem('token')
  if (saved) {
    token.value = saved
    if (activeTab.value === 'news') initEditor()
  }
})

const login = async () => {
  loginLoading.value = true
  loginError.value = ''
  try {
    const form = new URLSearchParams()
    form.append('username', username.value)
    form.append('password', password.value)
    const res = await fetch(`${API_BASE}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: form })
    if (!res.ok) throw new Error('Credenciais inválidas.')
    const data = await res.json()
    token.value = data.access_token
    localStorage.setItem('token', token.value)
    if (activeTab.value === 'news') initEditor()
  } catch (err) {
    loginError.value = err.message
  } finally {
    loginLoading.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  token.value = ''
}

const createNews = async () => {
  newsPosting.value = true
  newsMsg.value = ''
  try {
    const content = quill ? quill.root.innerHTML : newsForm.value.content
    const payload = { ...newsForm.value, content }
    const res = await fetch(`${API_BASE}/news/`, { 
      method: 'POST', 
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token.value}` }, 
      body: JSON.stringify(payload) 
    })
    if (!res.ok) throw new Error('Erro ao publicar.')
    newsSuccess.value = true
    newsMsg.value = '✅ Notícia publicada!'
    newsForm.value = { title: '', content: '', image_url: '', category: 'Geral' }
    if (quill) quill.setContents([])
  } catch (err) {
    newsMsg.value = err.message
  } finally {
    newsPosting.value = false
  }
}

const createBanner = async () => {
  bannerPosting.value = true
  try {
    const res = await fetch(`${API_BASE}/banners/`, { 
      method: 'POST', 
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token.value}` }, 
      body: JSON.stringify(bannerForm.value) 
    })
    if (!res.ok) throw new Error('Erro ao criar banner.')
    bannerForm.value = { title: '', subtitle: '', image_url: '', link_url: '', is_active: true }
    alert('Banner adicionado!')
  } catch (err) {
    alert(err.message)
  } finally {
    bannerPosting.value = false
  }
}
</script>
