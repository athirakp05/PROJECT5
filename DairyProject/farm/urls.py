from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.loginn, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('customer/dashboard/', views.c_dashboard, name='c_dashboard'),
    path('seller/dashboard/', views.s_dashboard, name='s_dashboard'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('view_customers/', views.view_customers, name='view_customers'),
    path('view_sellers/', views.view_sellers, name='view_sellers'),
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('sellers/', views.SellerListView.as_view(), name='seller-list'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('seller_list/', views.seller_list, name='seller_list'),
   # path('seller/<int:seller_id>/', views.seller_login_details, name='seller-login-details'),
    path('update_s/<int:seller_id>/', views.update_s, name='update_s'),
    path('delete_s/<int:seller_id>/', views.delete_s, name='delete_s'),
    path('add_seller/', views.add_seller, name='add_seller'),  # Add this line to define the URL pattern for the "add_seller" view
    path('c_delete/<int:customer_id>/', views.c_delete, name='c_delete'),
    path('edit_customer/', views.edit_customer, name='edit_customer'),
    path('edit_seller/<int:seller_id>/', views.edit_seller, name='edit_seller'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),


]
