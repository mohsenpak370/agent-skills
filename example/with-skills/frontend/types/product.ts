export interface Product {
  id: number
  name: string
  category: 'men' | 'women' | 'kids' | 'accessories'
  description: string
  price: string
  imageUrl: string
  isAvailable: boolean
}

export interface ProductCategory {
  value: 'all' | Product['category']
  label: string
  description: string
}

export interface ProductSortOption {
  value: 'featured' | 'priceAsc' | 'priceDesc' | 'newest'
  label: string
}

export interface ProductListResponse {
  data: Product[]
  pagination: {
    page: number
    pageSize: number
    totalItems: number
    totalPages: number
  }
}
