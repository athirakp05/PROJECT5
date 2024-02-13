# seller/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('delivery_register/', views.delivery_register, name='delivery_register'),
    # path('delivery_dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    # path('login/', views.deliveryboy_login, name='deliveryboy_login'),
    # path('admin/delivery/approval/', views.admin_delivery_approval, name='admin_delivery_approval'),
    # path('admin/delivery/approve/<int:registration_id>/', views.approve_delivery_registration, name='approve_delivery_registration'),
    ]
