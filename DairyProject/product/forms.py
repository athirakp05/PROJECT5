from django import forms
from .models import p_Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = p_Category
        fields = ['category']  # Define the fields you want to include in the form

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['p_name', 'mfg_date', 'expiry_date', 'grade_level', 'quantity', 'price', 'category', 'image']
