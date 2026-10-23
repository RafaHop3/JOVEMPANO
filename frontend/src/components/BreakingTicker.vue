<template>
  <div
    v-if="headlines.length > 0"
    class="overflow-hidden rounded-xl border border-cyan-500/25 bg-[#050811]/90 shadow-md relative"
  >
    <div class="max-w-7xl mx-auto px-4 flex items-center" style="height: 44px;">
      <!-- Static label -->
      <div
        class="flex items-center justify-center gap-2 flex-shrink-0 pr-4 h-full border-r border-cyan-500/20"
      >
        <span
          class="pulse-live w-2 h-2 rounded-full flex-shrink-0 bg-neon-cyan inline-block"
        ></span>
        <span
          class="font-mono font-extrabold text-[11px] uppercase tracking-widest text-neon-cyan select-none"
        >RADAR URGENTE</span>
      </div>

      <!-- Scrolling ticker -->
      <div
        class="overflow-hidden flex-1 ml-4 h-full flex items-center"
        style="mask-image: linear-gradient(to right, transparent 0%, black 3%, black 97%, transparent 100%);"
      >
        <div class="ticker-track flex items-center h-full" aria-live="polite">
          <span
            v-for="(headline, i) in loopedHeadlines"
            :key="i"
            class="text-xs sm:text-sm font-medium flex-shrink-0 flex items-center h-full text-slate-200"
          >
            {{ headline }}
            <span class="text-neon-cyan mx-6 opacity-75 font-mono">◆</span>
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
