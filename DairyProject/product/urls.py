from django.urls import path
from . import views  
from .views import addSample_test, milk_parameters, p_detail,update_quantity
from .views import sample_report

urlpatterns = [
    path('product_add/', views.product_add, name='product_add'),
    path('prod_view/', views.prod_view, name='prod_view'),
    path('product_detail/', views.product_detail, name='product_detail'),
    path('p_detail/', p_detail, name='p_detail'),
    path('add_to_cart/<int:p_code>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<str:p_code>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('payment/', views.payment, name='payment'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('add_milk_details/', views.add_milk_details, name='add_milk_details'),
    path('edit_milk_details/<int:pk>/', views.edit_milk_details, name='edit_milk_details'),
    path('all_milk_details/', views.all_milk_details, name='all_milk_details'),
    path('own_milk_details/', views.own_milk_details, name='own_milk_details'),
    path('search_products/', views.search_products, name='search_products'),
    path('view_carts/', views.view_carts, name='view_carts'),
    path('success', views.success, name='success'),
    path('update_quantity/', update_quantity, name='update_quantity'),
    path('sample_report/', sample_report, name='sample_report'),
    path('addSample_test/', addSample_test, name='addSample_test'),
    path('milk_parameters/', milk_parameters, name='milk_parameters'),
    path('admin_cart/', views.admin_cart, name='admin_cart'),
    path('order_history/', views.order_history, name='order_history'),
    path('payment-history/', views.payment_history, name='payment_history'),

]