# views.py
from .models import Product
from .forms import ProductForm
from .models import MilkCollection,Wishlists
from .forms import MilkCollectionForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404  # Import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('prod_view')

    else:
        form = ProductForm()

    return render(request, 'category/product_add.html', {'form': form})

def prod_view(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'category/prod_view.html', context)



def product_detail(request):
    category = request.GET.get('category', None)

    if category:
        products = Product.objects.filter(categories=category)
    else:
        products = Product.objects.all()

    context = {'products': products}
    return render(request, 'category/product_detail.html', context)

def p_detail(request):
    if request.method == 'GET' and request.is_ajax():
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'category/p_detail.html', {'product': product})

    # Handle non-AJAX or invalid requests gracefully
    return HttpResponseBadRequest("Invalid request")
    
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


# def common_search(request):
#     if request.method=='GET':
#         query = request.GET.get('query','')
#         products=Product.objects.filter(Q(p_name__icontains=query))
#         context={
#         'products' : products,
#         }
#         return render(request,'category/product_detail.html',context)


@login_required
def wishlist(request):
    wishlist=Wishlists.objects.all()
    context={
    "wishlist":wishlist
    }
    return render(request, "category/wishlist.html",context)


from django.views.decorators.csrf import csrf_exempt

@login_required
def add_to_wishlist(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        wishlist_item = Wishlists.objects.filter(user=request.user, product=product).first()

        if wishlist_item:
            return JsonResponse({'message': 'Product already exists in your wishlist.'}, status=400)

        new_wishlist_item = Wishlists(user=request.user, product=product)
        new_wishlist_item.save()

        return JsonResponse({'message': 'Product added to your wishlist successfully.'})

    return JsonResponse({'message': 'Invalid request.'}, status=400)