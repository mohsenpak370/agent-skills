<script setup lang="ts">
import ProductGrid from '~/components/ProductGrid.vue'
import type { ProductCategory, ProductListResponse, ProductSortOption } from '~/types/product'

const categories: ProductCategory[] = [
  { value: 'all', label: 'All', description: 'The full Atelier wardrobe edit' },
  { value: 'women', label: 'Women', description: 'Tailored drape, knits, and quiet structure' },
  { value: 'men', label: 'Men', description: 'Relaxed shirting, wool layers, clean utility' },
  { value: 'kids', label: 'Kids', description: 'Soft pieces with school-day durability' },
  { value: 'accessories', label: 'Accessories', description: 'Finishing objects with everyday purpose' },
]

const sortOptions: ProductSortOption[] = [
  { value: 'featured', label: 'Featured' },
  { value: 'newest', label: 'Newest' },
  { value: 'priceAsc', label: 'Price: low to high' },
  { value: 'priceDesc', label: 'Price: high to low' },
]

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl.replace(/\/$/, '')
const catalogUrl = `${siteUrl}/products`
const heroImage = 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=1400&q=85'
const catalogDescription = 'Shop Threadline Atelier, a cold-luxury fashion edit of refined wardrobe pieces, quiet tailoring, accessories, and private client service.'
const selectedCategory = shallowRef<ProductCategory['value']>('all')
const selectedSort = shallowRef<ProductSortOption['value']>('featured')
const productQuery = computed(() => ({
  page: 1,
  pageSize: 20,
  category: selectedCategory.value,
  sortBy: selectedSort.value,
}))
const {
  cart,
  cartQuantities,
  pending: cartPending,
  errorMessage: cartErrorMessage,
  loadCart,
  addItem,
  updateItem,
  removeItem,
  clearCart,
} = useCart()

const { data, pending, error } = await useFetch<ProductListResponse>(
  `${config.public.apiBase}/products/`,
  {
    query: productQuery,
    watch: [selectedCategory, selectedSort],
    default: () => ({
      data: [],
      pagination: { page: 1, pageSize: 20, totalItems: 0, totalPages: 0 },
    }),
  },
)

useSeoMeta({
  title: 'Luxury Fashion Edit',
  description: catalogDescription,
  ogTitle: 'Threadline Atelier Luxury Fashion Edit',
  ogDescription: catalogDescription,
  ogImage: heroImage,
  ogUrl: catalogUrl,
  twitterTitle: 'Threadline Atelier Luxury Fashion Edit',
  twitterDescription: catalogDescription,
  twitterImage: heroImage,
})

useHead({
  link: [
    { rel: 'canonical', href: catalogUrl },
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@graph': [
          {
            '@type': 'Organization',
            '@id': `${siteUrl}/#organization`,
            name: 'Threadline Atelier',
            url: siteUrl,
          },
          {
            '@type': 'WebSite',
            '@id': `${siteUrl}/#website`,
            name: 'Threadline Atelier',
            url: siteUrl,
            publisher: { '@id': `${siteUrl}/#organization` },
          },
          {
            '@type': 'CollectionPage',
            '@id': `${catalogUrl}#collection`,
            name: 'Luxury Fashion Edit',
            description: catalogDescription,
            url: catalogUrl,
            isPartOf: { '@id': `${siteUrl}/#website` },
          },
          {
            '@type': 'BreadcrumbList',
            itemListElement: [
              { '@type': 'ListItem', position: 1, name: 'Home', item: siteUrl },
              { '@type': 'ListItem', position: 2, name: 'Products', item: catalogUrl },
            ],
          },
        ],
      }).replace(/</g, '\\u003c'),
    },
  ],
})

onMounted(() => {
  loadCart()
})
</script>

<template>
  <div class="threadline-shell">
    <StorefrontHeader :item-count="cart.summary.itemCount" />

    <main class="threadline-container pb-24 pt-8 sm:py-10">
      <section class="grid gap-5 lg:grid-cols-[minmax(0,0.88fr)_minmax(380px,1.12fr)]" aria-labelledby="shop-hero-title">
        <div class="threadline-dark-panel flex min-h-[480px] flex-col justify-between p-7 sm:min-h-[560px] sm:p-10 lg:p-12">
          <div class="threadline-fade-up flex items-center justify-between gap-6 text-[11px] font-bold uppercase tracking-[0.24em] text-zinc-300">
            <span>Drop 026</span>
            <span class="hidden text-threadline-blue sm:inline">After-dark edit</span>
          </div>
          <div class="threadline-fade-up threadline-delay-1">
            <h1 id="shop-hero-title" class="threadline-heading-xl max-w-2xl">Luxury with a night pulse.</h1>
            <p class="mt-6 max-w-xl text-lg leading-8 text-zinc-200 sm:text-xl">
              Sharp wardrobe pieces for young customers who want polish without looking overdressed.
            </p>
            <div class="mt-8 flex flex-col gap-3 sm:flex-row">
              <NuxtLink to="#catalog" class="threadline-button-primary threadline-hover-lift h-12">Shop drop</NuxtLink>
              <NuxtLink to="#categories" class="threadline-button-secondary threadline-hover-lift h-12">Explore edits</NuxtLink>
            </div>
          </div>
          <dl class="threadline-fade-up threadline-delay-2 grid gap-4 border-t border-white/15 pt-6 text-sm text-zinc-200 sm:grid-cols-3">
            <div>
              <dt class="threadline-label-muted">Service</dt>
              <dd class="mt-2 font-semibold text-threadline-fog">Private client support</dd>
            </div>
            <div>
              <dt class="threadline-label-muted">Returns</dt>
              <dd class="mt-2 font-semibold text-threadline-fog">30-day complimentary</dd>
            </div>
            <div>
              <dt class="threadline-label-muted">Energy</dt>
              <dd class="mt-2 font-semibold text-threadline-fog">Night-out minimalism</dd>
            </div>
          </dl>
        </div>
        <div class="threadline-fade-up threadline-delay-3 relative min-h-[420px] overflow-hidden border border-white/15 bg-zinc-950 sm:min-h-[560px]" aria-hidden="true">
          <img
            class="threadline-image-drift absolute inset-0 size-full object-cover opacity-90"
            src="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=1400&q=85"
            alt=""
          >
          <div class="absolute inset-0 bg-gradient-to-t from-zinc-950/95 via-zinc-950/35 to-zinc-950/20" />
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_72%_22%,rgba(159,214,255,0.22),transparent_18rem)]" />
          <div class="absolute left-5 top-5 border border-white/30 bg-zinc-950/50 px-4 py-3 text-[11px] font-bold uppercase tracking-[0.22em] text-white backdrop-blur-md">
            Night / Street / Atelier
          </div>
          <div class="absolute bottom-5 right-5 max-w-sm border border-white/25 bg-zinc-950/72 p-5 text-threadline-fog backdrop-blur-md">
            <p class="text-3xl font-black leading-none tracking-[-0.06em]">Low light. High standards.</p>
            <p class="mt-3 text-sm leading-6 text-zinc-200">A wardrobe system for dinners, galleries, late trains, and every entrance that matters.</p>
          </div>
        </div>
      </section>

      <div class="mt-10">
        <CategoryRail
          :categories="categories"
          :active-category="selectedCategory"
          @select-category="selectedCategory = $event"
        />
      </div>

      <div class="mt-10 grid gap-6 lg:grid-cols-[minmax(0,1fr)_380px] lg:items-start">
        <section class="space-y-5">
          <section id="catalog" class="space-y-4">
            <div>
              <h2 class="threadline-heading-md max-w-2xl">The current wardrobe edit</h2>
              <p class="mt-3 max-w-2xl text-base leading-7 text-zinc-200">Filter the collection without losing the boutique rhythm. Each piece is selected for repeat wear, not novelty.</p>
            </div>
            <CatalogControls
              :categories="categories"
              :sort-options="sortOptions"
              :category="selectedCategory"
              :sort-by="selectedSort"
              :total-items="data.pagination.totalItems"
              @update-category="selectedCategory = $event"
              @update-sort="selectedSort = $event"
            />
          </section>

          <div v-if="pending" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3" aria-label="Loading products" aria-live="polite">
            <UCard v-for="index in 6" :key="index" :ui="{ body: 'space-y-4' }">
              <USkeleton class="h-56 w-full" />
              <USkeleton class="h-5 w-2/3" />
              <USkeleton class="h-20 w-full" />
            </UCard>
          </div>

          <UAlert
            v-else-if="error"
            color="error"
            variant="soft"
            icon="i-lucide-alert-circle"
            title="Products could not be loaded"
            description="Check that Django is running."
          />
          <UAlert
            v-else-if="data.data.length === 0"
            color="neutral"
            variant="soft"
            icon="i-lucide-package-open"
            title="No products are available yet"
            description="Try another category or sort option."
          />
          <ProductGrid
            v-else
            :products="data.data"
            :cart-quantities="cartQuantities"
            :is-busy="cartPending"
            @add-to-cart="addItem"
          />
        </section>

        <CartPanel
          id="cart"
          :cart="cart"
          :is-busy="cartPending"
          :error-message="cartErrorMessage"
          @update-quantity="updateItem"
          @remove-item="removeItem"
          @clear-cart="clearCart"
        />
      </div>
    </main>

    <NuxtLink to="#cart" class="threadline-mobile-cart-bar flex items-center justify-between gap-3" :aria-label="`Review bag with ${cart.summary.itemCount} items`">
      <span>
        <span class="block text-[11px] font-bold uppercase tracking-[0.22em] text-threadline-blue">Bag</span>
        <span class="block text-sm font-semibold text-threadline-fog">{{ cart.summary.itemCount }} items</span>
      </span>
      <span class="threadline-button-primary h-11 px-4">${{ cart.summary.subtotal }}</span>
    </NuxtLink>

    <StorefrontFooter />
  </div>
</template>
