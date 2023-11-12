from django.urls import path
from . import views  
from .views import p_detail,view_wishlist,rmv_wishlist,add_wishlist  # Import the p_detail view

urlpatterns = [
    path('product_add/', views.product_add, name='product_add'),
    path('prod_view/', views.prod_view, name='prod_view'),
    path('product_detail/', views.product_detail, name='product_detail'),
    path('milk_details/', views.milk_details, name='milk_details'),
    path('milk_edit/<int:pk>/', views.milk_edit, name='milk_edit'),
    path('milk_view/', views.milk_list, name='milk_list'),  # List all milk collections
    path('milk_view/', views.milk_view, name='milk_view'),  # View individual milk collection
    path('wishlist/', view_wishlist, name='wishlist'),
    path('add_wishlist/<int:product_id>/', add_wishlist, name='add_wishlist'),
    path('rmv_wishlist/<int:product_id>/', rmv_wishlist, name='rmv_wishlist'),
    path('product_detail/', views.common_search, name='common_search'),  # List all milk collections
    path('p_detail/', p_detail, name='p_detail'),

]
