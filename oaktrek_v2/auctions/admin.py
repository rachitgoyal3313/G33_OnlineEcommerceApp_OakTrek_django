# auctions/admin.py
from django.contrib import admin
from .models import LuxuryShoe, Bid

@admin.register(LuxuryShoe)
class LuxuryShoeAdmin(admin.ModelAdmin):
    list_display = ('product', 'starting_bid', 'auction_start', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('product__product_name',)

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('luxury_shoe', 'user', 'amount', 'timestamp')
    list_filter = ('luxury_shoe',)
    search_fields = ('user__username',)