# views.py
from .models import Product
from .forms import ProductForm
from .models import MilkCollection,Cart
from .forms import MilkCollectionForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404  # Import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q,F
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST
from farm.models import Seller  # Import the Seller model
from django.contrib import messages

@login_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = Seller.objects.get(user=request.user)  # Set the seller to the logged-in user's seller instance
            product.save()
            return redirect('prod_view')
    else:
        initial_data = {'seller': Seller.objects.get(user=request.user)}  # Prepopulate the seller field with the logged-in user's seller instance
        form = ProductForm(initial=initial_data)
    return render(request, 'category/product_add.html', {'form': form})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def prod_view(request):
    seller = Seller.objects.get(user=request.user)
    products_list = Product.objects.filter(seller=seller)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 10)  # Show 10 products per page
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
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

def add_milk_details(request):
    if request.method == 'POST':
        form = MilkCollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_milk_details')  # Redirect to the view all milk details page
    else:
        form = MilkCollectionForm()
    return render(request, 'admin/add_milk_detail.html', {'form': form})

def edit_milk_details(request, pk):
    milk_detail = MilkCollection.objects.get(pk=pk)
    if request.method == 'POST':
        form = MilkCollectionForm(request.POST, instance=milk_detail)
        if form.is_valid():
            form.save()
            return redirect('admindash')  # Redirect to the view all milk details page
    else:
        form = MilkCollectionForm(instance=milk_detail)
    return render(request, 'admin/edit_milk_details.html', {'form': form})

def all_milk_details(request):
    all_milk_details = MilkCollection.objects.all()
    context = {'all_milk_details': all_milk_details}
    return render(request, 'admin/all_milk_details.html', context)

from django.contrib.auth import get_user_model

def view_carts(request):
    User = get_user_model()
    carts = Cart.objects.select_related('product', 'user').all()
    context = {'carts': carts}
    return render(request, 'admin/view_carts.html', context)

def own_milk_details(request):
    seller = request.user.seller  # Assuming the seller is linked to the user
    seller_milk_details = MilkCollection.objects.filter(seller=seller)
    context = {'seller_milk_details': seller_milk_details}
    return render(request, 'category/own_milk_details.html', context)


@login_required
def add_to_cart(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        p_code = request.POST.get('p_code')
        user = request.user
        # Check if the product is already in the cart for the user
        existing_product = Cart.objects.filter(user=user, product__p_code=p_code).exists()
        if existing_product:
            existing_product.quantity += 1
            existing_product.save()
        else:           
            product = get_object_or_404(Product, p_code=p_code)
            cart_item = Cart.objects.create(
                user=user,
                product=product,
                quantity=1  # You can adjust the quantity as needed
            )
            cart_item.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def view_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user) 
    context = {'cart_items': cart_items}
    return render(request, 'category/view_cart.html', context)

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id)
    cart_item.delete()
    messages.success(request, 'Product removed from cart.')
    return redirect('c_dashboard')

@login_required
@require_POST
def update_quantity(request):
    cart_id = request.POST.get('cart_id')
    quantity = int(request.POST.get('quantity'))

    cart_item = get_object_or_404(Cart, pk=cart_id)
    cart_item.quantity = quantity
    total_amount = cart_item.product.price * quantity
    cart_item.save()
    return JsonResponse({'total_amount': total_amount})

def search_products(request):
    query = request.GET.get('query', None)
    if query:
        products = Product.objects.filter(Q(p_name__icontains=query))
    else:
        products = Product.objects.all()
    context = {'products': products}
    return render(request, 'category/product_detail.html', context)



def payment(request):
    return render(request, 'category/payment.html')

def process_payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        return HttpResponse("Payment processed successfully!") 
    else:
        return HttpResponse("Invalid request method")
    
