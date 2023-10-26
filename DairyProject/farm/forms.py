from django import forms
from .models import Seller
from .models import Customer
from .models import CustomerEdit
from .models import SellerEdit

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['firstname', 'lastname', 'email', 'phone']
        # forms.py



class CustomerEdit(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'email', 'phone']

class SellerEditForm(forms.ModelForm):
    class Meta:
        model = SellerEdit
        fields = '__all__'  # You can specify the fields you want to include in the form



