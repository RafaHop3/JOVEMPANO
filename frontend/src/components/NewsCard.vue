<template>
  <!-- HERO VARIANT: large image with text overlay -->
  <component
    v-if="variant === 'hero'"
    :is="linkTag"
    v-bind="linkProps"
    class="hero-card group"
    :style="{ minHeight: '320px' }"
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
    <div v-else class="absolute inset-0 flex items-center justify-center" style="background: var(--bg-surface);">
      <span class="text-8xl opacity-10">🗞️</span>
    </div>
    <div class="hero-card-overlay"></div>
    <div class="hero-card-body">
      <!-- Category badge -->
      <span
        class="inline-block text-[10px] font-black uppercase tracking-widest px-2.5 py-1 rounded-md mb-3"
        :style="`background: ${catBg}; color: ${catColor};`"
      >{{ article.category || 'Geral' }}</span>
      <!-- Title -->
      <h2 class="font-editorial text-2xl md:text-3xl font-bold text-white leading-tight mb-2 group-hover:text-rose-100 transition-colors duration-200">
        {{ article.title }}
      </h2>
      <!-- Date -->
      <p class="font-mono-jp text-xs" style="color: rgba(255,255,255,0.45);">
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
    <div class="w-32 flex-shrink-0 overflow-hidden">
      <img
        v-if="article.image_url"
        :src="article.image_url"
        :alt="article.title"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        loading="lazy"
        decoding="async"
      />
      <div v-else class="w-full h-full flex items-center justify-center" style="background: var(--bg-surface);">
        <span class="text-3xl opacity-15">🗞️</span>
      </div>
    </div>
    <div class="flex flex-col p-4 gap-1.5 flex-1">
      <span
        class="self-start text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded"
        :style="`background: ${catBg}; color: ${catColor};`"
      >{{ article.category || 'Geral' }}</span>
      <h3 class="text-sm font-bold text-white leading-snug line-clamp-3 group-hover:text-rose-300 transition-colors">
        {{ article.title }}
      </h3>
      <p class="font-mono-jp text-[10px] mt-auto" style="color: var(--text-muted);">
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
    <div v-if="article.image_url && variant !== 'compact'" class="h-44 overflow-hidden">
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
          class="text-[10px] font-black uppercase tracking-widest px-2 py-0.5 rounded"
          :style="`background: ${catBg}; color: ${catColor};`"
        >{{ article.category || 'Geral' }}</span>
        <span class="font-mono-jp text-[10px]" style="color: var(--text-muted);">
          {{ formatDate(article.created_at) }}
        </span>
      </div>
      <h3
        :class="[
          variant === 'compact' ? 'text-sm' : 'text-base',
          'font-bold text-white leading-snug group-hover:text-rose-300 transition-colors line-clamp-2'
        ]"
      >{{ article.title }}</h3>
      <p v-if="variant !== 'compact'" class="text-xs line-clamp-2" style="color: var(--text-secondary);">
        {{ getSnippet(article.content) }}
      </p>
    </div>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  article: { type: Object, required: true },
  variant: { type: String, default: 'default' },
})

// Routing: internal article vs external link (RSS)
const linkTag = computed(() => (props.article?.external ? 'a' : 'router-link'))
const linkProps = computed(() =>
  props.article?.external
    ? { href: props.article.link, target: '_blank', rel: 'noopener noreferrer' }
    : { to: `/news/${props.article?.id}` }
)

// Category colors
const CAT_COLORS = {
  'Política':       { color: 'var(--cat-politica)',      bg: 'var(--cat-politica-bg)' },
  'Economia':       { color: 'var(--cat-economia)',      bg: 'var(--cat-economia-bg)' },
  'Esportes':       { color: 'var(--cat-esportes)',      bg: 'var(--cat-esportes-bg)' },
  'Tecnologia':     { color: 'var(--cat-tecnologia)',    bg: 'var(--cat-tecnologia-bg)' },
  'Mundo':          { color: 'var(--cat-mundo)',         bg: 'var(--cat-mundo-bg)' },
  'Entretenimento': { color: 'var(--cat-entretenimento)',bg: 'var(--cat-entretenimento-bg)' },
  'Geral':          { color: 'var(--cat-geral)',         bg: 'var(--cat-geral-bg)' },
}
const catColor = computed(() => CAT_COLORS[props.article?.category]?.color || 'var(--cat-geral)')
const catBg    = computed(() => CAT_COLORS[props.article?.category]?.bg    || 'var(--cat-geral-bg)')

const formatDate = (d) => {
  if (!d) return ''
  try {
    return new Date(d).toLocaleDateString('pt-BR', {
      day: '2-digit', month: 'short', year: 'numeric',
    })
  } catch { return '' }
}

const getSnippet = (text) => {
  if (!text) return ''
  return text.replace(/<[^>]*>?/gm, '').substring(0, 130)
}
</script>
