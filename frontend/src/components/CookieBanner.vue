<template>
  <Transition name="slide-up">
    <div v-if="!accepted" class="fixed bottom-0 left-0 w-full bg-white/95 border-t border-slate-200 p-4 shadow-[0_-8px_32px_rgba(15,23,42,0.08)] backdrop-blur-md z-50">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 px-4">
        <p class="text-slate-600 text-sm">
          Nós utilizamos cookies para otimizar a sua experiência. Ao continuar navegando, você concorda com a nossa política de dados.
        </p>
        <button @click="acceptCookies" class="whitespace-nowrap bg-sky-600 hover:bg-sky-500 text-white px-8 py-2.5 rounded-full font-bold text-sm shadow-sm transition-transform hover:scale-[1.02]">
          Aceitar e fechar
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
