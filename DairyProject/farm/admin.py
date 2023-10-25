from django.contrib import admin
from .models import Seller
from .forms import SellerForm
from .utils import generate_random_password
from django.core.mail import send_mail

class SellerAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'phone')  # Include 'email' in list_display
    list_filter = ('firstname', 'lastname', 'email')  # Include 'email' in list_filter
    search_fields = ('firstname', 'lastname', 'email')  # Include 'email' in search_fields
    actions = ['send_login_details']

    def send_login_details(modeladmin, request, queryset):
        for seller in queryset:
            password = generate_random_password()
            seller.user.set_password(password)
            seller.user.save()

            subject = 'Your Seller Account Details'
            message = f'Your login ID is: {seller.user.email}\nYour temporary password is: {password}'
            from_email = 'athirakp808@gmail.com'
            recipient_list = [seller.user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            seller.save()
        modeladmin.message_user(request, "Login details sent to selected sellers.")

    send_login_details.short_description = "Send login details to selected sellers"

admin.site.register(Seller, SellerAdmin)
