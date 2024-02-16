# forms.py
from django import forms
from .models import Product,MilkCollection

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['p_name', 'mfg_date', 'expiry_date', 'quantity', 'price', 'description', 'seller', 'categories', 'image']
        widgets = {
            'mfg_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MilkCollectionForm(forms.ModelForm):
    class Meta:
        model = MilkCollection
        fields = ['seller','milk_type', 'collection_date', 'collection_time', 'quantity', 'quality_test_report', 'price', 'description']
        widgets = {
            'collection_date': forms.DateInput(attrs={'type': 'date'}),
        }
class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

from .models import SampleTestReport
class SampleTestReportForm(forms.ModelForm):
    class Meta:
        model = SampleTestReport
        fields = '__all__'
