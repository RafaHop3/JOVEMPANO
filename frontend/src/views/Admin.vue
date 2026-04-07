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
            <!-- Image Preview -->
            <div v-if="newsForm.image_url" class="mt-3 rounded-lg overflow-hidden border border-slate-200 h-40">
              <img :src="newsForm.image_url" alt="Preview" class="w-full h-full object-cover" @error="newsForm.image_url = ''" />
            </div>
            
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
            <!-- Quick pick: built-in images -->
            <div class="mt-3">
              <p class="text-xs text-slate-400 mb-2 font-mono">Imagens disponíveis (clique para usar):</p>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="img in builtinImages" :key="img.path" 
                  type="button"
                  @click="newsForm.image_url = img.path"
                  class="relative overflow-hidden rounded-lg border-2 transition-all hover:border-rose-500"
                  :class="newsForm.image_url === img.path ? 'border-rose-600 ring-2 ring-rose-500/30' : 'border-slate-200'"
                  style="width: 80px; height: 55px;"
                >
                  <img :src="img.path" :alt="img.label" class="w-full h-full object-cover" />
                  <span class="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-xs text-center py-0.5">{{ img.label }}</span>
                </button>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-bold text-slate-600 mb-2">Corpo da Matéria*</label>
            <!-- Quill Editor Container -->
            <div id="editor-container" class="bg-white h-80 rounded-b-lg border-slate-200"></div>
          </div>

          <div v-if="newsMsg" :class="['p-4 rounded-lg font-bold text-sm', newsSuccess ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-600 border border-rose-200']">
            {{ newsMsg }}
          </div>

          <button type="submit" class="self-start bg-rose-600 hover:bg-rose-500 text-white font-bold py-3 px-8 rounded-lg shadow-lg hover:shadow-rose-500/20 transition-all" :disabled="newsPosting">
            {{ newsPosting ? 'Publicando...' : '🚀 Publicar Agora' }}
          </button>
        </form>

        <!-- Manage Existing News -->
        <div class="mt-10 border-t border-slate-200 pt-8">
          <h4 class="text-lg font-bold text-slate-900 mb-4">Matérias Publicadas</h4>
          <div class="space-y-3 max-h-96 overflow-y-auto pr-2">
            <div v-for="item in newsList" :key="item.id" class="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-lg p-3">
              <img v-if="item.image_url" :src="item.image_url" alt="" class="w-16 h-12 object-cover rounded-lg flex-shrink-0" />
              <div v-else class="w-16 h-12 bg-slate-100 rounded-lg flex-shrink-0 flex items-center justify-center text-slate-400 text-xs">Sem img</div>
              <div class="flex-1 min-w-0">
                <p class="text-slate-900 font-semibold text-sm truncate">{{ item.title }}</p>
                <p class="text-slate-400 text-xs font-mono">{{ new Date(item.created_at).toLocaleString('pt-BR') }}</p>
              </div>
              <button @click="deleteNews(item.id)" class="flex-shrink-0 text-slate-400 hover:text-rose-500 transition-colors p-1" title="Excluir">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </div>
            <p v-if="newsList.length === 0" class="text-slate-400 text-sm text-center py-4">Nenhuma matéria publicada ainda.</p>
          </div>
        </div>
      </section>

      <!-- TAB: Banners / Destaque -->
      <section v-if="activeTab === 'banners'" class="bg-white border border-slate-200 rounded-xl p-8 shadow-sm">
        <h3 class="text-xl font-bold text-slate-900 mb-6">🖼️ Gerenciar Banners de Destaque</h3>
        
        <form @submit.prevent="createBanner" class="flex flex-col gap-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-bold text-slate-600 mb-2">Título do Banner*</label>
              <input v-model="bannerForm.title" type="text" placeholder="Ex: Eleições 2026: Quem são..." required class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-slate-900 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500" />
            </div>
            <div>
              <label class="block text-sm font-bold text-slate-600 mb-2">Link (URL da matéria)</label>
              <input v-model="bannerForm.link_url" type="url" placeholder="https://... ou deixe vazio" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-slate-900 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-bold text-slate-600 mb-2">Subtítulo / Chamada</label>
            <input v-model="bannerForm.subtitle" type="text" placeholder="Uma linha de chamada para o leitor..." class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-slate-900 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500" />
          </div>

          <div>
            <label class="block text-sm font-bold text-slate-600 mb-2">URL da Imagem de Fundo*</label>
            <input v-model="bannerForm.image_url" type="text" placeholder="https://... ou /images/hero_banner.png" required class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-slate-900 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500" />
            <!-- Quick pick -->
            <div class="mt-3 flex flex-wrap gap-2">
              <p class="w-full text-xs text-slate-400 font-mono mb-1">Imagens disponíveis:</p>
              <button 
                v-for="img in builtinImages" :key="img.path" 
                type="button"
                @click="bannerForm.image_url = img.path"
                class="relative overflow-hidden rounded-lg border-2 transition-all hover:border-rose-500"
                :class="bannerForm.image_url === img.path ? 'border-rose-600 ring-2 ring-rose-500/30' : 'border-slate-200'"
                style="width: 90px; height: 60px;"
              >
                <img :src="img.path" :alt="img.label" class="w-full h-full object-cover" />
                <span class="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-xs text-center py-0.5">{{ img.label }}</span>
              </button>
            </div>
            <!-- Preview -->
            <div v-if="bannerForm.image_url" class="mt-3 rounded-lg overflow-hidden border border-slate-200 h-48 relative">
              <img :src="bannerForm.image_url" alt="Preview" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-r from-black/60 to-transparent flex items-end p-4">
                <div class="text-white">
                  <p class="font-bold text-lg">{{ bannerForm.title || 'Título do banner' }}</p>
                  <p v-if="bannerForm.subtitle" class="text-sm text-slate-300">{{ bannerForm.subtitle }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <input type="checkbox" id="bannerActive" v-model="bannerForm.is_active" class="w-4 h-4 accent-rose-600" />
            <label for="bannerActive" class="text-sm text-slate-600">Publicar imediatamente (ativo)</label>
          </div>

          <div v-if="bannerMsg" :class="['p-4 rounded-lg font-bold text-sm', bannerSuccess ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-600 border border-rose-200']">
            {{ bannerMsg }}
          </div>

          <button type="submit" class="self-start bg-rose-600 hover:bg-rose-500 text-white font-bold py-3 px-8 rounded-lg transition-all" :disabled="bannerPosting">
            {{ bannerPosting ? 'Publicando...' : '🖼️ Adicionar Banner' }}
          </button>
        </form>

        <!-- Existing Banners List -->
        <div class="mt-10 border-t border-slate-200 pt-8">
          <h4 class="text-lg font-bold text-slate-900 mb-4">Banners Cadastrados</h4>
          <div class="space-y-3 max-h-[500px] overflow-y-auto pr-2">
            <div v-for="b in bannersList" :key="b.id" class="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-lg p-3">
              <img :src="b.image_url" alt="" class="w-20 h-14 object-cover rounded-lg flex-shrink-0" @error="e => e.target.style.display='none'" />
              <div class="flex-1 min-w-0">
                <p class="text-slate-900 font-semibold text-sm truncate">{{ b.title }}</p>
                <p v-if="b.subtitle" class="text-slate-400 text-xs truncate">{{ b.subtitle }}</p>
              </div>
              <!-- Active toggle -->
              <button @click="toggleBanner(b.id)" :class="['flex-shrink-0 text-xs font-bold px-3 py-1 rounded-full transition-all', b.is_active ? 'bg-emerald-100 text-emerald-700 hover:bg-emerald-200' : 'bg-slate-100 text-slate-400 hover:bg-slate-200']">
                {{ b.is_active ? '● Ativo' : '○ Off' }}
              </button>
              <button @click="deleteBanner(b.id)" class="flex-shrink-0 text-slate-400 hover:text-rose-500 transition-colors p-1">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </div>
            <p v-if="bannersList.length === 0" class="text-slate-400 text-sm text-center py-4">Nenhum banner cadastrado ainda.</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { API_BASE } from '../api.js'

// Auth
const token = ref('')
const username = ref('')
const password = ref('')
const loginError = ref('')
const loginLoading = ref(false)

// Tabs
const activeTab = ref('news')
import { watch } from 'vue'
watch(activeTab, (newTab) => {
  if (newTab === 'news') initEditor()
})
const tabs = [
  { id: 'news', label: '📰 Notícias' },
  { id: 'banners', label: '🖼️ Banners Destaque' },
]

// Built-in images
const builtinImages = [
  { path: '/images/hero_banner.png', label: 'Hero' },
  { path: '/images/news_politica.png', label: 'Política' },
  { path: '/images/news_economia.png', label: 'Economia' },
  { path: '/images/news_esportes.png', label: 'Esportes' },
]

// News form
const newsForm = ref({ title: '', content: '', image_url: '', category: 'Geral' })
const newsPosting = ref(false)
const newsMsg = ref('')
const newsSuccess = ref(false)
const newsList = ref([])

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
            ['bold', 'italic', 'underline', 'strike'],
            ['blockquote', 'code-block'],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            ['link', 'image'],
            ['clean']
          ]
        }
      })
    }
  }, 100)
}

// Banner form
const bannerForm = ref({ title: '', subtitle: '', image_url: '', link_url: '', is_active: true })
const bannerPosting = ref(false)
const bannerMsg = ref('')
const bannerSuccess = ref(false)
const bannersList = ref([])

// ---- Auth ----
onMounted(() => {
  const saved = localStorage.getItem('token')
  if (saved) {
    token.value = saved
    loadNews()
    loadBanners()
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
    loadNews()
    loadBanners()
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

const authHeaders = () => ({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token.value}`
})

const checkAuth = (res) => {
  if (res.status === 401) { logout(); return false }
  return true
}

// ---- News ----
const loadNews = async () => {
  const res = await fetch(`${API_BASE}/news/`)
  if (res.ok) newsList.value = await res.json()
}

const createNews = async () => {
  newsPosting.value = true
  newsMsg.value = ''
  try {
    const content = quill ? quill.root.innerHTML : newsForm.value.content
    const payload = { 
      title: newsForm.value.title, 
      content: content, 
      image_url: newsForm.value.image_url || null,
      category: newsForm.value.category
    }
    const res = await fetch(`${API_BASE}/news/`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(payload) })
    if (!checkAuth(res)) return
    if (!res.ok) throw new Error('Erro ao publicar.')
    newsSuccess.value = true
    newsMsg.value = '✅ Notícia publicada com sucesso!'
    newsForm.value = { title: '', content: '', image_url: '', category: 'Geral' }
    if (quill) quill.setContents([])
    await loadNews()
    setTimeout(() => newsMsg.value = '', 5000)
  } catch (err) {
    newsSuccess.value = false
    newsMsg.value = err.message
  } finally {
    newsPosting.value = false
  }
}

const deleteNews = async (id) => {
  if (!confirm('Excluir esta notícia?')) return
  const res = await fetch(`${API_BASE}/news/${id}`, { method: 'DELETE', headers: authHeaders() })
  if (checkAuth(res)) await loadNews()
}

// ---- Banners ----
const loadBanners = async () => {
  const res = await fetch(`${API_BASE}/banners/`)
  if (res.ok) bannersList.value = await res.json()
}

const createBanner = async () => {
  bannerPosting.value = true
  bannerMsg.value = ''
  try {
    const res = await fetch(`${API_BASE}/banners/`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(bannerForm.value) })
    if (!checkAuth(res)) return
    if (!res.ok) throw new Error('Erro ao criar banner.')
    bannerSuccess.value = true
    bannerMsg.value = '✅ Banner adicionado com sucesso!'
    bannerForm.value = { title: '', subtitle: '', image_url: '', link_url: '', is_active: true }
    await loadBanners()
    setTimeout(() => bannerMsg.value = '', 5000)
  } catch (err) {
    bannerSuccess.value = false
    bannerMsg.value = err.message
  } finally {
    bannerPosting.value = false
  }
}

const toggleBanner = async (id) => {
  const res = await fetch(`${API_BASE}/banners/${id}/toggle`, { method: 'PATCH', headers: authHeaders() })
  if (checkAuth(res)) await loadBanners()
}

const deleteBanner = async (id) => {
  if (!confirm('Excluir este banner?')) return
  const res = await fetch(`${API_BASE}/banners/${id}`, { method: 'DELETE', headers: authHeaders() })
  if (checkAuth(res)) await loadBanners()
}
</script>
