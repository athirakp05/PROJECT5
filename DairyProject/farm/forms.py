from django import forms
from django.utils.crypto import get_random_string
from .models import Seller

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['firstname', 'lastname', 'email', 'phone']

    def save(self, commit=True):
        # Generate a unique password with a specified length (e.g., 8 characters)
        unique_password = get_random_string(length=8)

        # Set the password field in the form's model instance
        self.instance.user.set_password(unique_password)

        if commit:
            # Save the form's model instance
            instance = super(SellerForm, self).save(commit=commit)
        else:
            instance = super(SellerForm, self).save(commit=False)

        return instance
