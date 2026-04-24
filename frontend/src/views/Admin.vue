<template>
  <div class="font-mono-jp bg-[#06060e] min-h-screen text-slate-300 relative z-0 flex flex-col">
    <!-- Background Elements -->
    <div class="fixed inset-0 bg-[url('/images/grid-bg.png')] bg-cover bg-center bg-fixed opacity-20 pointer-events-none z-[-2]"></div>
    <div class="fixed inset-0 bg-gradient-to-br from-black via-black/95 to-black/90 pointer-events-none z-[-1]"></div>

    <!-- ═══════ TOAST NOTIFICATIONS ═══════ -->
    <div class="fixed top-6 right-6 z-50 flex flex-col gap-3 pointer-events-none">
      <transition-group name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="pointer-events-auto flex items-center gap-4 px-6 py-4 min-w-[320px] rounded-lg border bg-black/80 shadow-2xl backdrop-blur-md"
          :class="{
            'border-green-500/50 shadow-[0_0_15px_rgba(34,197,94,0.1)]': toast.type === 'success',
            'border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.1)]': toast.type === 'error',
            'border-cyan-500/50 shadow-[0_0_15px_rgba(6,182,212,0.1)]': toast.type === 'info'
          }"
        >
          <svg v-if="toast.type === 'error'" class="w-6 h-6 text-red-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <svg v-if="toast.type === 'success'" class="w-6 h-6 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <svg v-if="toast.type === 'info'" class="w-6 h-6 text-cyan-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          
          <div class="flex flex-col">
            <span class="text-sm font-bold uppercase tracking-wide" :class="{
              'text-green-400': toast.type === 'success',
              'text-red-400': toast.type === 'error',
              'text-cyan-400': toast.type === 'info'
            }">{{ toast.title }}</span>
            <span class="text-xs text-slate-300 mt-1">{{ toast.message }}</span>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- ═══════ LOGIN ═══════ -->
    <div
      v-if="!token"
      class="flex flex-1 items-center justify-center p-6"
    >
      <div class="w-full max-w-lg p-10 bg-black/60 rounded-xl border border-white/10 backdrop-blur-md shadow-2xl flex flex-col gap-8">
        <div class="flex flex-col items-center gap-3 text-center">
          <div class="w-16 h-16 rounded-full bg-indigo-500/20 border border-indigo-500/50 flex items-center justify-center mb-2">
            <svg class="w-8 h-8 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
          </div>
          <h2 class="text-3xl font-black text-white tracking-wide">ÁREA RESTRITA</h2>
          <p class="text-sm text-indigo-300/80 uppercase tracking-widest">Painel Administrativo JovemPano</p>
        </div>

        <form @submit.prevent="login" class="flex flex-col gap-6">
          <div class="flex flex-col gap-2">
            <label class="text-xs font-bold uppercase tracking-widest text-slate-400">Usuário</label>
            <input
              v-model="username"
              type="text"
              required
              class="w-full px-5 py-4 text-base bg-black/50 border border-white/10 rounded-lg focus:border-indigo-500 outline-none transition-all text-white"
            />
          </div>
          <div class="flex flex-col gap-2">
            <label class="text-xs font-bold uppercase tracking-widest text-slate-400">Senha</label>
            <input
              v-model="password"
              type="password"
              required
              class="w-full px-5 py-4 text-base bg-black/50 border border-white/10 rounded-lg focus:border-indigo-500 outline-none transition-all text-white"
            />
          </div>
          <button
            type="submit"
            :disabled="loginLoading"
            class="mt-4 w-full py-4 rounded-lg font-bold text-sm uppercase tracking-widest transition-all bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg active:scale-[0.98] disabled:opacity-50"
          >
            <span class="flex items-center justify-center gap-3">
              <svg v-if="loginLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              {{ loginLoading ? 'AUTENTICANDO...' : 'ENTRAR' }}
            </span>
          </button>
        </form>
      </div>
    </div>

    <!-- ═══════ DASHBOARD ═══════ -->
    <div v-else class="flex flex-col flex-1 max-w-[1600px] w-full mx-auto p-4 md:p-8 gap-8">
      
      <!-- Top Header -->
      <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-6 border-b border-white/10">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg text-white font-black text-xl">
            JP
          </div>
          <div class="flex flex-col">
            <h1 class="text-2xl font-black text-white tracking-wide">
              ADMINISTRAÇÃO
            </h1>
            <p class="text-sm text-indigo-400 mt-1">
              Gerenciamento de Conteúdo
            </p>
          </div>
        </div>
        <button
          @click="logout"
          class="px-5 py-3 rounded-lg text-sm font-bold uppercase tracking-widest transition-all border border-red-500/30 text-red-400 hover:bg-red-500/10 active:scale-95 flex items-center gap-3"
        >
          <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
          Sair do Sistema
        </button>
      </header>

      <!-- Main Layout: Sidebar + Content -->
      <div class="flex flex-col lg:flex-row gap-8 flex-1">
        
        <!-- Sidebar Navigation -->
        <aside class="w-full lg:w-72 flex flex-col gap-4 flex-shrink-0">
          <div class="bg-black/40 rounded-xl border border-white/5 p-4 flex flex-col gap-2">
            <button
              @click="activeTab = 'manage'"
              class="w-full text-left px-5 py-4 rounded-lg transition-all duration-200 text-sm font-bold uppercase tracking-widest flex items-center gap-4"
              :class="activeTab === 'manage' ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' : 'text-slate-400 hover:bg-white/5 hover:text-white border border-transparent'"
            >
              <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
              Gerenciar Notícias
            </button>
            <button
              @click="activeTab = 'news'"
              class="w-full text-left px-5 py-4 rounded-lg transition-all duration-200 text-sm font-bold uppercase tracking-widest flex items-center gap-4"
              :class="activeTab === 'news' ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' : 'text-slate-400 hover:bg-white/5 hover:text-white border border-transparent'"
            >
              <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
              Postar Nova Notícia
            </button>
            <button
              @click="activeTab = 'banners'"
              class="w-full text-left px-5 py-4 rounded-lg transition-all duration-200 text-sm font-bold uppercase tracking-widest flex items-center gap-4"
              :class="activeTab === 'banners' ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' : 'text-slate-400 hover:bg-white/5 hover:text-white border border-transparent'"
            >
              <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
              Gerenciar Banners
            </button>
          </div>
        </aside>

        <!-- Right Content Area -->
        <main class="flex-1 bg-black/40 rounded-xl border border-white/5 p-6 lg:p-10 shadow-2xl overflow-y-auto min-h-[600px]">
          
          <!-- ── TAB: GERENCIAR NOTÍCIAS ── -->
          <section v-if="activeTab === 'manage'" class="flex flex-col gap-8">
            <div class="flex justify-between items-center border-b border-white/10 pb-6">
              <h3 class="text-xl font-bold text-white flex items-center gap-3">
                <svg class="w-6 h-6 text-indigo-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path></svg>
                Notícias Publicadas
              </h3>
              <span class="text-xs font-bold px-4 py-2 bg-indigo-500/10 text-indigo-300 rounded-full border border-indigo-500/20">
                {{ allNews.length }} Registros
              </span>
            </div>

            <div class="flex flex-col gap-4">
              <div v-if="newsLoading" class="flex flex-col gap-4">
                <div v-for="i in 3" :key="i" class="h-24 bg-white/5 rounded-lg animate-pulse"></div>
              </div>
              <div v-else-if="allNews.length === 0" class="p-12 text-center border border-dashed border-white/10 rounded-lg text-slate-500 text-sm">
                Nenhuma notícia encontrada no banco de dados.
              </div>
              <div
                v-else
                v-for="item in allNews"
                :key="item.id"
                class="group p-6 bg-white/5 rounded-lg border border-transparent hover:border-indigo-500/30 hover:bg-indigo-500/5 transition-all flex flex-col xl:flex-row justify-between items-start xl:items-center gap-6"
              >
                <div class="flex flex-col gap-3 flex-1">
                  <h4 class="text-white font-bold text-lg leading-snug">{{ item.title }}</h4>
                  <div class="flex flex-wrap items-center gap-4">
                    <span class="text-xs px-3 py-1 bg-white/10 text-white rounded uppercase tracking-wider">
                      {{ (item.category || 'GERAL') }}
                    </span>
                    <span class="text-xs text-slate-400 flex items-center gap-1.5">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                      {{ new Date(item.created_at).toLocaleDateString('pt-BR', { hour: '2-digit', minute: '2-digit' }) }}
                    </span>
                  </div>
                </div>
                
                <div class="flex gap-3">
                  <button @click="prepareEdit(item)" class="px-5 py-2.5 rounded-lg text-xs uppercase font-bold border border-indigo-500/50 text-indigo-300 hover:bg-indigo-500/10 transition-colors flex items-center gap-2">
                    <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                    Editar
                  </button>
                  <button @click="deleteNews(item.id)" class="px-5 py-2.5 rounded-lg text-xs uppercase font-bold border border-red-500/50 text-red-400 hover:bg-red-500/10 transition-colors flex items-center gap-2">
                    <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    Excluir
                  </button>
                </div>
              </div>
            </div>
          </section>

          <!-- ── TAB: POSTAR NOTÍCIA ── -->
          <section v-if="activeTab === 'news'" class="flex flex-col gap-8">
            <div class="flex justify-between items-center border-b border-white/10 pb-6">
              <h3 class="text-xl font-bold text-white flex items-center gap-3">
                <svg class="w-6 h-6 text-indigo-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                {{ isEditing ? 'Editar Notícia' : 'Publicar Nova Notícia' }}
              </h3>
              <button v-if="isEditing" @click="resetForm" class="text-xs font-bold uppercase text-slate-400 hover:text-white transition-colors">
                Cancelar Edição
              </button>
            </div>

            <form @submit.prevent="createNews" class="flex flex-col gap-6 max-w-4xl">
              
              <div class="flex flex-col gap-2">
                <label class="text-sm font-bold text-slate-300">Título da Notícia*</label>
                <input
                  v-model="newsForm.title"
                  type="text"
                  required
                  placeholder="Digite o título principal..."
                  class="w-full px-5 py-4 text-base bg-black/50 border border-white/10 rounded-lg focus:border-indigo-500 outline-none transition-all text-white"
                />
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="flex flex-col gap-2">
                  <label class="text-sm font-bold text-slate-300">URL da Imagem de Capa</label>
                  <input v-model="newsForm.image_url" type="url" placeholder="https://exemplo.com/imagem.jpg" class="w-full px-5 py-4 text-base bg-black/50 border border-white/10 rounded-lg focus:border-indigo-500 outline-none transition-all text-white" />
                </div>
                <div class="flex flex-col gap-2">
                  <label class="text-sm font-bold text-slate-300">Categoria*</label>
                  <select v-model="newsForm.category" required class="w-full px-5 py-4 text-base bg-black/50 border border-white/10 rounded-lg focus:border-indigo-500 outline-none transition-all text-white appearance-none">
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

              <div class="flex flex-col gap-2">
                <label class="text-sm font-bold text-slate-300">Conteúdo*</label>
                <div id="editor-container" class="bg-black/50 border border-white/10 rounded-lg overflow-hidden custom-quill-theme" style="min-height: 400px; color: white;"></div>
              </div>

              <div class="pt-6 border-t border-white/10 mt-2">
                <button type="submit" :disabled="newsPosting" class="font-bold py-4 px-10 rounded-lg text-sm uppercase tracking-widest bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg transition-all active:scale-95 disabled:opacity-50 flex items-center justify-center gap-3 w-full md:w-auto">
                  <svg v-if="newsPosting" class="animate-spin h-5 w-5 text-white flex-shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                  <svg v-else class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                  {{ newsPosting ? 'SALVANDO...' : (isEditing ? 'SALVAR ALTERAÇÕES' : 'PUBLICAR NOTÍCIA') }}
                </button>
              </div>
            </form>
          </section>

          <!-- ── TAB: BANNERS ── -->
          <section v-if="activeTab === 'banners'" class="flex flex-col gap-8">
             <div class="flex justify-between items-center border-b border-white/10 pb-6">
              <h3 class="text-xl font-bold text-white flex items-center gap-3">
                <svg class="w-6 h-6 text-indigo-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                Adicionar Novo Banner
              </h3>
            </div>
            
            <form @submit.prevent="createBanner" class="flex flex-col gap-6 max-w-4xl bg-white/5 p-8 rounded-xl border border-white/10">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="flex flex-col gap-2">
                  <label class="text-sm font-bold text-slate-300">Título do Banner*</label>
                  <input v-model="bannerForm.title" type="text" required class="w-full px-5 py-4 text-base bg-black/50 border border-white/10 rounded-lg focus:border-indigo-500 outline-none transition-all text-white" />
                </div>
                <div class="flex flex-col gap-2">
                  <label class="text-sm font-bold text-slate-300">URL da Imagem*</label>
                  <input v-model="bannerForm.image_url" type="url" required class="w-full px-5 py-4 text-base bg-black/50 border border-white/10 rounded-lg focus:border-indigo-500 outline-none transition-all text-white" />
                </div>
              </div>
              <button type="submit" :disabled="bannerPosting" class="self-start font-bold py-4 px-10 rounded-lg text-sm uppercase tracking-widest bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg transition-all active:scale-95 disabled:opacity-50 flex items-center gap-3">
                <svg v-if="bannerPosting" class="animate-spin h-5 w-5 text-white flex-shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                <svg v-else class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                {{ bannerPosting ? 'ENVIANDO...' : 'CADASTRAR BANNER' }}
              </button>
            </form>
          </section>

        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) || 'http://localhost:8000'

// ── Toast System ──────────────────────────────────────────────────────────────
const toasts = ref([])
let toastId = 0
const addToast = (title, message, type = 'info') => {
  const id = toastId++
  toasts.value.push({ id, title, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 4000)
}

// ── Auth ──────────────────────────────────────────────────────────────────────
const token        = ref('')
const username     = ref('')
const password     = ref('')
const loginLoading = ref(false)

// ── Tabs ──────────────────────────────────────────────────────────────────────
const activeTab = ref('manage') // Default to manage

// ── News data ─────────────────────────────────────────────────────────────────
const allNews    = ref([])
const newsLoading = ref(false)
const isEditing  = ref(false)
const editingId  = ref(null)

// ── Forms ─────────────────────────────────────────────────────────────────────
const newsForm    = ref({ title: '', content: '', image_url: '', category: 'Geral' })
const newsPosting = ref(false)

const bannerForm    = ref({ title: '', subtitle: '', image_url: '', link_url: '', is_active: true })
const bannerPosting = ref(false)

// ── Quill editor ──────────────────────────────────────────────────────────────
let quill = null

const initEditor = async () => {
  if (quill) return
  try {
    const QuillModule = await import('quill')
    await import('quill/dist/quill.snow.css')
    const Quill = QuillModule.default
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
    fetchAllNews()
    if (activeTab.value === 'news') initEditor()
  }
})

// ── Auth handlers ─────────────────────────────────────────────────────────────
const login = async () => {
  loginLoading.value = true
  try {
    const form = new URLSearchParams()
    form.append('username', username.value)
    form.append('password', password.value)

    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form,
    })
    if (!res.ok) throw new Error('Credenciais inválidas.')
    const data = await res.json()
    token.value = data.access_token
    localStorage.setItem('token', token.value)
    addToast('Acesso Permitido', 'Bem-vindo ao painel administrativo.', 'success')
    fetchAllNews()
  } catch (err) {
    addToast('Falha na Autenticação', err.message, 'error')
  } finally {
    loginLoading.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  token.value = ''
  addToast('Sessão Encerrada', 'Você saiu do sistema.', 'info')
}

const handleUnauthorized = () => {
  logout()
  addToast('Acesso Negado', 'Sua sessão expirou. Faça login novamente.', 'error')
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
    if (!res.ok) throw new Error('Erro na comunicação com o servidor.')

    addToast('Sucesso!', isEditing.value ? 'Notícia atualizada.' : 'Notícia publicada com sucesso.', 'success')

    setTimeout(() => {
      resetForm()
      activeTab.value = 'manage'
      fetchAllNews()
    }, 1000)
  } catch (err) {
    addToast('Erro', err.message, 'error')
  } finally {
    newsPosting.value = false
  }
}

const deleteNews = async (id) => {
  if (!confirm('Tem certeza que deseja excluir esta notícia? Esta ação não pode ser desfeita.')) return
  try {
    const res = await fetch(`${API_BASE}/news/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` },
    })
    if (res.status === 401) { handleUnauthorized(); return }
    if (!res.ok) throw new Error('Falha ao excluir notícia.')
    addToast('Excluído', 'A notícia foi removida do banco de dados.', 'success')
    fetchAllNews()
  } catch (err) {
    addToast('Erro', err.message, 'error')
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
    if (!res.ok) throw new Error('Falha ao cadastrar banner.')
    bannerForm.value = { title: '', subtitle: '', image_url: '', link_url: '', is_active: true }
    addToast('Sucesso!', 'Banner adicionado com sucesso.', 'success')
  } catch (err) {
    addToast('Erro', err.message, 'error')
  } finally {
    bannerPosting.value = false
  }
}
</script>

<style>
/* Toast Transitions */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

/* Custom Dark Theme for Quill Editor */
.custom-quill-theme .ql-toolbar {
  background: rgba(255, 255, 255, 0.05);
  border: none !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
  padding: 12px;
}
.custom-quill-theme .ql-toolbar button {
  color: #a1a1aa;
  border-radius: 4px;
  transition: all 0.2s;
}
.custom-quill-theme .ql-toolbar button:hover {
  background: rgba(255, 255, 255, 0.1);
}
.custom-quill-theme .ql-toolbar .ql-stroke {
  stroke: #a1a1aa !important;
}
.custom-quill-theme .ql-toolbar .ql-fill {
  fill: #a1a1aa !important;
}
.custom-quill-theme .ql-toolbar .ql-picker {
  color: #a1a1aa;
}
.custom-quill-theme .ql-container {
  border: none !important;
  font-family: inherit !important;
  font-size: 16px;
}
.custom-quill-theme .ql-editor {
  padding: 24px;
}
.custom-quill-theme .ql-editor.ql-blank::before {
  color: rgba(255, 255, 255, 0.3);
  font-style: normal;
}
</style>
