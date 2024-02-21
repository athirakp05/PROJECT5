# seller/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('delivery_register/', views.delivery_register, name='delivery_register'),
    path('delivery_dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('delivery_boys/', views.delivery_boys, name='delivery_boys'),
    # path('deliveryboy_approval/', views.deliveryboy_approval, name='deliveryboy_approval'),
    # path('activate/<uidb64>/<token>/', views.activate_delivery_boy, name='activate_delivery_boy'),
]
