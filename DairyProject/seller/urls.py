# seller/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.deliveryboy_register, name='deliveryboy_register'),
    # path('login/', views.deliveryboy_login, name='deliveryboy_login'),
    # Add other URL patterns as needed
]
