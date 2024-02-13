from django.urls import path
from . import views  
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from .views import SellerPasswordChangeView, complete_c_profile, s_profile, complete_s_profile,v_register

urlpatterns = [
    path('',views.index,name='home'),
    #path('admin',views.admin,name='admin'),
    path('login', views.loginn, name='login'),
    path('c_register',views.c_register,name='c_register'),
    path('s_register/', views.s_register, name='s_register'),
    path('logout/', views.logout_user, name='logout'),
    path('c_dashboard', views.c_dashboard, name='c_dashboard'),
    path('s_dashboard', views.s_dashboard, name='s_dashboard'),
    path('v_dashboard', views.v_dashboard, name='v_dashboard'),
    # path('delivery_dashboard', views.delivery_dashboard, name='delivery_dashboard'),
    path('admindash/', views.admindash, name='admindash'),
    path('add_cattle', views.add_cattle, name='add_cattle'),
    path('fetch_breeds/', views.fetch_breeds, name='fetch_breeds'),
    path('view_cattle/', views.view_cattle, name='view_cattle'),
    path('edit_cattle/<int:cattle_id>/', views.edit_cattle, name='edit_cattle'),
    path('delete_cattle/<int:cattle_id>/', views.delete_cattle, name='delete_cattle'),    path('add_breed', views.add_breed, name='add_breed'),
    path('view_breed/', views.view_breed, name='view_breed'),  # Define URL for view_breed
    path('delete_breed/<int:breed_id>/', views.delete_breed, name='delete_breed'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('s_view/', views.s_view, name='s_view'),
    path('c_view', views.c_view, name='c_view'),
    path('select', views.select, name='select'),
    path('profile', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('s_profile/', s_profile, name='s_profile'),
    path('seller_profile/', views.seller_profile, name='seller_profile'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('complete_s_profile/', complete_s_profile, name='complete_s_profile'),
    path('complete_c_profile/', complete_c_profile, name='complete_c_profile'),
    path('vaccination/<int:cattle_id>/', views.vac_details, name='vac_details'),
    path('insurance/<int:cattle_id>/', views.ins_details, name='ins_details'),
    path('usercount/', views.usercount, name='usercount'),
    path('society-seller-count/', views.society_seller_count, name='society_seller_count'),
    path('team-list/', views.team, name='team'),
    path('message/', views.message, name='message'),
    path('get_new_messages/', views.get_new_messages, name='get_new_messages'),
    path('pending_sellers/', views.pending_sellers, name='pending_sellers'),
    path('approve_seller/<str:email>/', views.approve_seller, name='approve_seller'),
    path('reject_seller/<str:email>/', views.reject_seller, name='reject_seller'),
    path('activate-customer/<str:email>/', views.activate_customer, name='activate_c'),
    path('deactivate-customer/<str:email>/', views.deactivate_customer, name='deactivate_c'),
    path('activate-seller/<str:email>/', views.activate_seller, name='activate_s'),
    path('deactivate-seller/<str:email>/', views.deactivate_seller, name='deactivate_s'),        
    path('seller/password_change/', SellerPasswordChangeView.as_view(), name='seller_password_change'),
    path('admin_view_cattle/', views.admin_view_cattle, name='admin_view_cattle'),
    path('search-sellers/', views.search_sellers, name='search_sellers'),
    path('v_register/', v_register, name='v_register'),

]
