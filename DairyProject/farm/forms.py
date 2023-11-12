from django.core.validators import RegexValidator
from django import forms
from .models import Cattle,Insurance,Vaccination,SellerEditProfile

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
    mobile = forms.CharField(max_length=15)
    farmer_license = forms.CharField(max_length=7, validators=[
        RegexValidator(
            regex=r'^F\d{5}$',
            message='Seller license must be in the format FXXXXX, where X is a digit (0-9).',
        ),
    ])


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerEditProfile
        fields = ['first_name', 'last_name', 'house_name', 'city', 'pin_code', 'occupation', 'gender', 'dob',
                  'rationcard_no', 'email', 'mobile', 'acc_no', 'society', 'profile_photo', 'farmer_license']

    def __init__(self, *args, **kwargs):
        # Get the logged-in user's seller profile
        seller_profile = kwargs.pop('seller_profile', None)
        super().__init__(*args, **kwargs)

        if seller_profile:
            # Set initial values for specific fields from the seller's profile
            self.fields['first_name'].initial = seller_profile.first_name
            self.fields['last_name'].initial = seller_profile.last_name
            self.fields['email'].initial = seller_profile.email
            self.fields['mobile'].initial = seller_profile.mobile

            # Disable these fields to prevent modification
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['last_name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['mobile'].widget.attrs['readonly'] = True
class CattleForm(forms.ModelForm):
    class Meta:
        model = Cattle
        fields = '__all__'
        widgets = {
            'vaccination': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'insurance': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        }

class CattleVaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = '__all__'


class CattleInsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = '__all__'