# event/urls.py
from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('meeting/', views.meeting, name='meeting'),
    path('meetinglist/', views.meetinglist, name='meetinglist'),
    path('generate_brochure/<int:meeting_id>/', views.generate_brochure, name='generate_brochure'),
    path('meeting_details_list/', views.meeting_details_list, name='meeting_details_list'),
    path('add_meeting_details/', views.add_meeting_details, name='add_meeting_details'),
    path('update_meeting_details/', views.update_meeting_details, name='update_meeting_details'),

]
