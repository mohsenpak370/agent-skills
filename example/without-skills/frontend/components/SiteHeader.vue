<script setup lang="ts">
withDefaults(
  defineProps<{
    cartCount?: number
  }>(),
  {
    cartCount: 0
  }
)

const links = [
  { label: 'Shop', to: '/products' },
  { label: 'Women', to: '/products?category=women' },
  { label: 'Men', to: '/products?category=men' },
  { label: 'Kids', to: '/products?category=kids' }
]
</script>

<template>
  <header class="sticky top-0 z-30 border-b border-stone-200/70 bg-[#fffaf4]/85 backdrop-blur-xl">
    <div class="mx-auto flex h-18 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
      <NuxtLink to="/" class="group flex items-center gap-3 text-stone-950">
        <span class="grid h-10 w-10 place-items-center rounded-full bg-stone-950 text-sm font-black text-amber-200 shadow-lg shadow-stone-900/15">M</span>
        <span class="text-2xl font-extrabold tracking-[-0.06em]">Moda</span>
      </NuxtLink>

      <nav class="hidden items-center gap-1 rounded-full border border-white/80 bg-white/70 p-1 shadow-sm shadow-stone-900/5 md:flex" aria-label="Main navigation">
        <NuxtLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="rounded-full px-4 py-2 text-sm font-semibold text-stone-600 transition hover:bg-amber-100/80 hover:text-stone-950"
        >
          {{ link.label }}
        </NuxtLink>
      </nav>

      <NuxtLink to="/products" class="inline-flex items-center gap-2 rounded-full bg-stone-950 px-4 py-2.5 text-sm font-bold text-white shadow-lg shadow-stone-900/15 transition hover:-translate-y-0.5 hover:bg-stone-800">
        <span>Cart</span>
        <span class="grid min-h-6 min-w-6 place-items-center rounded-full bg-amber-300 px-2 text-xs font-black text-stone-950">
          {{ cartCount }}
        </span>
      </NuxtLink>
    </div>
  </header>
</template>
