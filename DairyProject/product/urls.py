from django.urls import path
from . import views  
from .views import p_detail

urlpatterns = [
    path('product_add/', views.product_add, name='product_add'),
    path('prod_view/', views.prod_view, name='prod_view'),
    path('product_detail/', views.product_detail, name='product_detail'),
    path('milk_details/', views.milk_details, name='milk_details'),
    path('milk_edit/<int:pk>/', views.milk_edit, name='milk_edit'),
    path('milk_view/', views.milk_list, name='milk_list'),  # List all milk collections
    path('milk_view/', views.milk_view, name='milk_view'),  # View individual milk collection
    path('p_detail/', p_detail, name='p_detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('payment/', views.payment, name='payment'),
    path('process_payment/', views.process_payment, name='process_payment'),
]