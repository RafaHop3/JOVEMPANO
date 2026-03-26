<template>
  <article 
    :class="[
      'bg-white dark:bg-slate-900 border transition-all duration-500 rounded-xl relative overflow-hidden group mb-6 shadow-sm dark:shadow-xl',
      isExpanded ? 'border-rose-600 ring-2 ring-rose-500/20' : 'border-slate-200 dark:border-slate-800 hover:border-rose-500/50'
    ]"
  >
    <!-- Border Accent -->
    <div :class="['absolute top-0 left-0 w-1.5 h-full transition-colors duration-500', isExpanded ? 'bg-rose-600' : 'bg-slate-300 dark:bg-slate-800 group-hover:bg-rose-500']"></div>
    
    <div class="p-6">
      <div class="flex justify-between items-start mb-2">
        <h3 :class="['font-bold text-slate-900 dark:text-white leading-tight transition-all', isExpanded ? 'text-3xl mb-4' : 'text-xl']">
          {{ article.title }}
        </h3>
        <button 
          @click="$emit('toggle')" 
          :class="['p-2 rounded-full transition-colors', isExpanded ? 'bg-rose-600 text-white' : 'text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800']"
        >
          <svg class="w-5 h-5 transition-transform duration-500" :class="{ 'rotate-45': isExpanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
        </button>
      </div>

      <p class="text-xs text-rose-600 font-mono tracking-wider mb-4">
        {{ new Date(article.created_at).toLocaleString('pt-BR') }}
      </p>
      
      <!-- Content Area -->
      <transition 
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="transform opacity-0 -translate-y-2"
        enter-to-class="transform opacity-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="transform opacity-100 translate-y-0"
        leave-to-class="transform opacity-0 -translate-y-2"
      >
        <div v-if="isExpanded" class="mt-4 border-t border-slate-100 dark:border-slate-800 pt-6">
          <div class="prose dark:prose-invert max-w-none text-slate-700 dark:text-slate-300 leading-loose whitespace-pre-wrap">
            {{ article.content }}
          </div>
          <div class="mt-8 flex justify-end">
            <button @click="$emit('toggle')" class="bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-bold py-2 px-6 rounded-lg hover:bg-rose-600 hover:text-white transition-all">
              Fechar Notícia
            </button>
          </div>
        </div>
        <div v-else>
          <p class="text-slate-600 dark:text-slate-400 leading-relaxed line-clamp-2 italic">
            {{ getSnippet(article.content) }}
          </p>
          <button @click="$emit('toggle')" class="mt-4 text-rose-600 dark:text-rose-500 font-bold hover:underline flex items-center gap-1">
            Ler notícia completa <span>&darr;</span>
          </button>
        </div>
      </transition>
    </div>
  </article>
</template>

<script setup>
const props = defineProps(['article', 'isExpanded'])
const emit = defineEmits(['toggle'])

const getSnippet = (text) => {
    if(!text) return ''
    return text.replace(/[#*`_]/g, '').substring(0, 150) + '...'
}
</script>
