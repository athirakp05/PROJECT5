# forms.py

from django import forms
from .models import DeliveryBoy, DeliveryBoyEdit

# forms.py
from django import forms
from .models import DeliveryBoy

# farm/forms.py
from django import forms
from .models import DeliveryBoy

class DeliveryBoyRegistrationForm(forms.ModelForm):
    class Meta:
        model = DeliveryBoy
        fields = ['name', 'mobile', 'email', 'driving_license']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmpassword = cleaned_data.get("confirmpassword")

        if password and confirmpassword and password != confirmpassword:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class DeliveryBoyEditForm(forms.ModelForm):
    class Meta:
        model = DeliveryBoyEdit
        fields = ['house_name', 'city', 'pin_code', 'gender', 'age', 'email', 'mobile', 'profile_photo', 'driving_license']
        widgets = {
            'profile_photo': forms.ClearableFileInput(),
            'driving_license': forms.ClearableFileInput(),
        }

from .models import ApprovalRequest
class DeliveryBoyApprovalForm(forms.ModelForm):
    class Meta:
        model = ApprovalRequest
        fields = ['is_approved']
