<template>
  <div>
    <div v-if="!token" class="max-w-md mx-auto bg-slate-900 p-8 rounded-xl shadow-lg border border-slate-800 mt-12">
      <h2 class="text-2xl font-bold mb-6 text-white text-center">Login Administrativo</h2>
      <form @submit.prevent="login" class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-slate-400 mb-1">Usuário</label>
          <input v-model="username" type="text" required class="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white focus:outline-none focus:border-rose-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-400 mb-1">Senha</label>
          <input v-model="password" type="password" required class="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white focus:outline-none focus:border-rose-500" />
        </div>
        <div v-if="error" class="text-rose-500 text-sm font-bold">{{ error }}</div>
        <button type="submit" class="mt-4 w-full bg-rose-600 hover:bg-rose-700 text-white font-bold py-2 px-4 rounded transition-colors" :disabled="loading">
          {{ loading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>
    </div>

    <div v-else class="bg-slate-900 border border-slate-800 rounded-xl p-8 shadow-xl">
      <div class="flex justify-between items-center mb-8 pb-4 border-b border-slate-800">
        <h2 class="text-3xl font-bold text-white flex items-center gap-3">
            <span class="w-3 h-8 bg-rose-600 rounded"></span>
            Publicar Nova Matéria
        </h2>
        <button @click="logout" class="text-slate-400 font-medium hover:text-white transition-colors">Sair</button>
      </div>

      <form @submit.prevent="createNews" class="flex flex-col gap-6">
        <div>
          <label class="block text-sm font-bold text-slate-300 mb-2">Manchete (Título)</label>
          <input v-model="newsTitle" type="text" placeholder="Ex: Governo anuncia novas medidas..." required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-white text-lg focus:outline-none focus:border-rose-500" />
        </div>
        
        <div>
          <label class="block text-sm font-bold text-slate-300 mb-2">Corpo da Matéria</label>
          <textarea v-model="newsContent" rows="12" placeholder="Escreva o conteúdo completo aqui..." required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-rose-500 font-mono"></textarea>
        </div>

        <div v-if="postMessage" :class="['p-4 rounded-lg font-bold text-sm', postSuccess ? 'bg-emerald-900/50 text-emerald-400 border border-emerald-800' : 'bg-rose-900/50 text-rose-400 border border-rose-800']">
            {{ postMessage }}
        </div>

        <button type="submit" class="mt-2 self-start bg-rose-600 hover:bg-rose-500 text-white font-bold py-3 px-8 rounded-lg shadow-lg hover:shadow-rose-500/20 transition-all" :disabled="posting">
          {{ posting ? 'Publicando...' : 'Publicar Agora' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const token = ref('')
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const newsTitle = ref('')
const newsContent = ref('')
const posting = ref(false)
const postMessage = ref('')
const postSuccess = ref(false)

const API_BASE = 'http://127.0.0.1:8000'

onMounted(() => {
  const savedToken = localStorage.getItem('token')
  if (savedToken) {
    token.value = savedToken
  }
})

const login = async () => {
  loading.value = true
  error.value = ''
  try {
    const formData = new URLSearchParams()
    formData.append('username', username.value)
    formData.append('password', password.value)

    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData
    })
    
    if (!res.ok) throw new Error('Credenciais inválidas.')
    const data = await res.json()
    token.value = data.access_token
    localStorage.setItem('token', token.value)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const logout = () => {
    localStorage.removeItem('token')
    token.value = ''
}

const createNews = async () => {
    posting.value = true
    postMessage.value = ''
    
    try {
        const payload = {
            title: newsTitle.value,
            content: newsContent.value
        }
        
        const res = await fetch(`${API_BASE}/news/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token.value}`
            },
            body: JSON.stringify(payload)
        })
        
        if (res.status === 401) {
            logout()
            return
        }
        
        if (!res.ok) throw new Error('Erro ao publicar notícia.')
        
        postSuccess.value = true
        postMessage.value = 'Notícia publicada com sucesso no feed!'
        newsTitle.value = ''
        newsContent.value = ''
        
        setTimeout(() => {
            postMessage.value = ''
        }, 5000)
    } catch(err) {
        postSuccess.value = false
        postMessage.value = err.message
    } finally {
        posting.value = false
    }
}
</script>
