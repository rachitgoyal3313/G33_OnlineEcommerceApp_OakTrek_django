from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<str:collection_name>/', views.products_view, 
    name='products'),
    path('products/<str:collection_name>/<slug:product_slug>/', views.product_page_view, name='product_page'),
    path('stores/', views.stores, name='stores'),
    path('coming_soon/', views.coming_soon, name='coming_soon'),
    path('sustainability/', views.sustainability, name='sustainability'),
]