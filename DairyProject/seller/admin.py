from pyexpat.errors import messages
from django.contrib import admin
from .models import ApprovalRequest, DeliveryBoy, Delivery

admin.site.register(Delivery)  # You can keep this if needed

class DeliveryBoyAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_delivery_boys']

    def approve_delivery_boys(self, request, queryset):
        for delivery_boy in queryset:
            # Create an ApprovalRequest for each selected delivery boy
            approval_request = ApprovalRequest.objects.create(delivery_boy=delivery_boy)

        messages.success(request, 'Approval requests sent for selected delivery boys.')

    approve_delivery_boys.short_description = 'Send approval requests for selected delivery boys'

admin.site.register(DeliveryBoy, DeliveryBoyAdmin)
