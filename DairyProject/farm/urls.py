from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('',views.index,name='home'),
   # path('store',views.store,name='store'),
    path('login',views.loginn,name='login'),
    path('registration',views.register,name='registration'),
    path('logout',views.logout,name='logout'),
    path('c_dashboard',views.c_dashboard,name='c_dash'),

]
