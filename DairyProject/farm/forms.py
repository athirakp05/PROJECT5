from django.core.validators import RegexValidator
from django import forms
from .models import Cattle,Insurance,Vaccination,SellerEditProfile,Breed, CattleType
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

class SellerEditProfileForm(forms.ModelForm):
    class Meta:
        model = SellerEditProfile
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('---', '---'), ('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]),
        }
class BreedForm(forms.ModelForm):
    class Meta:
        model = Breed
        fields = ['cattle_type', 'name', 'status']
class CattleForm(forms.ModelForm):
    class Meta:
        model = Cattle
        exclude = ['user', 'seller']
        widgets = {
            'CattleType': forms.Select(),
            'BreedName': forms.Select(),
            'feed': forms.Select(choices=[('Wheat','Wheat',),('Soya hull','Soya hull',),('Hay','Hay',),('Rice Bran','Rice Bran',),('Corn','Corn',),('Maize','Maize',),('Pellete','Pellete',)]),
        }

class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        exclude = ['cattle']

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        exclude = ['cattle']