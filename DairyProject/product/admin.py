from django.contrib import admin
from .models import Order, Product,MilkCollection,Cart,Payment

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(MilkCollection)
admin.site.register(Payment)
admin.site.register(Order)
