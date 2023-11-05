# views.py
from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm  # Import your ProductForm

CATEGORY_CHOICES = [
    ('Milk', 'Milk'),
    ('Curd', 'Curd'),
    ('Paneer', 'Paneer'),
    ('Ghee', 'Ghee'),
    ('Butter', 'Butter'),
    ('Cheese', 'Cheese'),
]
GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
]
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_add')
    else:
        form = ProductForm()

    categories = [choice for choice in CATEGORY_CHOICES]
    grade_level = [choice for choice in GRADE_CHOICES]

    return render(request, 'category/product_add.html', {'form': form, 'categories': categories})

def prod_view(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'category/prod_view.html', context)
