<template>
  <div
    v-if="headlines.length > 0"
    class="overflow-hidden rounded-2xl aero-shine-sweep"
    style="
      background: linear-gradient(90deg,
        rgba(200,235,255,0.85) 0%,
        rgba(255,255,255,0.80) 50%,
        rgba(210,240,255,0.85) 100%
      );
      border: 1px solid rgba(255,255,255,0.70);
      backdrop-filter: blur(12px) saturate(160%);
      -webkit-backdrop-filter: blur(12px) saturate(160%);
      box-shadow: 0 2px 0 rgba(255,255,255,0.9) inset, 0 4px 16px rgba(30,100,200,0.10);
      position: relative;
    "
  >
    <div class="max-w-7xl mx-auto px-4 flex items-center" style="height: 44px;">
      <!-- Static label -->
      <div
        class="flex items-center justify-center gap-2 flex-shrink-0 pr-4 h-full"
        style="border-right: 1px solid rgba(30,144,255,0.20);"
      >
        <span
          class="pulse-live w-2 h-2 rounded-full flex-shrink-0"
          style="background: var(--brand); display: inline-block;"
        ></span>
        <span
          class="font-extrabold text-[11px] uppercase tracking-widest select-none pt-0.5"
          style="color: var(--brand);"
        >Urgente</span>
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
            class="text-sm font-semibold flex-shrink-0 flex items-center h-full pt-0.5"
            style="color: var(--text-secondary);"
          >
            {{ headline }}
            <span style="color: var(--brand-light); margin: 0 1.5rem; opacity: 0.6;">◆</span>
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
