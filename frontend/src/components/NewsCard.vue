<template>
  <article class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 hover:border-rose-500/50 transition-colors shadow-sm dark:shadow-xl relative overflow-hidden group mb-6">
    <div class="absolute top-0 left-0 w-1 h-full bg-rose-600 transition-colors"></div>
    <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-2 leading-tight">{{ article.title }}</h3>
    <p class="text-xs text-rose-600 font-mono tracking-wider mb-4">{{ new Date(article.created_at).toLocaleString('pt-BR') }}</p>
    
    <p class="text-slate-600 dark:text-slate-300 leading-relaxed mb-6 line-clamp-3">{{ getSnippet(article.content) }}</p>
    
    <div class="flex justify-between items-center mt-4">
      <router-link :to="`/news/${article.id}`" class="text-rose-600 dark:text-rose-500 font-bold hover:underline">Leia Mais &rarr;</router-link>
      <div class="flex gap-2">
        <button class="text-slate-400 hover:text-rose-500 transition-colors" title="Compartilhar">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path></svg>
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
const props = defineProps(['article'])

const getSnippet = (text) => {
    if(!text) return ''
    return text.replace(/[#*`_]/g, '').substring(0, 180) + '...'
}
</script>
