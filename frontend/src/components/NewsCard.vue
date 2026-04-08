<template>
  <article 
    :class="[
      'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl transition-all shadow-sm dark:shadow-xl relative overflow-hidden group mb-4',
      variant === 'compact' ? 'p-4' : 'p-6'
    ]"
  >
    <!-- Image -->
    <div v-if="article.image_url" :class="[variant === 'compact' ? 'h-32' : 'h-48', 'w-full overflow-hidden mb-4 rounded-lg']">
      <img :src="article.image_url" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" :alt="article.title" />
    </div>

    <!-- Category Tag -->
    <div class="mb-2">
      <span class="text-[10px] font-black uppercase tracking-widest px-2 py-0.5 bg-rose-600 text-white rounded">
        {{ article.category || 'Geral' }}
      </span>
    </div>

    <h3 :class="[variant === 'compact' ? 'text-lg' : 'text-2xl', 'font-bold text-slate-900 dark:text-white mb-2 leading-tight group-hover:text-rose-600 transition-colors']">
      {{ article.title }}
    </h3>
    
    <p v-if="variant !== 'compact'" class="text-xs text-slate-400 font-mono tracking-wider mb-4">{{ new Date(article.created_at).toLocaleString('pt-BR') }}</p>
    
    <p v-if="variant !== 'compact'" class="text-slate-600 dark:text-slate-300 leading-relaxed mb-6 line-clamp-3">{{ getSnippet(article.content) }}</p>
    
    <div class="flex justify-between items-center mt-auto">
      <router-link :to="`/news/${article.id}`" class="text-rose-600 dark:text-rose-500 text-sm font-bold hover:underline italic">Leia Mais &rarr;</router-link>
    </div>
  </article>
</template>

<script setup>
const props = defineProps({
  article: Object,
  variant: {
    type: String,
    default: 'default'
  }
})

const getSnippet = (text) => {
    if(!text) return ''
    // Remove tags HTML se houver (por conta do Quill)
    const cleanText = text.replace(/<[^>]*>?/gm, '')
    return cleanText.substring(0, 120) + '...'
}
</script>
