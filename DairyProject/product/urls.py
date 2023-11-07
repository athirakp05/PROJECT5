from django.urls import path
from . import views  

urlpatterns = [
    path('product_add/', views.product_add, name='product_add'),
    path('prod_view/', views.prod_view, name='prod_view'),
    path('milk_details/', views.milk_details, name='milk_details'),
    path('milk_edit/<int:pk>/', views.milk_edit, name='milk_edit'),
    path('milk_view/', views.milk_list, name='milk_list'),  # List all milk collections
    path('milk_view/<int:pk>/', views.milk_view, name='milk_view'),  # View individual milk collection
]
