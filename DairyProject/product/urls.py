from django.urls import path
from . import views  

urlpatterns = [
    path('product_add/', views.product_add, name='product_add'),
    path('prod_view/', views.prod_view, name='prod_view'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('milk_details/', views.milk_details, name='milk_details'),
    path('milk_edit/<int:pk>/', views.milk_edit, name='milk_edit'),
    path('milk_view/', views.milk_list, name='milk_list'),  # List all milk collections
    path('milk_view/', views.milk_view, name='milk_view'),  # View individual milk collection
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('product_detail/', views.product_detail, name='product_detail'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('product_detail/', views.common_search, name='common_search'),  # List all milk collections

]
