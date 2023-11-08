from django.core.validators import RegexValidator
from django import forms
from .models import Cattle,Insurance,Vaccination

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