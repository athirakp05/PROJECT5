from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['p_name', 'mfg_date', 'expiry_date', 'grade_level', 'quantity', 'price', 'Description', 'seller', 'categories', 'image']

