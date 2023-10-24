# admin.py
from django.contrib import admin
from .models import Seller
from .forms import SellerForm
from .models import generate_random_password  # Import the function to generate a random password
from django.core.mail import send_mail  # Import send_mail to send emails

class SellerAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'phone')
    list_filter = ('firstname', 'lastname', 'email')
    search_fields = ('email', 'firstname', 'lastname')
    actions = ['send_login_details']

    def send_login_details(modeladmin, request, queryset):
        for seller in queryset:
            # Generate a random password for the seller
            password = generate_random_password()  # You need to define this function
            seller.user.set_password(password)
            seller.user.save()

            # Send an email to the seller with login details
            subject = 'Your Seller Account Details'
            message = f'Your login ID is: {seller.user.email}\nYour temporary password is: {password}'
            from_email = 'athirakp808@gmail.com'  # Change to your email address
            recipient_list = [seller.user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            seller.save()
        modeladmin.message_user(request, "Login details sent to selected sellers.")

    send_login_details.short_description = "Send login details to selected sellers"
import random
import string

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


admin.site.register(Seller, SellerAdmin)
