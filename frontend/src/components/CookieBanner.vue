<template>
  <Transition name="slide-up">
    <div
      v-if="!accepted"
      class="fixed bottom-0 left-0 w-full bg-[#050811]/95 border-t border-cyan-500/30 p-4 shadow-2xl backdrop-blur-xl z-50 text-slate-200"
    >
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 px-4">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-cyan-950 border border-cyan-500/40 flex items-center justify-center text-neon-cyan flex-shrink-0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
          </div>
          <p class="text-xs sm:text-sm text-slate-300 leading-relaxed font-sans">
            A Orbe Systems utiliza armazenamento estritamente necessário e telemetria anônima para métricas de desempenho em conformidade com a <strong class="text-neon-cyan">LGPD (Lei nº 13.709/2018, Art. 8º)</strong>.
          </p>
        </div>

        <div class="flex items-center gap-3 flex-shrink-0 w-full md:w-auto justify-end">
          <button
            @click="acceptEssential"
            class="px-4 py-2 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white border border-slate-700 hover:border-slate-500 bg-slate-900/60 transition-all"
          >
            Apenas Essenciais
          </button>
          <button
            @click="acceptAll"
            class="whitespace-nowrap px-5 py-2 rounded-lg text-xs font-mono font-bold text-black bg-neon-cyan hover:brightness-110 shadow-neon-cyan transition-all"
          >
            Aceitar Todos
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const accepted = ref(true)

onMounted(() => {
  if (!localStorage.getItem('cookies_accepted')) {
    setTimeout(() => {
      accepted.value = false
    }, 400)
  }
})

const acceptEssential = () => {
  localStorage.setItem('cookies_accepted', 'essential')
  accepted.value = true
}

const acceptAll = () => {
  localStorage.setItem('cookies_accepted', 'all')
  accepted.value = true
}
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(100%);
}
</style>
