<template>
  <div>
    <!-- ═══════ LOGIN ═══════ -->
    <div
      v-if="!token"
      class="max-w-md mx-auto mt-12 p-8 rounded-2xl fade-up"
      style="background: var(--bg-card); border: 1px solid var(--border);"
    >
      <div class="flex items-center gap-3 mb-8">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center" style="background: var(--brand);">
          <span class="text-white font-black">JP</span>
        </div>
        <h2 class="text-xl font-bold" style="color: var(--text-primary);">Painel Editorial</h2>
      </div>

      <form @submit.prevent="login" class="flex flex-col gap-4">
        <div>
          <label class="block text-xs font-bold uppercase tracking-wider mb-2" style="color: var(--text-muted);">Usuário</label>
          <input
            id="input-username"
            v-model="username"
            type="text"
            required
            autocomplete="username"
            class="w-full rounded-lg px-4 py-3 text-sm outline-none transition-all"
            style="background: var(--bg-surface); border: 1px solid var(--border); color: var(--text-primary);"
            @focus="e => e.target.style.borderColor = 'var(--brand)'"
            @blur="e => e.target.style.borderColor = 'var(--border)'"
          />
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-wider mb-2" style="color: var(--text-muted);">Senha</label>
          <input
            id="input-password"
            v-model="password"
            type="password"
            required
            autocomplete="current-password"
            class="w-full rounded-lg px-4 py-3 text-sm outline-none transition-all"
            style="background: var(--bg-surface); border: 1px solid var(--border); color: var(--text-primary);"
            @focus="e => e.target.style.borderColor = 'var(--brand)'"
            @blur="e => e.target.style.borderColor = 'var(--border)'"
          />
        </div>
        <div v-if="loginError" class="text-sm font-bold px-4 py-3 rounded-lg" style="background: rgba(225,29,72,0.1); color: var(--brand);">
          {{ loginError }}
        </div>
        <button
          id="btn-login"
          type="submit"
          :disabled="loginLoading"
          class="mt-2 w-full py-3 rounded-xl font-bold text-sm text-white transition-opacity disabled:opacity-50"
          style="background: var(--brand);"
        >
          {{ loginLoading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>
    </div>

    <!-- ═══════ DASHBOARD ═══════ -->
    <div v-else class="flex flex-col gap-8">

      <!-- Header -->
      <div class="flex justify-between items-center pb-5 fade-up" style="border-bottom: 1px solid var(--border);">
        <div class="flex items-center gap-3">
          <div class="w-1.5 h-8 rounded-full" style="background: var(--brand);"></div>
          <h2 class="text-2xl font-bold" style="color: var(--text-primary);">Painel do Admin</h2>
        </div>
        <button
          id="btn-logout"
          @click="logout"
          class="text-sm transition-colors hover:opacity-80"
          style="color: var(--text-muted);"
        >
          Sair →
        </button>
      </div>

      <!-- Tabs -->
      <div style="border-bottom: 1px solid var(--border);" class="flex gap-0">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :id="`admin-tab-${tab.id}`"
          @click="activeTab = tab.id"
          :class="['tab-btn', activeTab === tab.id ? 'active' : '']"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- ── TAB: Gerenciar ── -->
      <section
        v-if="activeTab === 'manage'"
        class="rounded-2xl p-6 fade-up"
        style="background: var(--bg-card); border: 1px solid var(--border);"
      >
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-bold" style="color: var(--text-primary);">📋 Gerenciar Matérias</h3>
          <button
            id="btn-new-article"
            @click="activeTab = 'news'; resetForm()"
            class="text-sm font-bold px-4 py-2 rounded-xl text-white transition-opacity hover:opacity-90"
            style="background: var(--brand);"
          >
            + Nova Notícia
          </button>
        </div>

        <div v-if="newsLoading" class="flex flex-col gap-3">
          <div v-for="i in 4" :key="i" class="skeleton" style="height: 52px;"></div>
        </div>
        <div v-else-if="allNews.length === 0" class="text-center py-10" style="color: var(--text-muted);">
          Nenhuma notícia publicada ainda.
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr style="border-bottom: 1px solid var(--border);">
                <th class="py-3 px-4 text-xs font-bold uppercase tracking-wider" style="color: var(--text-muted);">Título</th>
                <th class="py-3 px-4 text-xs font-bold uppercase tracking-wider" style="color: var(--text-muted);">Categoria</th>
                <th class="py-3 px-4 text-xs font-bold uppercase tracking-wider" style="color: var(--text-muted);">Data</th>
                <th class="py-3 px-4 text-xs font-bold uppercase tracking-wider text-right" style="color: var(--text-muted);">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in allNews"
                :key="item.id"
                class="transition-colors"
                style="border-bottom: 1px solid var(--border);"
                @mouseenter="e => e.currentTarget.style.background = 'var(--bg-card-hover)'"
                @mouseleave="e => e.currentTarget.style.background = 'transparent'"
              >
                <td class="py-3 px-4 text-sm font-medium max-w-xs truncate" style="color: var(--text-primary);">{{ item.title }}</td>
                <td class="py-3 px-4 text-xs" style="color: var(--text-secondary);">{{ item.category }}</td>
                <td class="py-3 px-4 text-xs font-mono-jp" style="color: var(--text-muted);">{{ new Date(item.created_at).toLocaleDateString('pt-BR') }}</td>
                <td class="py-3 px-4 text-right">
                  <div class="flex justify-end gap-2">
                    <button
                      :id="`btn-edit-${item.id}`"
                      @click="prepareEdit(item)"
                      class="p-1.5 rounded-lg transition-colors text-base"
                      style="color: var(--text-muted);"
                      title="Editar"
                    >✏️</button>
                    <button
                      :id="`btn-delete-${item.id}`"
                      @click="deleteNews(item.id)"
                      class="p-1.5 rounded-lg transition-colors text-base"
                      style="color: var(--text-muted);"
                      title="Excluir"
                    >🗑️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ── TAB: Postar ── -->
      <section
        v-if="activeTab === 'news'"
        class="rounded-2xl p-6 fade-up"
        style="background: var(--bg-card); border: 1px solid var(--border);"
      >
        <div class="flex justify-between items-center mb-6 flex-wrap gap-3">
          <h3 class="text-lg font-bold" style="color: var(--text-primary);">
            {{ isEditing ? '✏️ Editar Matéria' : '📰 Nova Matéria' }}
          </h3>
          <!-- Templates -->
          <div class="flex gap-2 flex-wrap">
            <button
              id="btn-template-furo"
              @click="applyTemplate('furo')"
              class="text-xs font-bold px-3 py-1.5 rounded-full transition-opacity hover:opacity-80"
              style="background: rgba(249,115,22,0.15); color: #f97316;"
            >🚨 FURO</button>
            <button
              id="btn-template-opinion"
              @click="applyTemplate('opinion')"
              class="text-xs font-bold px-3 py-1.5 rounded-full transition-opacity hover:opacity-80"
              style="background: rgba(59,130,246,0.15); color: #3b82f6;"
            >✍️ OPINIÃO</button>
            <button
              id="btn-template-rapida"
              @click="applyTemplate('rapidinha')"
              class="text-xs font-bold px-3 py-1.5 rounded-full transition-opacity hover:opacity-80"
              style="background: rgba(16,185,129,0.15); color: #10b981;"
            >⚡ RÁPIDA</button>
          </div>
        </div>

        <form @submit.prevent="createNews" class="flex flex-col gap-5">
          <!-- Title + AI -->
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider mb-2" style="color: var(--text-muted);">Manchete*</label>
            <div class="flex gap-2">
              <input
                id="input-title"
                v-model="newsForm.title"
                type="text"
                required
                placeholder="Ex: Governo anuncia novas medidas..."
                class="flex-1 rounded-xl px-4 py-3 text-sm outline-none transition-all"
                style="background: var(--bg-surface); border: 1px solid var(--border); color: var(--text-primary);"
                @focus="e => e.target.style.borderColor = 'var(--brand)'"
                @blur="e => e.target.style.borderColor = 'var(--border)'"
              />
              <button
                id="btn-ai-title"
                type="button"
                @click="improveTitle"
                class="px-4 rounded-xl text-xs font-bold transition-opacity hover:opacity-80 flex-shrink-0"
                style="background: var(--bg-surface); border: 1px solid var(--border); color: var(--text-secondary);"
                title="Otimizar título"
              >✨ IA</button>
            </div>
          </div>

          <!-- Image + Category -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider mb-2" style="color: var(--text-muted);">URL da Imagem</label>
              <input
                id="input-image-url"
                v-model="newsForm.image_url"
                type="url"
                placeholder="https://..."
                class="w-full rounded-xl px-4 py-3 text-sm outline-none transition-all"
                style="background: var(--bg-surface); border: 1px solid var(--border); color: var(--text-primary);"
                @focus="e => e.target.style.borderColor = 'var(--brand)'"
                @blur="e => e.target.style.borderColor = 'var(--border)'"
              />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider mb-2" style="color: var(--text-muted);">Categoria*</label>
              <select
                id="select-category"
                v-model="newsForm.category"
                required
                class="w-full rounded-xl px-4 py-3 text-sm outline-none transition-all"
                style="background: var(--bg-surface); border: 1px solid var(--border); color: var(--text-primary);"
                @focus="e => e.target.style.borderColor = 'var(--brand)'"
                @blur="e => e.target.style.borderColor = 'var(--border)'"
              >
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

          <!-- Rich Text Editor -->
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider mb-2" style="color: var(--text-muted);">Conteúdo*</label>
            <div id="editor-container" style="background: white; border-radius: 0 0 10px 10px; height: 320px;"></div>
          </div>

          <!-- Feedback message -->
          <div v-if="newsMsg" class="px-4 py-3 rounded-xl text-sm font-bold"
               :style="newsSuccess
                 ? 'background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.2);'
                 : 'background: rgba(225,29,72,0.1); color: var(--brand); border: 1px solid rgba(225,29,72,0.2);'"
          >{{ newsMsg }}</div>

          <!-- Actions -->
          <div class="flex gap-3">
            <button
              id="btn-submit-news"
              type="submit"
              :disabled="newsPosting"
              class="font-bold py-3 px-8 rounded-xl text-white transition-opacity disabled:opacity-50"
              style="background: var(--brand);"
            >
              {{ newsPosting ? 'Processando...' : (isEditing ? '💾 Salvar' : '🚀 Publicar') }}
            </button>
            <button
              v-if="isEditing"
              id="btn-cancel-edit"
              type="button"
              @click="resetForm"
              class="font-bold py-3 px-8 rounded-xl transition-opacity hover:opacity-80"
              style="background: var(--bg-surface); border: 1px solid var(--border); color: var(--text-secondary);"
            >Cancelar</button>
          </div>
        </form>
      </section>

      <!-- ── TAB: Banners ── -->
      <section
        v-if="activeTab === 'banners'"
        class="rounded-2xl p-6 fade-up"
        style="background: var(--bg-card); border: 1px solid var(--border);"
      >
        <h3 class="text-lg font-bold mb-6" style="color: var(--text-primary);">🖼️ Gerenciar Banners de Destaque</h3>
        <form @submit.prevent="createBanner" class="flex flex-col gap-4 max-w-xl">
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider mb-2" style="color: var(--text-muted);">Título do Banner*</label>
            <input
              id="input-banner-title"
              v-model="bannerForm.title"
              type="text"
              required
              placeholder="Ex: Eleições 2026..."
              class="w-full rounded-xl px-4 py-3 text-sm outline-none"
              style="background: var(--bg-surface); border: 1px solid var(--border); color: var(--text-primary);"
            />
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider mb-2" style="color: var(--text-muted);">URL da Imagem*</label>
            <input
              id="input-banner-image"
              v-model="bannerForm.image_url"
              type="text"
              required
              placeholder="/images/hero_banner.png"
              class="w-full rounded-xl px-4 py-3 text-sm outline-none"
              style="background: var(--bg-surface); border: 1px solid var(--border); color: var(--text-primary);"
            />
          </div>
          <button
            id="btn-add-banner"
            type="submit"
            :disabled="bannerPosting"
            class="self-start font-bold py-3 px-8 rounded-xl text-white transition-opacity disabled:opacity-50"
            style="background: var(--brand);"
          >
            {{ bannerPosting ? 'Publicando...' : '+ Adicionar Banner' }}
          </button>
        </form>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

// Quill is loaded dynamically to avoid polluting the main bundle

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ── Auth ──────────────────────────────────────────────────────────────────────
const token        = ref('')
const username     = ref('')
const password     = ref('')
const loginError   = ref('')
const loginLoading = ref(false)

// ── Tabs ──────────────────────────────────────────────────────────────────────
const activeTab = ref('manage')
const tabs = [
  { id: 'manage',  label: '📋 Gerenciar' },
  { id: 'news',    label: '📰 Postar' },
  { id: 'banners', label: '🖼️ Banners' },
]

// ── News data ─────────────────────────────────────────────────────────────────
const allNews    = ref([])
const newsLoading = ref(false)
const isEditing  = ref(false)
const editingId  = ref(null)

// ── Forms ─────────────────────────────────────────────────────────────────────
const newsForm    = ref({ title: '', content: '', image_url: '', category: 'Geral' })
const newsPosting = ref(false)
const newsMsg     = ref('')
const newsSuccess = ref(false)

const bannerForm    = ref({ title: '', subtitle: '', image_url: '', link_url: '', is_active: true })
const bannerPosting = ref(false)

// ── Quill editor ──────────────────────────────────────────────────────────────
let quill = null

const initEditor = async () => {
  if (quill) return
  try {
    // Dynamic import: Quill only loads when admin navigates to the post tab
    const [{ default: Quill }, _css] = await Promise.all([
      import('quill'),
      import('quill/dist/quill.snow.css'),
    ])
    setTimeout(() => {
      const container = document.getElementById('editor-container')
      if (!container) return
      quill = new Quill('#editor-container', {
        theme: 'snow',
        placeholder: 'Escreva o conteúdo da notícia aqui...',
        modules: {
          toolbar: [
            [{ header: [1, 2, 3, false] }],
            ['bold', 'italic', 'underline'],
            ['link', 'image'],
            ['clean'],
          ],
        },
      })
    }, 120)
  } catch (e) {
    console.error('[Admin] Quill load failed:', e)
  }
}

// ── Watchers ──────────────────────────────────────────────────────────────────
watch(activeTab, (tab) => {
  if (tab === 'news')   initEditor()
  if (tab === 'manage') fetchAllNews()
})

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(() => {
  const saved = localStorage.getItem('token')
  if (saved) {
    token.value = saved
    if (activeTab.value === 'manage') fetchAllNews()
    if (activeTab.value === 'news')   initEditor()
  }
})

// ── Auth handlers ─────────────────────────────────────────────────────────────
const login = async () => {
  loginLoading.value = true
  loginError.value   = ''
  try {
    const form = new URLSearchParams()
    form.append('username', username.value)
    form.append('password', password.value)

    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form,
    })
    if (!res.ok) throw new Error('Usuário ou senha incorretos.')
    const data = await res.json()
    token.value = data.access_token
    localStorage.setItem('token', token.value)
    fetchAllNews()
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

/** Handle 401: session expired → auto-logout */
const handleUnauthorized = () => {
  logout()
  loginError.value = 'Sessão expirada. Faça login novamente.'
}

// ── News CRUD ─────────────────────────────────────────────────────────────────
const fetchAllNews = async () => {
  newsLoading.value = true
  try {
    const res = await fetch(`${API_BASE}/news/`)
    if (res.ok) allNews.value = await res.json()
  } catch (err) {
    console.error(err)
  } finally {
    newsLoading.value = false
  }
}

const createNews = async () => {
  newsPosting.value = true
  newsMsg.value     = ''
  try {
    const content = quill ? quill.root.innerHTML : newsForm.value.content
    const payload = { ...newsForm.value, content }

    const url    = isEditing.value ? `${API_BASE}/news/${editingId.value}` : `${API_BASE}/news/`
    const method = isEditing.value ? 'PUT' : 'POST'

    const res = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token.value}`,
      },
      body: JSON.stringify(payload),
    })

    if (res.status === 401) { handleUnauthorized(); return }
    if (!res.ok) throw new Error('Erro ao processar requisição.')

    newsSuccess.value = true
    newsMsg.value     = isEditing.value ? '✅ Matéria atualizada!' : '✅ Notícia publicada!'

    setTimeout(() => {
      resetForm()
      activeTab.value = 'manage'
      fetchAllNews()
    }, 1500)
  } catch (err) {
    newsMsg.value     = err.message
    newsSuccess.value = false
  } finally {
    newsPosting.value = false
  }
}

const deleteNews = async (id) => {
  if (!confirm('Tem certeza que deseja excluir esta notícia?')) return
  try {
    const res = await fetch(`${API_BASE}/news/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` },
    })
    if (res.status === 401) { handleUnauthorized(); return }
    if (!res.ok) throw new Error('Erro ao excluir.')
    fetchAllNews()
  } catch (err) {
    alert(err.message)
  }
}

const prepareEdit = (item) => {
  isEditing.value = true
  editingId.value = item.id
  newsForm.value  = {
    title:     item.title,
    image_url: item.image_url || '',
    category:  item.category  || 'Geral',
    content:   item.content   || '',
  }
  activeTab.value = 'news'
  setTimeout(() => {
    initEditor()
    if (quill) quill.root.innerHTML = item.content || ''
  }, 200)
}

const resetForm = () => {
  isEditing.value = false
  editingId.value = null
  newsForm.value  = { title: '', content: '', image_url: '', category: 'Geral' }
  if (quill) quill.setContents([])
  newsMsg.value   = ''
}

// ── Templates ─────────────────────────────────────────────────────────────────
const applyTemplate = (type) => {
  if (type === 'furo')      { newsForm.value.title = '🚨 [URGENTE] ';  newsForm.value.category = 'Política' }
  if (type === 'opinion')   { newsForm.value.title = 'ANÁLISE: ';       newsForm.value.category = 'Geral' }
  if (type === 'rapidinha') { newsForm.value.title = '⚡ ';              newsForm.value.category = 'Entretenimento' }
}

const improveTitle = () => {
  if (!newsForm.value.title) return
  const options = [
    `BOMBA: ${newsForm.value.title}`,
    `${newsForm.value.title} — Entenda o Impacto`,
    `EXCLUSIVO: ${newsForm.value.title}`,
    `${newsForm.value.title}: O que Ninguém Está Contando`,
  ]
  newsForm.value.title = options[Math.floor(Math.random() * options.length)]
}

// ── Banners ───────────────────────────────────────────────────────────────────
const createBanner = async () => {
  bannerPosting.value = true
  try {
    const res = await fetch(`${API_BASE}/banners/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token.value}`,
      },
      body: JSON.stringify(bannerForm.value),
    })
    if (res.status === 401) { handleUnauthorized(); return }
    if (!res.ok) throw new Error('Erro ao criar banner.')
    bannerForm.value = { title: '', subtitle: '', image_url: '', link_url: '', is_active: true }
    alert('Banner adicionado com sucesso!')
  } catch (err) {
    alert(err.message)
  } finally {
    bannerPosting.value = false
  }
}
</script>
