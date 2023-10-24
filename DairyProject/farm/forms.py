# forms.py

from django import forms
from .models import Seller

class SellerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['firstname', 'lastname', 'email', 'password', 'phone']

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
