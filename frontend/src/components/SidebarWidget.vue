<template>
  <aside class="w-full sticky top-24">
    <!-- Ad space or Monetization -->
    <div class="bg-gradient-to-br from-amber-50 to-slate-50 border border-slate-200 rounded-xl p-6 mb-6 text-center shadow-sm">
      <span class="text-xs text-slate-400 uppercase tracking-widest font-bold mb-2 block">Publicidade</span>
      <div class="w-full h-64 bg-slate-100 rounded flex items-center justify-center border border-dashed border-slate-300">
        <p class="text-slate-400 font-medium">Espaço Premium</p>
      </div>
    </div>
    
    <!-- Top Read / Trending -->
    <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
      <h4 class="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
        <span class="w-1.5 h-4 bg-amber-500 rounded"></span> Em Alta
      </h4>
      <ul class="flex flex-col gap-4">
        <li class="border-b border-slate-100 pb-3 last:border-0 last:pb-0">
          <a href="#" class="text-slate-600 hover:text-blue-600 transition-colors text-sm font-medium line-clamp-2">Governo vota novo arcabouço fiscal que impactará importações este ano.</a>
        </li>
        <li class="border-b border-slate-100 pb-3 last:border-0 last:pb-0">
          <a href="#" class="text-slate-600 hover:text-blue-600 transition-colors text-sm font-medium line-clamp-2">Tecnologia: Vue 3 se consolida como escolha número 1 em SPAs de portais.</a>
        </li>
      </ul>
    </div>
  </aside>
</template>
