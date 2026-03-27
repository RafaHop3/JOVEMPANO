<template>
  <div v-if="!accepted" class="fixed bottom-0 left-0 w-full bg-white border-t border-slate-200 p-4 shadow-[0_-10px_30px_rgba(0,0,0,0.08)] z-50">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 px-4">
      <p class="text-slate-600 text-sm">
        Nós utilizamos cookies para otimizar a sua experiência e personalizar anúncios. Ao continuar navegando, você concorda com a nossa política legal de dados.
      </p>
      <button @click="acceptCookies" class="whitespace-nowrap bg-rose-600 hover:bg-rose-500 text-white px-8 py-2.5 rounded-lg font-bold transition-all hover:scale-105">
        Aceitar e Fechar
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const accepted = ref(true)

onMounted(() => {
  if (!localStorage.getItem('cookies_accepted')) {
    accepted.value = false
  }
})

const acceptCookies = () => {
  localStorage.setItem('cookies_accepted', 'true')
  accepted.value = true
}
</script>
