from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<str:collection_name>/', views.products_view, name='products'),
    path('products/<str:collection_name>/<slug:product_slug>/', views.product_page_view, name='product_page'),
    path('stores/', views.stores, name='stores'),
    path('coming_soon/', views.coming_soon, name='coming_soon'),
    path('moonshot/', views.moonshot, name='moonshot'),
    path('adidasxoaktrek/', views.adidasxoaktrek, name='adidasxoaktrek'),
    path('bcorp/', views.bcorp, name='bcorp'),
    path('mothernature/', views.mothernature, name='mothernature'),
    path('carbonFootprint/', views.carbonFootprint, name='carbonoffsets'),
    path('oaktrek_help/', views.oaktrek_help, name='oaktrek_help'),
    path('returns/', views.returns, name='returns'),
    path('faq/', views.faq, name='faq'),
    path('aboutUs/', views.aboutUs, name='about_us'),
    path('our_story/', views.our_story, name='our_story'),
    path('our_materials/', views.our_materials, name='our_materials'),
    path('sustainability/', views.sustainability, name='sustainability'),
    path('regenerative/', views.regenerative, name='regenerative'),
    path('renewable/', views.renewable, name='renewable'),
    path('terms/', views.terms, name='terms'),
    path('responsibleEnergy/', views.responsibleEnergy, name='responsibleEnergy'),
    # New paths for apparel and socks
    path('products/mens-apparel/', views.products_view, name='mens_apparel'),
    path('products/womens-apparel/', views.products_view, name='womens_apparel'),
    path('products/socks/', views.products_view, name='socks'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)