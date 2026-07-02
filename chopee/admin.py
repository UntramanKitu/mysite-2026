from django.contrib import admin
from .models import (
    Shop, Category, Product, ProductImage, Cart, CartItem,
    Order, OrderItem, Review, UserProfile
)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'owner', 'follow_count', 'rating', 'created_at')
    search_fields = ('shop_name', 'owner__username')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('follow_count', 'created_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'price', 'discount_percentage', 'stock', 'sold_count', 'created_at')
    search_fields = ('name', 'shop__shop_name')
    list_filter = ('category', 'created_at', 'discount_percentage')
    readonly_fields = ('sold_count', 'view_count', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_at')
    search_fields = ('product__name',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'created_at')
    search_fields = ('product__name', 'cart__user__username')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_price', 'created_at')
    search_fields = ('order_number', 'user__username')
    list_filter = ('status', 'created_at')
    readonly_fields = ('order_number', 'created_at', 'updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__order_number', 'product__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'created_at')
    search_fields = ('user__username', 'city')
    readonly_fields = ('created_at',)
