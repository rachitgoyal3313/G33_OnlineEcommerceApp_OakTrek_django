# auctions/models.py
from django.db import models
from Store.models import Product
from Profile.models import User

class LuxuryShoe(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='luxury_auctions')
    starting_bid = models.FloatField()
    auction_start = models.DateTimeField()
    auction_end = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Auction for {self.product.product_name}"

class Bid(models.Model):
    luxury_shoe = models.ForeignKey(LuxuryShoe, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.luxury_shoe.product.product_name}"