import os
import django

# ✅ Set the settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oaktrek_v2.settings')

# ✅ Setup Django before importing anything model-related
django.setup()

# ✅ Now you can safely import models and Django modules
from django.core.management.base import BaseCommand
from Store.models import Product

if __name__ == "__main__":
        products = Product.objects.all()
        for product in products:
            old_price = product.price
            product.price = round(product.price * 100, 2)
            product.save()
            print(f"Updated {product.product_name}: ₹{old_price} → ₹{product.price}")


