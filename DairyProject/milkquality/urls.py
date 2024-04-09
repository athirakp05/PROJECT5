from django.urls import path
from . import views  


urlpatterns = [
       path('milkquality/', views.milk_quality_prediction, name='milk_quality_prediction'),

]