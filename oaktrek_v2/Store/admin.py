from django.contrib import admin
from .models import Product, Review, Cart, Wishlist, Order, OrderItem
from django.utils.html import format_html


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'gender', 'price', 'rating', 'display_image')
    list_filter = ('category', 'gender')
    search_fields = ('product_name', 'category')
    prepopulated_fields = {'slug': ('product_name',), 'category_slug': ('category',)}

    def display_image(self, obj):
        if obj.image_1:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image_1.url))
        return "-"
    
    # Set a more descriptive column name
    display_image.short_description = 'Image'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__product_name')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__product_name')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__product_name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_amount')
    list_filter = ('order_date',)
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

# No need to register OrderItem separately as it's included as an inline in OrderAdmin