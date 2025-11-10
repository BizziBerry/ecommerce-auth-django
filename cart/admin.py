from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'cart', 'quantity', 'price', 'total_price', 'added_at')
    list_filter = ('added_at', 'cart')
    search_fields = ('product_name', 'cart__user__email')
    readonly_fields = ('added_at',)

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Общая стоимость'
