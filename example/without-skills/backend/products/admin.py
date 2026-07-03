from django.contrib import admin

from .models import Cart, CartItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price", "featured", "is_available", "created_at")
    list_filter = ("category", "featured", "is_available")
    search_fields = ("name", "description", "brand", "color")


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    inlines = [CartItemInline]
