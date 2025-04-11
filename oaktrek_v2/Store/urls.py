from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<str:collection_name>/', views.products_view, 
    name='products'),
    path('products/<str:collection_name>/<slug:product_slug>/', views.product_page_view, name='product_page'),
    path('stores/', views.stores, name='stores'),
    path('coming_soon/', views.coming_soon, name='coming_soon'),
    path('sustainability/', views.sustainability, name='sustainability'),
    path('moonshot/', views.moonshot, name='moonshot'),
    path('adidasxoaktrek/', views.adidasxoaktrek, name='adidasxoaktrek'),
    path('bcorp/', views.bcorp, name='bcorp'),
    path('mothernature/', views.mothernature, name='mothernature'),
    path('carbonFootprint/', views.carbonFootprint, name='carbonoffsets'),
    path('oaktrek_help/', views.oaktrek_help, name='oaktrek_help'),
    path('returns/', views.returns, name='returns'),
    path('faq/', views.faq, name='faq'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)