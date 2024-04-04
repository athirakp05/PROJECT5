# forms.py
from django import forms
from .models import Product,MilkSample

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['p_name', 'mfg_date', 'expiry_date', 'quantity', 'price', 'description', 'seller', 'categories', 'image']
        widgets = {
            'mfg_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class MilkCollectionForm(forms.ModelForm):
    class Meta:
        model = MilkSample
        fields = ['seller', 'milk_type', 'collection_date', 'collection_time', 'quantity', 'description','pH', 'temperature', 'taste', 'odor', 'fat', 'turbidity', 'color', 'grade']
        widgets = {
            'collection_date': forms.DateInput(attrs={'type': 'date'}),
        }

# class SampleTestReportForm(forms.ModelForm):
#     class Meta:
#         model = MilkSample
#         fields = ['pH', 'temperature', 'taste', 'odor', 'fat', 'turbidity', 'color', 'grade']