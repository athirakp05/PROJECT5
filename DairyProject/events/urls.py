# event/urls.py
from django import views
from django.urls import path
from .views import generate_brochure, meeting, meetinglist

urlpatterns = [
    path('meeting/', meeting, name='meeting'),
    path('meetinglist/', meetinglist, name='meetinglist'),
    path('generate_brochure/<int:meeting_id>/', generate_brochure, name='generate_brochure'),
]
