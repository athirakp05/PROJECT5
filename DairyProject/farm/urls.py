from django.urls import path
from . import views  
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from .views import s_profile, complete_prof


urlpatterns = [
    path('',views.index,name='home'),
    #path('admin',views.admin,name='admin'),
    path('login', views.loginn, name='login'),
    path('c_register',views.c_register,name='c_register'),
    path('s_register/', views.s_register, name='s_register'),
    path('logout',views.logout,name='logout'),
    path('about',views.logout,name='about'),
    path('c_dashboard', views.c_dashboard, name='c_dashboard'),
    path('s_dashboard', views.s_dashboard, name='s_dashboard'),
    path('a_dashboard/', views.a_dashboard, name='a_dashboard'),
    path('add_cattle', views.add_cattle, name='add_cattle'),
    path('edit_cattle/', views.edit_cattle, name='edit_cattle'),
    path('view_cattle/', views.view_cattle, name='view_cattle'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('s_view', views.s_view, name='s_view'),
    path('c_view', views.c_view, name='c_view'),
    path('select', views.select, name='select'),
    path('profile', views.profile, name='profile'),
    path('common_search', views.common_search, name='common_search'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('s_profile/', s_profile, name='s_profile'),
    path('complete_prof/', complete_prof, name='complete_prof'),
]
