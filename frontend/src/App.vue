<template>
  <!-- Main Wrapper -->
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 transition-colors duration-300">
    <header class="border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <!-- Brand -->
        <router-link to="/" class="hover:opacity-80 transition-opacity">
          <h1 class="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Jovem<span class="text-rose-600">Pano</span>
          </h1>
        </router-link>
        
        <!-- Navigation & Toggles -->
        <nav class="flex items-center gap-6">
          <router-link to="/" class="text-sm font-semibold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors uppercase tracking-wider">Feed</router-link>
          
          <!-- Secreto: Não tem mais link explícito para '/admin'. Autores devem digitar na URl por segurança básica (KISS) -->
          
          <!-- Dark Mode Toggle -->
          <button @click="toggleDarkMode" class="p-2 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-rose-500 transition-colors" title="Alternar Tema">
            <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path></svg>
          </button>
        </nav>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-10">
      <router-view></router-view>
    </main>

    <CookieBanner />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CookieBanner from './components/CookieBanner.vue'

const isDark = ref(true)

onMounted(() => {
  // Puxa a preferência do sistema se estiver vazia
  if (localStorage.theme === 'light') {
    isDark.value = false
    document.documentElement.classList.remove('dark')
  } else {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})

const toggleDarkMode = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.theme = 'dark'
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.theme = 'light'
  }
}
</script>
