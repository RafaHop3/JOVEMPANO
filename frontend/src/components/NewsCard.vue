<template>
  <!-- HERO VARIANT: large image with text overlay -->
  <component
    v-if="variant === 'hero'"
    :is="linkTag"
    v-bind="linkProps"
    class="hero-card group"
    :style="{ minHeight: '340px' }"
  >
    <img
      v-if="article.image_url"
      :src="article.image_url"
      :alt="article.title"
      class="hero-card-img"
      loading="eager"
      fetchpriority="high"
      decoding="async"
    />
    <div v-else class="absolute inset-0 flex items-center justify-center bg-slate-950/90">
      <VoidGlyph shape="cluster" size="64" color="#00fff5" class="opacity-40" />
    </div>
    <div class="hero-card-overlay"></div>
    <div class="hero-card-body">
      <!-- Category badge -->
      <span
        class="inline-block text-[10px] font-mono font-black uppercase tracking-widest px-2.5 py-1 rounded-md mb-3 border border-cyan-500/30"
        :style="`background: ${catBg}; color: ${catColor};`"
      >{{ article.category || 'Geral' }}</span>
      <!-- Title -->
      <h2 class="font-editorial text-2xl md:text-3xl font-bold text-white leading-tight mb-2 group-hover:text-cyan-300 transition-colors duration-200">
        {{ article.title }}
      </h2>
      <!-- Date -->
      <p class="font-mono text-xs text-slate-400">
        {{ formatDate(article.created_at) }}
      </p>
    </div>
  </component>

  <!-- SECONDARY VARIANT: horizontal thumbnail + text -->
  <component
    v-else-if="variant === 'secondary'"
    :is="linkTag"
    v-bind="linkProps"
    class="news-card group flex flex-row overflow-hidden"
    style="min-height: 130px;"
  >
    <div class="w-32 flex-shrink-0 overflow-hidden bg-slate-950/80">
      <img
        v-if="article.image_url"
        :src="article.image_url"
        :alt="article.title"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        loading="lazy"
        decoding="async"
      />
      <div v-else class="w-full h-full flex items-center justify-center">
        <VoidGlyph shape="cluster" size="32" color="#00fff5" class="opacity-30" />
      </div>
    </div>
    <div class="flex flex-col p-4 gap-1.5 flex-1">
      <span
        class="self-start text-[9px] font-mono font-black uppercase tracking-widest px-2 py-0.5 rounded border border-cyan-500/20"
        :style="`background: ${catBg}; color: ${catColor};`"
      >{{ article.category || 'Geral' }}</span>
      <h3 class="text-sm font-bold leading-snug line-clamp-3 text-white group-hover:text-cyan-300 transition-colors">
        {{ article.title }}
      </h3>
      <p class="font-mono text-[10px] text-slate-400 mt-auto">
        {{ formatDate(article.created_at) }}
      </p>
    </div>
  </component>

  <!-- DEFAULT / COMPACT VARIANT: standard vertical card -->
  <component
    v-else
    :is="linkTag"
    v-bind="linkProps"
    class="news-card group block"
  >
    <div v-if="article.image_url && variant !== 'compact'" class="h-44 overflow-hidden bg-slate-950/80">
      <img
        :src="article.image_url"
        :alt="article.title"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        loading="lazy"
        decoding="async"
      />
    </div>
    <div class="p-4 flex flex-col gap-2">
      <div class="flex items-center gap-2 flex-wrap">
        <span
          class="text-[10px] font-mono font-black uppercase tracking-widest px-2 py-0.5 rounded border border-cyan-500/20"
          :style="`background: ${catBg}; color: ${catColor};`"
        >{{ article.category || 'Geral' }}</span>
        <span class="font-mono text-[10px] text-slate-400">
          {{ formatDate(article.created_at) }}
        </span>
      </div>
      <h3
        :class="[
          variant === 'compact' ? 'text-sm' : 'text-base',
          'font-bold text-white leading-snug group-hover:text-cyan-300 transition-colors line-clamp-2'
        ]"
      >{{ article.title }}</h3>
      <p v-if="variant !== 'compact'" class="text-xs text-slate-400 line-clamp-2">
        {{ getSnippet(article.content) }}
      </p>
    </div>
  </component>
</template>

<script setup>
import { computed } from 'vue'
import VoidGlyph from './VoidGlyph.vue'

const props = defineProps({
  article: { type: Object, required: true },
  variant: { type: String, default: 'default' },
})

const isExternal = computed(() => !!props.article?.external)
const linkTag = computed(() => (isExternal.value ? 'a' : 'router-link'))
const linkProps = computed(() => {
  if (isExternal.value) {
    return {
      href: props.article.link,
      target: '_blank',
      rel: 'noopener noreferrer'
    }
  }
  return {
    to: `/news/${props.article.id}`
  }
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

const getSnippet = (html) => {
  if (!html) return ''
  return html.replace(/<[^>]*>/g, '').slice(0, 160)
}
</script>
