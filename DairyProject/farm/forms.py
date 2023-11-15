from django.core.validators import RegexValidator
from django import forms
from .models import Cattle,Insurance,Vaccination,SellerEditProfile,Breed,CattleType
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
        fields = '__all__'
class SellerEditProfileForm(forms.ModelForm):
    class Meta:
        model = SellerEditProfile
        fields = ['first_name', 'last_name', 'house_name', 'city', 'pin_code', 'occupation', 'gender', 'dob', 'rationcard_no', 'email', 'mobile', 'acc_no', 'society', 'profile_photo', 'farmer_license']

class CattleForm(forms.ModelForm):
    class Meta:
        model = Cattle
        fields = '__all__'
class CattleRegistrationForm(forms.ModelForm):
    class Meta:
        model = Cattle
        fields = ['EarTagID', 'CattleType', 'BreedName', 'weight', 'height', 'Age', 'Colour', 'feed', 'milk_obtained', 'health_status', 'vaccination', 'insurance', 'photo']
        widgets = {
            'CattleType': forms.Select(attrs={'class': 'form-control'}),
            'BreedName': forms.Select(attrs={'class': 'form-control'}),
            # Add more widgets as needed
        }

    def __init__(self, *args, **kwargs):
        super(CattleRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['CattleType'].queryset = CattleType.objects.filter(status=True)
class CattleVaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = '__all__'


class CattleInsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = '__all__'