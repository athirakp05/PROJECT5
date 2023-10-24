from django.contrib import admin
from .models import CustomUser, Seller
from .forms import SellerRegistrationForm

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_customer', 'is_seller', 'is_superuser')
    list_filter = ('is_customer', 'is_seller', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_customer', 'is_seller', 'is_superuser')}),
        # Add other fieldsets as needed for custom user fields
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_customer', 'is_seller', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

class SellerAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'phone')  # Add or remove fields as needed
    search_fields = ('firstname', 'lastname', 'email', 'phone')  # Add or remove fields as needed
    list_filter = ()  # Add or remove fields as needed
    add_form = SellerRegistrationForm

    def save_model(self, request, obj, form, change):
        # You may need to set up the password and other fields manually here
        # For example, to hash the password, use the following:
        obj.set_password(form.cleaned_data['password'])
        obj.save()
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Seller, SellerAdmin)
