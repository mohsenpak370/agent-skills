<script setup lang="ts">
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

type ProductDetail = {
  product: Product
  related_products: Product[]
}

type CartItem = {
  product: Product
  quantity: number
  line_total: string
}

type Cart = {
  cart_id: string
  items: CartItem[]
  total_items: number
  total_price: string
}

type CartRequestOptions = {
  method?: 'GET' | 'POST' | 'DELETE'
  body?: unknown
  headers?: Record<string, string>
}

const route = useRoute()
const config = useRuntimeConfig()
const cart = ref<Cart | null>(null)
const cartError = ref('')
const activeProductId = ref<number | null>(null)

const { data, pending, error, refresh } = await useFetch<ProductDetail | null>(
  `${config.public.apiBase}/products/${route.params.id}/`,
  { default: () => null }
)

const product = computed(() => data.value?.product)
const relatedProducts = computed(() => data.value?.related_products ?? [])
const cartItems = computed(() => cart.value?.items ?? [])
const cartCount = computed(() => cart.value?.total_items ?? 0)
const cartTotal = computed(() => cart.value?.total_price ?? '0.00')

const quantitiesByProduct = computed(() => {
  return cartItems.value.reduce<Record<number, number>>((quantities, item) => {
    quantities[item.product.id] = item.quantity
    return quantities
  }, {})
})

function getCartId() {
  return import.meta.client ? localStorage.getItem('cart_id') : null
}

function saveCartId(cartId: string) {
  if (import.meta.client) {
    localStorage.setItem('cart_id', cartId)
  }
}

async function cartRequest(path: string, options: CartRequestOptions = {}) {
  cartError.value = ''
  const cartId = getCartId()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers
  }

  if (cartId) {
    headers['X-Cart-Id'] = cartId
  }

  const response = await $fetch<Cart>(`${config.public.apiBase}${path}`, {
    ...options,
    headers
  })

  cart.value = response
  saveCartId(response.cart_id)
  return response
}

async function loadCart() {
  try {
    await cartRequest('/cart/')
  } catch {
    cartError.value = 'Could not load your cart.'
  }
}

async function addToCart(productId: number) {
  activeProductId.value = productId
  try {
    await cartRequest('/cart/items/', {
      method: 'POST',
      body: { product_id: productId, quantity: 1 }
    })
  } catch {
    cartError.value = 'Could not add this product.'
  } finally {
    activeProductId.value = null
  }
}

async function increaseItem(productId: number) {
  activeProductId.value = productId
  try {
    await cartRequest(`/cart/items/${productId}/increase/`, { method: 'POST' })
  } catch {
    cartError.value = 'Could not increase quantity.'
  } finally {
    activeProductId.value = null
  }
}

async function decreaseItem(productId: number) {
  activeProductId.value = productId
  try {
    await cartRequest(`/cart/items/${productId}/decrease/`, { method: 'POST' })
  } catch {
    cartError.value = 'Could not decrease quantity.'
  } finally {
    activeProductId.value = null
  }
}

onMounted(loadCart)
</script>

<template>
  <div class="min-h-screen text-stone-950">
    <SiteHeader :cart-count="cartCount" />

    <main>
      <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div v-if="pending" class="surface-card rounded-[1.75rem] p-6">Loading product...</div>

        <div
          v-else-if="error || !product"
          class="rounded-[1.75rem] border border-red-200 bg-red-50 p-6 text-red-900"
        >
          <p class="text-lg font-extrabold">Product not found</p>
          <p class="mt-1 text-sm">We could not load this product. It may no longer be available.</p>
          <div class="mt-4 flex flex-wrap gap-3">
            <button class="rounded-full bg-stone-950 px-4 py-2 text-sm font-bold text-white" @click="refresh()">Try again</button>
            <NuxtLink to="/products" class="rounded-full border border-red-200 bg-white px-4 py-2 text-sm font-bold text-red-900">Back to shop</NuxtLink>
          </div>
        </div>

        <template v-else>
          <NuxtLink :to="`/products?category=${product.category}`" class="mb-5 inline-flex rounded-full px-3 py-2 text-sm font-bold text-amber-800 transition hover:bg-amber-100">
            Back to {{ product.category }}
          </NuxtLink>

          <section class="grid gap-6 lg:grid-cols-[0.95fr_1fr]">
            <div class="product-card overflow-hidden rounded-[2rem] lg:sticky lg:top-24 lg:h-fit">
              <div class="relative">
                <img v-if="product.image_url" :src="product.image_url" :alt="product.name" class="h-[420px] w-full object-cover lg:h-[680px]">
                <div v-else class="flex h-[420px] items-center justify-center bg-stone-200 text-stone-500 lg:h-[680px]">No image</div>
                <span v-if="product.featured" class="absolute right-4 top-4 rounded-full bg-amber-300 px-3 py-1 text-xs font-bold text-stone-950">
                  Featured
                </span>
              </div>
            </div>

            <section class="surface-card rounded-[2rem] p-6 sm:p-8">
              <p class="mb-4 inline-flex rounded-full bg-amber-100 px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-amber-800">
                {{ product.brand }}
              </p>
              <h1 class="display-title text-5xl font-extrabold sm:text-7xl">
                {{ product.name }}
              </h1>
              <p class="mt-5 text-3xl font-extrabold tracking-[-0.04em]">${{ product.price }}</p>
              <p class="mt-5 max-w-2xl text-lg leading-8 text-stone-600">{{ product.description }}</p>

              <div class="mt-8 grid gap-3 sm:grid-cols-2">
                <div class="warm-panel rounded-3xl p-5"><p class="text-xs font-bold uppercase tracking-[0.16em] text-stone-500">Category</p><p class="mt-1 font-extrabold capitalize">{{ product.category }}</p></div>
                <div class="warm-panel rounded-3xl p-5"><p class="text-xs font-bold uppercase tracking-[0.16em] text-stone-500">Color</p><p class="mt-1 font-extrabold">{{ product.color }}</p></div>
                <div class="warm-panel rounded-3xl p-5"><p class="text-xs font-bold uppercase tracking-[0.16em] text-stone-500">Size</p><p class="mt-1 font-extrabold">{{ product.size }}</p></div>
                <div class="warm-panel rounded-3xl p-5"><p class="text-xs font-bold uppercase tracking-[0.16em] text-stone-500">Brand</p><p class="mt-1 font-extrabold">{{ product.brand }}</p></div>
              </div>

              <div v-if="cartError" class="mt-6 rounded-2xl border border-red-200 bg-red-50 p-3 text-sm font-semibold text-red-900">{{ cartError }}</div>

              <div class="mt-8 flex flex-col gap-4 border-t border-stone-200 pt-6 sm:flex-row sm:items-center sm:justify-between">
                <button
                  v-if="!quantitiesByProduct[product.id]"
                  type="button"
                  class="rounded-full bg-stone-950 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-stone-800 disabled:cursor-wait disabled:opacity-60"
                  :disabled="activeProductId === product.id"
                  @click="addToCart(product.id)"
                >
                  {{ activeProductId === product.id ? 'Adding...' : 'Add to cart' }}
                </button>

                <div v-else class="inline-flex w-fit overflow-hidden rounded-full border border-stone-200 bg-white text-base">
                  <button class="px-4 py-3 font-bold disabled:opacity-50" :disabled="activeProductId === product.id" @click="decreaseItem(product.id)">-</button>
                  <span class="bg-stone-100 px-6 py-3 font-bold">{{ quantitiesByProduct[product.id] }}</span>
                  <button class="px-4 py-3 font-bold disabled:opacity-50" :disabled="activeProductId === product.id" @click="increaseItem(product.id)">+</button>
                </div>

                <div class="text-left sm:text-right">
                  <p class="text-sm font-bold text-stone-500">Cart total</p>
                  <p class="text-2xl font-extrabold">${{ cartTotal }}</p>
                </div>
              </div>
            </section>
          </section>

          <section v-if="relatedProducts.length" class="mt-14">
            <p class="mb-4 inline-flex rounded-full bg-amber-100 px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-amber-800">
              More Like This
            </p>
            <h2 class="display-title mb-6 text-3xl font-extrabold sm:text-5xl">Related products</h2>

            <div class="grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
              <article
                v-for="related in relatedProducts"
                :key="related.id"
                class="product-card overflow-hidden rounded-[1.75rem] transition hover:-translate-y-1"
              >
                <NuxtLink :to="`/products/${related.id}`">
                  <img v-if="related.image_url" :src="related.image_url" :alt="related.name" class="h-64 w-full object-cover">
                  <div class="p-5">
                    <p class="text-xs font-bold uppercase tracking-[0.16em] text-stone-500">{{ related.brand }} / {{ related.color }}</p>
                    <h3 class="mt-2 text-xl font-extrabold tracking-[-0.04em]">{{ related.name }}</h3>
                    <p class="mt-2 line-clamp-2 text-sm leading-6 text-stone-600">{{ related.description }}</p>
                    <p class="mt-5 text-lg font-extrabold">${{ related.price }}</p>
                  </div>
                </NuxtLink>
              </article>
            </div>
          </section>
        </template>
      </div>
    </main>

    <SiteFooter />
  </div>
</template>
