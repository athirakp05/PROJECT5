from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('',views.index,name='home'),
    #path('admin',views.admin,name='admin'),
    path('login',views.loginn,name='login'),
    path('registration',views.registration,name='registration'),
    path('logout',views.logout,name='logout'),
    path('c_dashboard/', views.c_dashboard, name='c_dashboard')  # Remove the trailing slash
    #path('s_dashboard', views.s_dashboard, name='s_dashboard'),

]
