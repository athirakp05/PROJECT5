from django.urls import path
from . import views  
from .views import addSample_test, milk_parameters, p_detail,update_quantity
from .views import sample_report

urlpatterns = [
    path('product_add/', views.product_add, name='product_add'),
    path('prod_view/', views.prod_view, name='prod_view'),
    path('product_detail/', views.product_detail, name='product_detail'),
    path('p_detail/', p_detail, name='p_detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_quantity/<int:cart_item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_history/', views.payment_history, name='payment_history'),
    path('order_history/', views.order_history, name='order_history'),
    path('order/', views.order, name='order'),
    path('update_delivery_status/<int:order_id>/', views.update_delivery_status, name='update_delivery_status'),
    path('add_milk_details/', views.add_milk_details, name='add_milk_details'),
    path('edit_milk_details/<int:pk>/', views.edit_milk_details, name='edit_milk_details'),
    path('all_milk_details/', views.all_milk_details, name='all_milk_details'),
    path('own_milk_details/', views.own_milk_details, name='own_milk_details'),
    path('search_products/', views.search_products, name='search_products'),
    path('view_carts/', views.view_carts, name='view_carts'),
    path('success/<int:order_id>/', views.success, name='success'),
    path('update_quantity/', update_quantity, name='update_quantity'),
    path('sample_report/', sample_report, name='sample_report'),
    path('addSample_test/', addSample_test, name='addSample_test'),
    path('milk_parameters/', milk_parameters, name='milk_parameters'),
    path('admin_cart/', views.admin_cart, name='admin_cart'),
    path('all_milk_details/export-csv/', views.export_milk_sample_to_csv, name='export_milk_sample_to_csv'),
    path('feedback_submit/', views.feedback_submit, name='feedback_submit'),
    path('cust_order/', views.cust_order, name='cust_order'),
    path('rating_submit/', views.rating_submit, name='rating_submit'),
]