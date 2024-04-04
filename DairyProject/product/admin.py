from django.contrib import admin
from .models import Product,MilkSample,Cart,Payment

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(MilkSample)
admin.site.register(Payment)
