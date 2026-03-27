<template>
  <!-- Active Banners Carousel -->
  <section v-if="banners.length > 0" class="relative overflow-hidden rounded-2xl shadow-2xl mb-10 group" style="min-height: 380px;">
    <!-- Slides -->
    <div 
      class="flex transition-transform duration-700 ease-in-out h-full"
      :style="{ transform: `translateX(-${current * 100}%)` }"
    >
      <div 
        v-for="banner in banners" 
        :key="banner.id"
        class="relative w-full flex-shrink-0"
        style="min-height: 380px;"
      >
        <!-- Background Image -->
        <img 
          :src="banner.image_url" 
          :alt="banner.title"
          class="w-full h-full object-cover absolute inset-0"
          style="min-height: 380px;"
        />
        <!-- Overlay -->
        <div class="absolute inset-0 bg-gradient-to-r from-black/80 via-black/50 to-transparent"></div>
        
        <!-- Content Balloon -->
        <div class="absolute inset-0 flex items-end p-8 lg:p-12">
          <div class="max-w-2xl">
            <!-- Live Badge -->
            <div class="flex items-center gap-2 mb-4">
              <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
              <span class="text-xs font-bold tracking-widest text-rose-400 uppercase">Destaque</span>
            </div>
            <!-- Title Balloon -->
            <div class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-xl">
              <h2 class="text-2xl lg:text-4xl font-extrabold text-white leading-tight mb-3 drop-shadow-lg">
                {{ banner.title }}
              </h2>
              <p v-if="banner.subtitle" class="text-slate-200 text-base lg:text-lg leading-relaxed mb-4">
                {{ banner.subtitle }}
              </p>
              <a 
                v-if="banner.link_url" 
                :href="banner.link_url"
                class="inline-flex items-center gap-2 bg-rose-600 hover:bg-rose-500 text-white font-bold py-2 px-6 rounded-full transition-all hover:shadow-rose-500/40 hover:shadow-lg text-sm"
              >
                Ver Matéria Completa <span>→</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation Dots -->
    <div v-if="banners.length > 1" class="absolute bottom-4 right-6 flex gap-2">
      <button 
        v-for="(b, i) in banners" 
        :key="i"
        @click="current = i"
        :class="['w-2 h-2 rounded-full transition-all', i === current ? 'bg-white w-6' : 'bg-white/40 hover:bg-white/70']"
      ></button>
    </div>

    <!-- Arrow Navigation -->
    <button v-if="banners.length > 1" @click="prev" class="absolute left-4 top-1/2 -translate-y-1/2 bg-black/30 hover:bg-black/60 text-white rounded-full w-10 h-10 flex items-center justify-center backdrop-blur transition-all opacity-0 group-hover:opacity-100">‹</button>
    <button v-if="banners.length > 1" @click="next" class="absolute right-4 top-1/2 -translate-y-1/2 bg-black/30 hover:bg-black/60 text-white rounded-full w-10 h-10 flex items-center justify-center backdrop-blur transition-all opacity-0 group-hover:opacity-100">›</button>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const banners = ref([])
const current = ref(0)
let autoplay = null

const next = () => { current.value = (current.value + 1) % banners.value.length }
const prev = () => { current.value = (current.value - 1 + banners.value.length) % banners.value.length }

const startAutoplay = () => {
  autoplay = setInterval(() => {
    if (banners.value.length > 1) next()
  }, 5000)
}

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/banners/active')
    if (res.ok) banners.value = await res.json()
  } catch(e) {
    console.error('Banners fetch failed:', e)
  }
  startAutoplay()
})

onBeforeUnmount(() => clearInterval(autoplay))
</script>
