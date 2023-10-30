from django.shortcuts import render, redirect
from .models import p_Category,Product  # Import your Category model
from .forms import CategoryForm
from .forms import ProductForm  # Create a Django form for adding products

def cat_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('cat_add')  # Redirect to a category list view
    else:
        form = CategoryForm()

    return render(request, 'category/cat_add.html', {'form': form})



def product_add(request):
    categories = p_Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_add')
    else:
        form = ProductForm()

    return render(request, 'category/product_add.html', {'form': form, 'categories': categories})


def prod_view(request):
    products = Product.objects.all()
    return render(request, 'category/prod_view.html', {'products': products})
