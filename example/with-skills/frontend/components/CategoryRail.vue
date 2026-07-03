<script setup lang="ts">
import type { ProductCategory } from '~/types/product'

defineProps<{
  categories: ProductCategory[]
  activeCategory: ProductCategory['value']
}>()

defineEmits<{
  selectCategory: [category: ProductCategory['value']]
}>()
</script>

<template>
  <section id="categories" class="threadline-panel p-5 sm:p-6" aria-labelledby="categories-title">
    <div class="grid gap-4 border-b border-white/15 pb-5 sm:grid-cols-[0.8fr_1.2fr] sm:items-end">
      <h2 id="categories-title" class="text-2xl font-black tracking-[-0.05em] text-threadline-fog sm:text-3xl">Shop by edit</h2>
      <p class="max-w-xl text-sm leading-6 text-zinc-200 sm:justify-self-end sm:text-right">A sharper path through the drop: full edit, statement layers, relaxed tailoring, and finishing objects.</p>
    </div>

    <div class="mt-5 grid gap-2 sm:grid-cols-2 lg:grid-cols-5">
      <button
        v-for="category in categories"
        :key="category.value"
        class="threadline-fade-up threadline-hover-lift group min-h-32 cursor-pointer border p-4 text-left focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-threadline-blue sm:min-h-36"
        :class="category.value === activeCategory ? 'border-threadline-blue bg-threadline-fog text-zinc-950 shadow-threadline-glow' : 'border-white/15 bg-white/[0.045] text-threadline-fog hover:border-threadline-blue/70 hover:bg-white/[0.08]'"
        type="button"
        :aria-pressed="category.value === activeCategory"
        @click="$emit('selectCategory', category.value)"
      >
        <span class="flex items-center justify-between gap-3 text-[11px] font-bold uppercase tracking-[0.22em]" :class="category.value === activeCategory ? 'text-zinc-600' : 'text-threadline-blue'">
          Edit
          <span v-if="category.value === activeCategory" class="text-zinc-950">Selected</span>
        </span>
        <span class="mt-7 block text-xl font-black tracking-[-0.04em]">{{ category.label }}</span>
        <small class="mt-2 block text-sm leading-5" :class="category.value === activeCategory ? 'text-zinc-700' : 'text-zinc-200'">{{ category.description }}</small>
      </button>
    </div>
  </section>
</template>
