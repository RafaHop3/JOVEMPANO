<template>
  <a
    :href="article.link"
    target="_blank"
    rel="noopener noreferrer"
    class="feed-card group"
  >
    <!-- Image -->
    <div class="overflow-hidden" style="height: 160px; background: var(--bg-surface);">
      <img
        v-if="article.image_url"
        :src="article.image_url"
        :alt="article.title"
        class="feed-card-img"
        loading="lazy"
      />
      <div v-else class="w-full h-full flex items-center justify-center">
        <span class="text-5xl" style="opacity: 0.08;">📰</span>
      </div>
    </div>

    <!-- Content -->
    <div class="p-4 flex flex-col gap-2 flex-1">
      <!-- Meta row -->
      <div class="flex items-center justify-between gap-2">
        <span
          class="text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded flex-shrink-0"
          :style="`background: ${catBg}; color: ${catColor};`"
        >{{ article.category }}</span>
        <span class="font-mono-jp text-[9px] truncate" style="color: var(--text-muted);">
          {{ article.source }}
        </span>
      </div>

      <!-- Title -->
      <h3 class="text-sm font-bold leading-snug line-clamp-3 group-hover:text-rose-300 transition-colors duration-200"
          style="color: var(--text-primary);">
        {{ article.title }}
      </h3>

      <!-- Date + external indicator -->
      <p class="font-mono-jp text-[10px] mt-auto flex items-center justify-between"
         style="color: var(--text-muted);">
        <span>{{ formatDate(article.published_at) }}</span>
        <span style="color: var(--brand);" class="text-[9px] font-bold">↗ externo</span>
      </p>
    </div>
  </a>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  article: { type: Object, required: true },
})

const CAT_COLORS = {
  'Política':       { color: 'var(--cat-politica)',       bg: 'var(--cat-politica-bg)' },
  'Economia':       { color: 'var(--cat-economia)',       bg: 'var(--cat-economia-bg)' },
  'Esportes':       { color: 'var(--cat-esportes)',       bg: 'var(--cat-esportes-bg)' },
  'Tecnologia':     { color: 'var(--cat-tecnologia)',     bg: 'var(--cat-tecnologia-bg)' },
  'Mundo':          { color: 'var(--cat-mundo)',          bg: 'var(--cat-mundo-bg)' },
  'Entretenimento': { color: 'var(--cat-entretenimento)', bg: 'var(--cat-entretenimento-bg)' },
  'Geral':          { color: 'var(--cat-geral)',          bg: 'var(--cat-geral-bg)' },
}

const catColor = computed(() => CAT_COLORS[props.article?.category]?.color || 'var(--cat-geral)')
const catBg    = computed(() => CAT_COLORS[props.article?.category]?.bg    || 'var(--cat-geral-bg)')

const formatDate = (d) => {
  if (!d) return ''
  try {
    return new Date(d).toLocaleDateString('pt-BR', {
      day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit',
    })
  } catch { return '' }
}
</script>
