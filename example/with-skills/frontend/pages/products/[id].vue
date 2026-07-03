<script setup lang="ts">
import ProductDetailView from '~/components/ProductDetailView.vue'
import type { Product } from '~/types/product'

const route = useRoute()
const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl.replace(/\/$/, '')
const productId = computed(() => String(route.params.id))
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

const { data: product, pending, error } = await useFetch<Product>(
  () => `${config.public.apiBase}/products/${productId.value}/`,
)

const productUrl = computed(() => `${siteUrl}/products/${productId.value}`)
const pageTitle = computed(() => product.value ? product.value.name : 'Product')
const pageDescription = computed(() => {
  if (!product.value) {
    return 'Shop refined wardrobe pieces, accessories, and private client service from Threadline Atelier.'
  }

  return product.value.description.length > 155
    ? `${product.value.description.slice(0, 152)}...`
    : product.value.description
})
const cartQuantity = computed(() => product.value ? cartQuantities.value[product.value.id] || 0 : 0)

useSeoMeta({
  title: pageTitle,
  description: pageDescription,
  ogTitle: computed(() => product.value ? `${product.value.name} | Threadline Atelier` : 'Product | Threadline Atelier'),
  ogDescription: pageDescription,
  ogImage: computed(() => product.value?.imageUrl || ''),
  ogUrl: productUrl,
  ogType: 'product',
  twitterTitle: computed(() => product.value ? `${product.value.name} | Threadline Atelier` : 'Product | Threadline Atelier'),
  twitterDescription: pageDescription,
  twitterImage: computed(() => product.value?.imageUrl || ''),
})

useHead({
  link: [
    { rel: 'canonical', href: productUrl },
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: computed(() => JSON.stringify({
        '@context': 'https://schema.org',
        '@graph': [
          {
            '@type': 'Product',
            '@id': `${productUrl.value}#product`,
            name: product.value?.name || 'Threadline Atelier product',
            description: pageDescription.value,
            image: product.value?.imageUrl ? [product.value.imageUrl] : undefined,
            brand: {
              '@type': 'Brand',
              name: 'Threadline Atelier',
            },
            category: product.value?.category,
            offers: product.value
              ? {
                  '@type': 'Offer',
                  url: productUrl.value,
                  priceCurrency: 'USD',
                  price: product.value.price,
                  availability: product.value.isAvailable ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock',
                  itemCondition: 'https://schema.org/NewCondition',
                }
              : undefined,
          },
          {
            '@type': 'BreadcrumbList',
            itemListElement: [
              { '@type': 'ListItem', position: 1, name: 'Home', item: siteUrl },
              { '@type': 'ListItem', position: 2, name: 'Products', item: `${siteUrl}/products` },
              { '@type': 'ListItem', position: 3, name: product.value?.name || 'Product', item: productUrl.value },
            ],
          },
        ],
      }).replace(/</g, '\\u003c')),
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
      <div v-if="pending" class="grid gap-5 lg:grid-cols-[minmax(0,1fr)_380px]">
        <UCard :ui="{ body: 'space-y-4' }">
          <USkeleton class="h-[560px] w-full" />
        </UCard>
        <UCard :ui="{ body: 'space-y-4' }">
          <USkeleton class="h-6 w-32" />
          <USkeleton class="h-12 w-full" />
          <USkeleton class="h-28 w-full" />
        </UCard>
      </div>
      <section v-else-if="error || !product" class="mx-auto max-w-2xl py-20" aria-labelledby="missing-product-title">
        <div class="threadline-panel space-y-5 p-8 text-center">
          <p class="threadline-label">Not found</p>
          <h1 id="missing-product-title" class="text-4xl font-black tracking-[-0.05em] text-threadline-fog">This product is not available.</h1>
          <p class="text-zinc-200">It may have sold out or been removed from the current edit.</p>
          <UButton to="/products" color="neutral" size="lg" class="mx-auto">Return to shop</UButton>
        </div>
      </section>

      <div v-else class="grid gap-6 lg:grid-cols-[minmax(0,1fr)_380px] lg:items-start">
        <ProductDetailView
          :product="product"
          :cart-quantity="cartQuantity"
          :is-busy="cartPending"
          @add-to-cart="addItem"
        />

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
