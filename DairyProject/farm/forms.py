
from django import forms
# forms.py
from .models import SellerEditProfile,Cattle


class SellerProfileEditForm(forms.ModelForm):
    class Meta:
        model = SellerEditProfile
        fields = ['first_name', 'last_name', 'house_name', 'city', 'pin_code', 'occupation', 'gender', 'dob', 'rationcard_no', 'email', 'mobile', 'acc_no', 'society', 'profile_photo']


class CustomerRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(max_length=15)

class SellerRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    mobile = forms.DecimalField(max_digits=10, decimal_places=0)



class CattleForm(forms.ModelForm):
    class Meta:
        model = Cattle
        fields = '__all__'
