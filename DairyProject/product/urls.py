from django.urls import path
from . import views  # Import your views module

urlpatterns = [
    # Other URL patterns
    path('cat_add/', views.cat_add, name='cat_add'),
    path('product_add/', views.product_add, name='product_add'),
    path('prod_view/', views.prod_view, name='prod_view'),

]
