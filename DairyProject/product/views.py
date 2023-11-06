# views.py
from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_add')
    else:
        form = ProductForm()

    return render(request, 'category/product_add.html', {'form': form})

def prod_view(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'category/prod_view.html', context)
