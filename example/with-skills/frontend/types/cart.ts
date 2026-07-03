import type { Product } from '~/types/product'

export interface CartItem {
  id: number
  quantity: number
  lineTotal: string
  product: Product
}

export interface CartSummary {
  itemCount: number
  subtotal: string
}

export interface CartResponse {
  cartId: string
  items: CartItem[]
  summary: CartSummary
}
