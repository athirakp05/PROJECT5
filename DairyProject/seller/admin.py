from django.contrib import admin
from .models import DeliveryBoy, Delivery

admin.site.register(DeliveryBoy)
admin.site.register(Delivery)
class DeliveryBoyAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_delivery_boys']

    def approve_delivery_boys(self, request, queryset):
        queryset.update(is_approved=True)

    approve_delivery_boys.short_description = 'Approve selected delivery boys'
