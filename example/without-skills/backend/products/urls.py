from django.urls import path

from .views import add_cart_item, cart_detail, category_list, clear_cart, decrease_cart_item, increase_cart_item, product_detail, product_list, remove_cart_item

urlpatterns = [
    path("categories/", category_list, name="category-list"),
    path("products/", product_list, name="product-list"),
    path("products/<int:product_id>/", product_detail, name="product-detail"),
    path("cart/", cart_detail, name="cart-detail"),
    path("cart/items/", add_cart_item, name="add-cart-item"),
    path("cart/items/<int:product_id>/increase/", increase_cart_item, name="increase-cart-item"),
    path("cart/items/<int:product_id>/decrease/", decrease_cart_item, name="decrease-cart-item"),
    path("cart/items/<int:product_id>/", remove_cart_item, name="remove-cart-item"),
    path("cart/clear/", clear_cart, name="clear-cart"),
]
