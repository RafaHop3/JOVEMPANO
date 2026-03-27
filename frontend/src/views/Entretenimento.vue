<template>
  <div>
    <div class="mb-10">
      <div class="flex items-center gap-3 mb-2">
        <span class="w-10 h-10 bg-pink-500 rounded-lg flex items-center justify-center text-white text-xl">🎬</span>
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">Entretenimento</h1>
      </div>
      <p class="text-slate-500 text-lg">Cinema, música, séries e cultura pop — o melhor do entretenimento.</p>
      <div class="h-px bg-gradient-to-r from-pink-500 via-pink-200 to-transparent mt-4"></div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <article v-for="(item, i) in articles" :key="i" class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-all group">
        <div class="h-44 overflow-hidden bg-gradient-to-br from-pink-100 to-rose-50 flex items-center justify-center">
          <span class="text-6xl">{{ item.emoji }}</span>
        </div>
        <div class="p-5">
          <span class="text-xs font-bold text-pink-600 uppercase tracking-wider">{{ item.tag }}</span>
          <h3 class="text-lg font-bold text-slate-900 mt-1 mb-2 leading-snug">{{ item.title }}</h3>
          <p class="text-slate-500 text-sm leading-relaxed line-clamp-3">{{ item.summary }}</p>
          <p class="text-xs text-slate-400 mt-3 font-mono">{{ item.date }}</p>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
const articles = [
  { tag: 'Cinema', emoji: '🎥', title: 'Filme brasileiro leva Palma de Ouro em Cannes pela primeira vez', summary: 'O longa "Maré Alta", dirigido por Clara Santos, conquistou o prêmio máximo do festival francês com história ambientada nas comunidades ribeirinhas do Amazons.', date: '27 Mar 2026 · 20:00' },
  { tag: 'Música', emoji: '🎵', title: 'Anitta anuncia turnê mundial com 60 datas em 5 continentes', summary: 'A cantora brasileira revelou os detalhes da "Baile Funk World Tour", que passará por estádios na Europa, Ásia e América do Norte a partir de setembro.', date: '27 Mar 2026 · 14:30' },
  { tag: 'Séries', emoji: '📺', title: 'Nova série da Netflix baseada em Machado de Assis bate recorde de audiência', summary: '"Dom Casmurro" estreou no topo do ranking global da plataforma com 45 milhões de visualizações na primeira semana, tornando-se a série em português mais assistida.', date: '26 Mar 2026 · 10:00' },
  { tag: 'Games', emoji: '🎮', title: 'Estúdio indie de Recife ganha prêmio de melhor jogo no The Game Awards', summary: 'O puzzle-adventure "Cordel Digital", da Manguebit Studios, emocionou o público e o júri com sua narrativa baseada no folclore nordestino e estética de xilogravura.', date: '25 Mar 2026 · 22:00' },
]
</script>
