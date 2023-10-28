from django import forms
from .models import CustomUser
from .models import Seller
from .models import SellerEdit
from .models import Customer


class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'phone', 'email', 'password']


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['firstname', 'lastname', 'email', 'phone']


class CustomerEdit(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'email', 'phone']  # Include the fields you want to allow customers to edit

class SellerEditForm(forms.ModelForm):
    class Meta:
        model = SellerEdit
        fields = ['FirstName', 'LastName', 'HouseName', 'City', 'PinCode', 'Occupation', 'Gender', 'DOB', 'RationcardNo', 'Email', 'Mobile', 'AccNo', 'Societycode', 'Photo']