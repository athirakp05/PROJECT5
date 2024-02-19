# seller/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('delivery_register/', views.delivery_register, name='delivery_register'),
    path('delivery_dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    # path('login/', views.deliveryboy_login, name='deliveryboy_login'),
    path('deliveryboy_approval/', views.deliveryboy_approval, name='deliveryboy_approval'),
    # path('admin/delivery/approve/<int:registration_id>/', views.approve_delivery_registration, name='approve_delivery_registration'),
    ]
