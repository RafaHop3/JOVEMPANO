<template>
  <div
    v-if="headlines.length > 0"
    class="overflow-hidden"
    style="background: var(--brand); position: relative;"
  >
    <div class="max-w-7xl mx-auto px-4 flex items-center" style="height: 38px;">
      <!-- Static label -->
      <div
        class="flex items-center gap-2 flex-shrink-0 pr-4"
        style="border-right: 1px solid rgba(255,255,255,0.25);"
      >
        <span
          class="pulse-live w-2 h-2 rounded-full flex-shrink-0"
          style="background: white; display: inline-block;"
        ></span>
        <span class="text-white font-black text-[11px] uppercase tracking-widest select-none">
          Urgente
        </span>
      </div>

      <!-- Scrolling ticker -->
      <div class="overflow-hidden flex-1 ml-4" style="mask-image: linear-gradient(to right, transparent 0%, black 3%, black 97%, transparent 100%);">
        <div class="ticker-track" aria-live="polite">
          <span
            v-for="(headline, i) in loopedHeadlines"
            :key="i"
            class="text-white text-xs font-medium flex-shrink-0"
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
