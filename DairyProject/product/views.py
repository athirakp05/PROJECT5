# views.py
from .models import Product
from .forms import ProductForm
from .models import MilkCollection
from .forms import MilkCollectionForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404  # Import get_object_or_404


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


def product_detail(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'category/product_detail.html', context)

def milk_details(request):
    if request.method == 'POST':
        form = MilkCollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('milk_view')
    else:
        form = MilkCollectionForm()
    context = {'form': form}
    return render(request, 'category/milk_details.html', {'form': form})


def milk_edit(request, pk):
    collection = get_object_or_404(MilkCollection, pk=pk)

    if request.method == "POST":
        form = MilkCollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return redirect('milk_list')
    else:
        form = MilkCollectionForm(instance=collection)

    return render(request, 'category/milk_edit.html', {'form': form, 'collection': collection})


def milk_list(request):
    collections = MilkCollection.objects.all()
    context = {'collections': collections}
    return render(request, 'category/milk_view.html', context)

def milk_view(request, pk):
    collection = MilkCollection.objects.get(pk=pk)
    context = {'collection': collection}
    return render(request, 'category/milk_view.html', context)