from django.urls import path
from . import views  


urlpatterns = [
       path('milk_quality_prediction/', views.milk_quality_prediction, name='milk_quality_prediction'),

]