from django.shortcuts import render
from django.views.generic import ListView
from .models import Farmer

class FarmerListView(ListView):
    model = Farmer
    template_name = 'farmer/farmer_list.html'
    context_object_name = 'farmers'
