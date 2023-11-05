
from django import forms
from .models import Cattle

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
    cattle_license = forms.CharField(max_length=50)  # Add the cattle_license field

class CattleRegistrationForm(forms.ModelForm):
    class Meta:
        model = Cattle
        fields = '__all__'
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
        model = Cattle
        fields = '__all__'

class CattleInsuranceForm(forms.ModelForm):
    class Meta:
        model = Cattle
        fields = '__all__'