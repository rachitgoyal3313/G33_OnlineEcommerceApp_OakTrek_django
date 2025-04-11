from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def sustainability(request):
    return render(request, 'sustainability.html')

def stores(request):
    return render(request, 'stores.html')

def coming_soon(request):
    return render(request, "coming_soon.html")

def products_view(request, collection_name):
    context = {
        'collection_name': collection_name,
    }
    return render(request, 'products.html', context)



from django.shortcuts import render

def product_page_view(request, collection_name, product_slug):
    context = {
        'collection_name': collection_name,
        'product_slug': product_slug,
    }
    return render(request, 'product_page.html', context)
