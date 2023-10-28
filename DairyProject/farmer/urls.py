from django.urls import path
from . import views

app_name = 'farmer'

urlpatterns = [
    path('farmer-list/', views.FarmerListView.as_view(), name='farmer-list'),
    path('society-list/', views.SocietyListView.as_view(), name='society-list'),
    path('bank-list/', views.BankListView.as_view(), name='bank-list'),
    path('cattle-list/', views.CattleListView.as_view(), name='cattle-list'),
    path('milking-cattle-list/', views.MilkingCattleListView.as_view(), name='milking-cattle-list'),
    path('health-record-list/', views.HealthRecordListView.as_view(), name='health-record-list'),
    path('breed-list/', views.BreedListView.as_view(), name='breed-list'),
    path('customer-list/', views.CustomerListView.as_view(), name='customer-list'),
    # You can add more URLs for other views as needed
]
