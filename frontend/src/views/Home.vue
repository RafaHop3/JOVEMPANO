<template>
  <div>
    <h2 class="text-3xl font-bold text-white mb-8 border-b border-slate-800 pb-4">Feed de Notícias</h2>
    <div v-if="loading" class="text-slate-500 animate-pulse">Carregando novidades do frontend...</div>
    <div v-else-if="news.length === 0" class="text-slate-500 bg-slate-900 border border-slate-800 p-8 rounded-xl text-center shadow-lg">
      <p class="text-xl font-bold text-white mb-2">Nada por aqui ainda.</p>
      Nenhuma notícia cadastrada. Acesse o Painel Admin para criar a sua primeira matéria!
    </div>
    <div v-else class="grid gap-8">
      <article v-for="item in news" :key="item.id" class="bg-slate-900 border border-slate-800 rounded-xl p-8 hover:border-slate-700 transition-colors shadow-lg relative overflow-hidden group">
        <div class="absolute top-0 left-0 w-1 h-full bg-rose-600 group-hover:bg-rose-500 transition-colors"></div>
        <h3 class="text-3xl font-bold text-white mb-2 leading-tight">{{ item.title }}</h3>
        <p class="text-xs text-rose-500 font-mono tracking-wider mb-6">{{ new Date(item.created_at).toLocaleString('pt-BR') }}</p>
        <div class="prose prose-invert max-w-none text-slate-300 text-lg leading-relaxed" v-html="formatMarkdown(item.content)"></div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const news = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/news/')
    news.value = await res.json()
  } catch (error) {
    console.error("Failed to fetch news:", error)
  } finally {
    loading.value = false
  }
})

const formatMarkdown = (text) => {
    if(!text) return ''
    return text.replace(/\n/g, '<br>')
}
</script>
