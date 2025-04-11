from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stores/', views.stores, name='stores'),
    path('sustainability/', views.sustainability, name='sustainability'),
]