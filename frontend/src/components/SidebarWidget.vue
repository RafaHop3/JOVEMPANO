<template>
  <aside class="w-full sticky top-24">
    <!-- Ad space or Monetization -->
    <div class="bg-gradient-to-br from-rose-900/20 to-slate-100 dark:from-rose-900/40 dark:to-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 mb-6 text-center shadow-lg">
      <span class="text-xs text-slate-400 dark:text-slate-500 uppercase tracking-widest font-bold mb-2 block">Publicidade</span>
      <div class="w-full h-64 bg-slate-200/50 dark:bg-slate-800/50 rounded flex items-center justify-center border border-dashed border-slate-300 dark:border-slate-700">
        <p class="text-slate-500 font-medium">Espaço Premium</p>
      </div>
    </div>
    
    <!-- Top Read / Trending -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm dark:shadow-xl">
      <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
        <span class="w-1.5 h-4 bg-rose-600 rounded"></span> Em Alta
      </h4>
      <ul class="flex flex-col gap-4">
        <li class="border-b border-light-200 dark:border-slate-800 pb-3 last:border-0 last:pb-0">
          <a href="#" class="text-slate-700 dark:text-slate-300 hover:text-rose-500 transition-colors text-sm font-medium line-clamp-2">Governo vota novo arcabouço fiscal que impactará importações este ano.</a>
        </li>
        <li class="border-b border-light-200 dark:border-slate-800 pb-3 last:border-0 last:pb-0">
          <a href="#" class="text-slate-700 dark:text-slate-300 hover:text-rose-500 transition-colors text-sm font-medium line-clamp-2">Tecnologia: Vue 3 se consolida como escolha número 1 em SPAs de portais.</a>
        </li>
      </ul>
    </div>
  </aside>
</template>
