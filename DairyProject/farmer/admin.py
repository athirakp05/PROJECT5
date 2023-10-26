from django.contrib import admin
from .models import Farmer, Society, Bank, Cattle, MilkingCattle, Breed, Customer, HealthRecord

admin.site.register(Farmer)
admin.site.register(Society)
admin.site.register(Bank)
admin.site.register(Cattle)
admin.site.register(MilkingCattle)
admin.site.register(Breed)
admin.site.register(Customer)
admin.site.register(HealthRecord)
