from django.contrib import admin
from .models import Product,MilkCollection,Cart,Payment

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(MilkCollection)
admin.site.register(Payment)
