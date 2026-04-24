<template>
  <div
    v-if="headlines.length > 0"
    class="overflow-hidden"
    style="background: var(--brand); position: relative; border-bottom: 4px solid var(--bg-base);"
  >
    <div class="max-w-7xl mx-auto px-4 flex items-center" style="height: 44px;">
      <!-- Static label -->
      <div
        class="flex items-center justify-center gap-2 flex-shrink-0 pr-4 h-full"
        style="border-right: 1px solid rgba(255,255,255,0.25);"
      >
        <span
          class="pulse-live w-2 h-2 rounded-full flex-shrink-0"
          style="background: white; display: inline-block;"
        ></span>
        <span class="text-white font-black text-[11px] uppercase tracking-widest select-none pt-0.5">
          Urgente
        </span>
      </div>

      <!-- Scrolling ticker -->
      <div class="overflow-hidden flex-1 ml-4 h-full flex items-center" style="mask-image: linear-gradient(to right, transparent 0%, black 3%, black 97%, transparent 100%);">
        <div class="ticker-track flex items-center h-full" aria-live="polite">
          <span
            v-for="(headline, i) in loopedHeadlines"
            :key="i"
            class="text-white text-sm font-bold flex-shrink-0 flex items-center h-full pt-0.5"
          >
            {{ headline }}
            <span style="opacity: 0.35; margin: 0 1.5rem;">●</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  headlines: {
    type: Array,
    default: () => [],
  },
})

// Triple the headlines so the ticker loops seamlessly before restarting
const loopedHeadlines = computed(() => {
  if (props.headlines.length === 0) return []
  return [...props.headlines, ...props.headlines, ...props.headlines]
})
</script>
