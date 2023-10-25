from django import forms
from django.utils.crypto import get_random_string
from .models import Seller
import re

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['firstname', 'lastname', 'phone', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Define a regular expression pattern to validate the email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            raise forms.ValidationError("Invalid email format. Use a valid email address.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Remove non-numeric characters from the phone number
        cleaned_phone = re.sub(r'\D', '', phone)
        
        if len(cleaned_phone) != 10:
            raise forms.ValidationError("Mobile number must be 10 digits long.")
        return cleaned_phone

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
