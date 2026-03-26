<template>
  <div class="grid grid-cols-1 lg:grid-cols-[70%_30%] gap-8">
    <!-- Left Column (70%) -->
    <section>
      <div class="flex justify-between items-center mb-8 border-b border-slate-200 dark:border-slate-800 pb-4">
        <h2 class="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">Últimas Publicações</h2>
        <span class="text-xs font-bold text-rose-600 px-3 py-1 bg-rose-600/10 rounded-full uppercase">Ao Vivo</span>
      </div>
      
      <div v-if="loading" class="space-y-6">
        <div v-for="i in 3" :key="i" class="h-32 bg-slate-200 dark:bg-slate-900 animate-pulse rounded-xl"></div>
      </div>
      
      <div v-else-if="news.length === 0" class="text-slate-500 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-12 rounded-xl text-center shadow-lg">
        <div class="w-16 h-16 bg-slate-100 dark:bg-slate-800 rounded-full mx-auto flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path></svg>
        </div>
        <p class="text-xl font-bold text-slate-900 dark:text-white mb-2">A redação está quieta.</p>
        <p class="text-slate-500">Nenhuma transmissão captada nas últimas horas.</p>
      </div>
      
      <div v-else>
        <!-- Feed de Notícias com Transição -->
        <NewsCard 
            v-for="item in news" 
            :key="item.id" 
            :article="item" 
            :isExpanded="expandedId === item.id"
            @toggle="toggleExpand(item.id)"
        />
      </div>
    </section>

    <!-- Right Column (30%) -->
    <SidebarWidget />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useHead } from '@unhead/vue'
import NewsCard from '../components/NewsCard.vue'
import SidebarWidget from '../components/SidebarWidget.vue'

// SEO
useHead({
  title: 'JOVEMPANO - Feed em Tempo Real',
  meta: [
    { name: 'description', content: 'Notícias exclusivas e curadoria humana sem filtros.' }
  ]
})

const news = ref([])
const loading = ref(true)
const expandedId = ref(null)

const toggleExpand = (id) => {
    if (expandedId.value === id) {
        expandedId.value = null
    } else {
        expandedId.value = id
    }
}

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/news/')
    if (!res.ok) throw new Error('Falha na conexão com o motor.')
    news.value = await res.json()
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>
