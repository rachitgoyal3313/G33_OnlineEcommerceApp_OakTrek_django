# auctions/urls.py
from django.urls import path
from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.auction_list, name='auction_list'),
    path('<int:luxury_shoe_id>/', views.auction_detail, name='auction_detail'),
    # path('test/', views.test_websocket, name='test_websocket'),

]