from django.urls import path

from .views import cart_detail, cart_item_detail, cart_items, product_detail, product_list


urlpatterns = [
    path("products/", product_list, name="product-list"),
    path("products/<int:product_id>/", product_detail, name="product-detail"),
    path("cart/", cart_detail, name="cart-detail"),
    path("cart/items/", cart_items, name="cart-items"),
    path("cart/items/<int:item_id>/", cart_item_detail, name="cart-item-detail"),
]
