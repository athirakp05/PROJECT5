# forms.py

from django import forms
from .models import DeliveryBoy, DeliveryBoyEdit

class DeliveryBoyRegistrationForm(forms.ModelForm):
    class Meta:
        model = DeliveryBoy
        fields = ['name', 'mobile', 'email', 'driving_license']  # Include the correct fields from DeliveryBoy model

class DeliveryBoyEditForm(forms.ModelForm):
    class Meta:
        model = DeliveryBoyEdit
        fields = ['house_name', 'city', 'pin_code', 'gender', 'age', 'email', 'mobile', 'profile_photo', 'driving_license']
        widgets = {
            'profile_photo': forms.ClearableFileInput(),
            'driving_license': forms.ClearableFileInput(),
        }
