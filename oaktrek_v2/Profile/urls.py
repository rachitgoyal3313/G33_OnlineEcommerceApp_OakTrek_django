from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.profile_view, name='profile'),
    path('addresses/', views.address_list_view, name='address_list'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('signup/', views.register_view, name='signup')
]
