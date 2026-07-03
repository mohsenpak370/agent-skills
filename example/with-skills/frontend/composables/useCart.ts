import type { CartResponse } from '~/types/cart'

const emptyCart = (): CartResponse => ({
  cartId: '',
  items: [],
  summary: { itemCount: 0, subtotal: '0.00' },
})

export function useCart() {
  const config = useRuntimeConfig()
  const cart = useState<CartResponse>('cart', emptyCart)
  const pending = shallowRef(false)
  const errorMessage = shallowRef('')

  const cartId = computed(() => cart.value.cartId)
  const cartQuantities = computed(() =>
    Object.fromEntries(cart.value.items.map((item) => [item.product.id, item.quantity])),
  )

  function saveCartId(id: string) {
    if (!import.meta.client || id === '') {
      return
    }
    localStorage.setItem('cartId', id)
  }

  function storedCartId() {
    if (!import.meta.client) {
      return ''
    }
    return localStorage.getItem('cartId') || ''
  }

  async function requestCart<T>(path: string, options: Parameters<typeof $fetch<T>>[1] = {}) {
    errorMessage.value = ''

    try {
      const response = await $fetch<CartResponse>(`${config.public.apiBase}${path}`, options)
      cart.value = response
      saveCartId(response.cartId)
      return response
    } catch (error) {
      errorMessage.value = 'Cart could not be updated. Please try again.'
      throw error
    }
  }

  async function loadCart() {
    pending.value = true
    try {
      const query = storedCartId() ? { cartId: storedCartId() } : undefined
      await requestCart('/cart/', { query })
    } finally {
      pending.value = false
    }
  }

  async function addItem(productId: number) {
    pending.value = true
    try {
      await requestCart('/cart/items/', {
        method: 'POST',
        body: { cartId: cartId.value || storedCartId(), productId, quantity: 1 },
      })
    } finally {
      pending.value = false
    }
  }

  async function updateItem(itemId: number, quantity: number) {
    pending.value = true
    try {
      await requestCart(`/cart/items/${itemId}/`, {
        method: 'PATCH',
        body: { cartId: cartId.value || storedCartId(), quantity },
      })
    } finally {
      pending.value = false
    }
  }

  async function removeItem(itemId: number) {
    pending.value = true
    try {
      await requestCart(`/cart/items/${itemId}/`, {
        method: 'DELETE',
        query: { cartId: cartId.value || storedCartId() },
      })
    } finally {
      pending.value = false
    }
  }

  async function clearCart() {
    pending.value = true
    try {
      await requestCart('/cart/', {
        method: 'DELETE',
        query: { cartId: cartId.value || storedCartId() },
      })
    } finally {
      pending.value = false
    }
  }

  return {
    cart,
    cartQuantities,
    pending: readonly(pending),
    errorMessage: readonly(errorMessage),
    loadCart,
    addItem,
    updateItem,
    removeItem,
    clearCart,
  }
}
