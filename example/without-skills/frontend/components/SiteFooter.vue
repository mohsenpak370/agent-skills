<template>
  <footer class="border-t border-amber-100/80 bg-[#fffaf1]/75">
    <div class="mx-auto grid max-w-7xl gap-8 px-4 py-10 sm:px-6 md:grid-cols-[1fr_auto] md:items-start lg:px-8">
      <div>
        <NuxtLink to="/" class="text-2xl font-extrabold tracking-[-0.06em] text-stone-950">
          Moda
        </NuxtLink>
        <p class="mt-3 max-w-xl text-sm leading-6 text-stone-600">
          Everyday clothing for women, men, and kids. Simple fits, calm colors, easy shopping.
        </p>
      </div>

      <div class="flex flex-wrap gap-2">
        <NuxtLink to="/products" class="rounded-full px-3 py-2 text-sm font-semibold text-stone-600 transition hover:bg-white hover:text-stone-950">All Products</NuxtLink>
        <NuxtLink to="/products?category=women" class="rounded-full px-3 py-2 text-sm font-semibold text-stone-600 transition hover:bg-white hover:text-stone-950">Women</NuxtLink>
        <NuxtLink to="/products?category=men" class="rounded-full px-3 py-2 text-sm font-semibold text-stone-600 transition hover:bg-white hover:text-stone-950">Men</NuxtLink>
        <NuxtLink to="/products?category=kids" class="rounded-full px-3 py-2 text-sm font-semibold text-stone-600 transition hover:bg-white hover:text-stone-950">Kids</NuxtLink>
      </div>
    </div>
  </footer>
</template>
