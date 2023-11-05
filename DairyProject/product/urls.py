from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    # Other URL patterns
    path('product_add/', views.product_add, name='product_add'),
    path('prod_view/', views.prod_view, name='prod_view'),

]
