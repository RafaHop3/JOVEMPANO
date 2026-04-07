<template>
  <div class="min-h-screen bg-white relative transition-colors duration-300">
    <!-- ═══════ HEADER ═══════ -->
    <header class="border-b border-slate-200 bg-white/95 backdrop-blur sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <!-- Brand with Logo -->
        <router-link to="/" class="flex items-center gap-3 hover:opacity-90 transition-opacity">
          <img src="/images/logo.png" alt="JovemPano" class="w-10 h-10 object-contain" />
          <h1 class="text-2xl font-extrabold tracking-tight">
            <span class="text-blue-600">Jovem</span><span class="text-amber-500">Pano</span>
          </h1>
        </router-link>
        <span class="text-xs text-slate-400 hidden md:block font-mono">{{ formattedDate }}</span>
      </div>
    </header>

    <!-- ═══════ NAVIGATION BAR ═══════ -->
    <nav class="bg-white/90 backdrop-blur border-b border-slate-200 shadow-sm sticky top-[57px] z-40">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex items-center gap-1 overflow-x-auto scrollbar-hide py-1">
          <router-link 
            v-for="btn in navButtons" 
            :key="btn.path" 
            :to="btn.path"
            :class="[
              'nav-btn flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-semibold transition-all whitespace-nowrap border',
              isActive(btn.path) 
                ? `${btn.activeBg} ${btn.activeText} border-current shadow-sm` 
                : 'text-slate-600 hover:text-slate-900 border-transparent hover:bg-slate-50 hover:border-slate-200'
            ]"
          >
            {{ btn.label }}
          </router-link>
        </div>
      </div>
    </nav>

    <!-- ═══════ MAIN CONTENT ═══════ -->
    <main class="max-w-7xl mx-auto px-4 py-10 relative z-10">
      <router-view></router-view>
    </main>
    
    <!-- PHASE 2 NOTIFICATION -->
    <div v-if="debug" class="fixed bottom-4 right-4 bg-emerald-500 text-white p-4 rounded-xl shadow-xl z-50">
      Phase 2: Restoration Complete
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const debug = ref(true)

const navButtons = [
  { path: '/',               label: 'Início',         activeBg: 'bg-blue-50',     activeText: 'text-blue-700' },
  { path: '/politica',       label: 'Política',       activeBg: 'bg-rose-50',     activeText: 'text-rose-700' },
  { path: '/economia',       label: 'Economia',       activeBg: 'bg-amber-50',    activeText: 'text-amber-700' },
  { path: '/esportes',       label: 'Esportes',       activeBg: 'bg-emerald-50',  activeText: 'text-emerald-700' },
]

const isActive = (path) => {
  if (!route || !route.path) return false
  return route.path === path
}

const formattedDate = computed(() => {
  return new Date().toLocaleDateString('pt-BR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
})
</script>
