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

    