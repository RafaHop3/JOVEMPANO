<template>
  <a
    :href="article.link"
    target="_blank"
    rel="noopener noreferrer"
    :class="['feed-card', 'group', article.is_positive ? 'positive-highlight' : '']"
  >
    <!-- Image -->
    <div class="overflow-hidden relative" style="height: 160px; background: #050811;">
      <img
        v-if="article.image_url"
        :src="article.image_url"
        :alt="article.title"
        class="feed-card-img"
        loading="lazy"
        decoding="async"
      />
      <div v-else class="w-full h-full flex items-center justify-center bg-slate-950/80">
        <VoidGlyph shape="cluster" size="40" color="#00fff5" class="opacity-25" />
      </div>
    </div>

    <!-- Content -->
    <div class="p-4 flex flex-col gap-2 flex-1">
      <!-- Meta row -->
      <div class="flex items-center justify-between gap-2">
        <span
          class="text-[9px] font-mono font-black uppercase tracking-widest px-2 py-0.5 rounded flex-shrink-0 border border-cyan-500/20"
          :style="`background: ${catBg}; color: ${catColor};`"
        >{{ article.category }}</span>
        <span class="font-mono text-[9px] text-slate-400 truncate">
          {{ article.source }}
        </span>
      </div>

      <!-- Title -->
      <div v-if="article.is_positive" class="cyber-badge-positive">
        [ IMPACTO POSITIVO ]
      </div>
      <h3 class="text-sm font-bold leading-snug line-clamp-3 text-white group-hover:text-neon-cyan transition-colors duration-200">
        {{ article.title }}
      </h3>

      <!-- Date + external indicator -->
      <p class="font-mono text-[10px] mt-auto flex items-center justify-between text-slate-400">
        <span>{{ formatDate(article.published_at) }}</span>
        <span class="text-neon-cyan text-[9px] font-mono font-bold tracking-wider">↗ EXTERNO</span>
      </p>
    </div>
  </a>
</template>

<script setup>
import { computed } from 'vue'
import VoidGlyph from './VoidGlyph.vue'

const props = defineProps({
  article: { type: Object, required: true },
})

const CAT_COLORS = {
  'Política':       { color: '#f43f5e', bg: 'rgba(244, 63, 94, 0.15)' },
  'Politica':       { color: '#f43f5e', bg: 'rgba(244, 63, 94, 0.15)' },
  'Economia':       { color: '#10b981', bg: 'rgba(16, 185, 129, 0.15)' },
  'Esportes':       { color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.15)' },
  'Tecnologia':     { color: '#00fff5', bg: 'rgba(0, 255, 245, 0.15)' },
  'Mundo':          { color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.15)' },
  'Entretenimento': { color: '#a855f7', bg: 'rgba(168, 85, 247, 0.15)' },
  'Geral':          { color: '#7eb8e0', bg: 'rgba(126, 184, 224, 0.15)' },
}

const catColor = computed(() => CAT_COLORS[props.article?.category]?.color || '#00fff5')
const catBg    = computed(() => CAT_COLORS[props.article?.category]?.bg    || 'rgba(0, 255, 245, 0.15)')

const formatDate = (d) => {
  if (!d) return ''
  try {
    return new Date(d).toLocaleDateString('pt-BR', {
      day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit',
    })
  } catch { return '' }
}
</script>

<style scoped>
.cyber-badge-positive {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.35);
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.65rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 2px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.positive-highlight {
  border-color: rgba(16, 185, 129, 0.4) !important;
}
</style>
