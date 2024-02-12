# In seller/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import DeliveryBoy

class DeliveryBoyLoginForm(AuthenticationForm):
    class Meta:
        model = DeliveryBoy
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add any additional email validation logic here if needed
        return email
