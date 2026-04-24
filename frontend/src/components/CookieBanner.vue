<template>
  <Transition name="slide-up">
    <div v-if="!accepted" class="fixed bottom-0 left-0 w-full bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 p-4 shadow-[0_-10px_30px_rgba(0,0,0,0.1)] dark:shadow-[0_-10px_30px_rgba(0,0,0,0.5)] z-50">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 px-4">
        <p class="text-slate-600 dark:text-slate-300 text-sm">
          Nós utilizamos cookies para otimizar a sua experiência e personalizar anúncios. Ao continuar navegando, você concorda com a nossa política legal de dados.
        </p>
        <button @click="acceptCookies" class="whitespace-nowrap bg-rose-600 hover:bg-rose-500 text-white px-8 py-2.5 rounded-lg font-bold transition-all hover:scale-105">
          Aceitar e Fechar
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const accepted = ref(true)

onMounted(() => {
  if (!localStorage.getItem('cookies_accepted')) {
    // Slight delay to allow transition to run on initial load
    setTimeout(() => {
      accepted.value = false
    }, 500)
  }
})

const acceptCookies = () => {
  localStorage.setItem('cookies_accepted', 'true')
  accepted.value = true
}
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(100%);
}
</style>
