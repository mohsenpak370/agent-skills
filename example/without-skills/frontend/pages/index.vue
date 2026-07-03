<script setup lang="ts">
type Category = {
  value: string
  label: string
  count: number
}

type Product = {
  id: number
  name: string
  description: string
  category: string
  brand: string
  size: string
  color: string
  price: string
  image_url: string
  featured: boolean
}

const config = useRuntimeConfig()

const { data: categoryData } = await useFetch<{ categories: Category[] }>(
  `${config.public.apiBase}/categories/`,
  { default: () => ({ categories: [] }) }
)

const { data: featuredData } = await useFetch<{ products: Product[] }>(
  `${config.public.apiBase}/products/`,
  {
    query: { featured: 'true', sort: 'newest' },
    default: () => ({ products: [] })
  }
)

const categories = computed(() => categoryData.value?.categories ?? [])
const featuredProducts = computed(() => featuredData.value?.products.slice(0, 4) ?? [])
</script>

<template>
  <div class="min-h-screen text-stone-950">
    <SiteHeader />

    <main>
      <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8 lg:py-16">
        <section class="grid items-center gap-10 lg:grid-cols-[1.05fr_0.85fr]">
          <div>
            <p class="mb-5 inline-flex rounded-full border border-amber-200 bg-amber-100/70 px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-amber-800">
              New Season Essentials
            </p>
            <h1 class="display-title max-w-4xl text-5xl font-extrabold text-stone-950 sm:text-7xl lg:text-8xl">
              Clothes for every day, every age, every plan.
            </h1>
            <p class="mt-6 max-w-2xl text-lg leading-8 text-stone-600">
              Discover calm, wearable pieces for women, men, and kids. Curated outfits, useful basics,
              and easy add-to-cart shopping from one simple store.
            </p>
            <div class="mt-8 flex flex-wrap gap-3">
              <NuxtLink to="/products" class="rounded-full bg-stone-950 px-6 py-3.5 text-sm font-bold text-white shadow-xl shadow-stone-900/15 transition hover:-translate-y-0.5 hover:bg-stone-800">
                Shop collection
              </NuxtLink>
              <NuxtLink to="/products?category=kids" class="rounded-full border border-stone-300 bg-white/55 px-6 py-3.5 text-sm font-bold text-stone-800 transition hover:-translate-y-0.5 hover:bg-white">
                Explore kids
              </NuxtLink>
            </div>
          </div>

          <div class="relative overflow-hidden rounded-[2rem] border border-white/80 shadow-2xl shadow-stone-900/12">
            <img
              src="https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1000&q=80"
              alt="Fashion store clothing racks"
              class="h-[420px] w-full object-cover lg:h-[620px]"
            >
            <div class="surface-card absolute bottom-4 left-4 max-w-56 rounded-3xl p-5">
              <p class="font-extrabold text-stone-950">Fresh drops</p>
              <p class="text-sm text-stone-600">Men, women, kids</p>
            </div>
          </div>
        </section>

        <section class="mt-16">
          <div class="mb-6">
            <p class="mb-3 inline-flex rounded-full bg-amber-100 px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-amber-800">
              Shop by Category
            </p>
            <h2 class="display-title text-3xl font-extrabold text-stone-950 sm:text-5xl">
              Find the right fit faster.
            </h2>
          </div>

          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <NuxtLink
              v-for="category in categories"
              :key="category.value"
              :to="`/products?category=${category.value}`"
              class="group block transition hover:-translate-y-1"
            >
              <div class="overflow-hidden rounded-[1.75rem] bg-stone-950 p-6 text-white shadow-lg shadow-stone-900/10 group-hover:shadow-xl">
                <div class="relative min-h-28">
                  <div class="absolute right-0 top-0 h-16 w-16 rounded-full bg-amber-300/90 transition group-hover:scale-110" />
                  <div class="absolute bottom-0 left-0">
                    <h3 class="text-3xl font-extrabold tracking-[-0.05em]">{{ category.label }}</h3>
                    <p class="mt-1 text-sm font-bold text-stone-300">{{ category.count }} products</p>
                  </div>
                </div>
              </div>
            </NuxtLink>
          </div>
        </section>

        <section class="warm-panel mt-10 rounded-[2rem] p-6 sm:p-8">
          <div class="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div>
              <p class="mb-3 inline-flex rounded-full bg-white/70 px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-stone-700">
                Easy Styling
              </p>
              <h2 class="display-title max-w-4xl text-3xl font-extrabold text-stone-950 sm:text-5xl">
                Build outfits from polished basics and playful layers.
              </h2>
            </div>
            <NuxtLink to="/products?sort=price_asc" class="w-fit rounded-full bg-stone-950 px-5 py-3 text-sm font-bold text-white transition hover:-translate-y-0.5 hover:bg-stone-800">
              Shop best value
            </NuxtLink>
          </div>
        </section>

        <section class="mt-16">
          <div class="mb-6">
            <p class="mb-3 inline-flex rounded-full bg-amber-100 px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-amber-800">
              Featured
            </p>
            <h2 class="display-title text-3xl font-extrabold text-stone-950 sm:text-5xl">
              Popular pieces this week.
            </h2>
          </div>

          <div class="grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
            <NuxtLink
              v-for="product in featuredProducts"
              :key="product.id"
              :to="`/products/${product.id}`"
              class="block transition hover:-translate-y-1"
            >
              <article class="product-card overflow-hidden rounded-[1.75rem] transition">
                <img v-if="product.image_url" :src="product.image_url" :alt="product.name" class="h-64 w-full object-cover">
                <div class="p-5">
                  <p class="text-xs font-bold uppercase tracking-[0.16em] text-stone-500">{{ product.brand }} / {{ product.category }}</p>
                  <h3 class="mt-2 text-xl font-extrabold tracking-[-0.04em] text-stone-950">{{ product.name }}</h3>
                  <p class="mt-2 line-clamp-2 text-sm leading-6 text-stone-600">{{ product.description }}</p>
                  <div class="mt-5 flex items-center justify-between gap-3">
                    <p class="text-lg font-extrabold">${{ product.price }}</p>
                    <span class="text-sm font-bold text-stone-700">
                      View details
                    </span>
                  </div>
                </div>
              </article>
            </NuxtLink>
          </div>
        </section>
      </div>
    </main>

    <SiteFooter />
  </div>
</template>
