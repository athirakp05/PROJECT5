# views.py
import razorpay
from .models import Product
from .forms import ProductForm, SampleTestReportForm
from .models import MilkCollection,Cart
from .forms import MilkCollectionForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404  # Import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Sum,F
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from farm.models import CustomerEditProfile, Seller  # Import the Seller model
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
    products = Product.objects.all()
    date_filter = request.GET.get('date_filter')
    seller_filter = request.GET.get('seller_filter')
    product_name_filter = request.GET.get('product_name_filter')
    if date_filter:
        products = products.filter(upload_datetime__date=date_filter)
    if seller_filter:
        products = products.filter(seller__name=seller_filter)
    if product_name_filter:
        products = products.filter(p_name__icontains=product_name_filter)
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)  # Show 10 products per page
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'category/p_detail.html', {'products': products})
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

from datetime import date
from datetime import datetime

def all_milk_details(request):
    all_milk_details = MilkCollection.objects.all()
    sellers = Seller.objects.all()  # Fetch all sellers for the filter dropdown
    date_filter = request.GET.get('date')
    seller_filter = request.GET.get('seller')

    if date_filter:
        date_filter = datetime.strptime(date_filter, '%Y-%m-%d').date()
        all_milk_details = all_milk_details.filter(collection_date=date_filter)

    if seller_filter:
        all_milk_details = all_milk_details.filter(seller__name=seller_filter)

    context = {'all_milk_details': all_milk_details, 'sellers': sellers}
    return render(request, 'admin/all_milk_details.html', context)

@login_required
def admin_cart(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    # Get all cart items from the database
    all_cart_items = Cart.objects.all()

    context = {'all_cart_items': all_cart_items}
    return render(request, 'admin/admin_cart.html', context)

@login_required
def view_carts(request):
    customer = request.user
    cart_items = Cart.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price() for item in cart_items)

    # Convert cart_items to a list of dictionaries
    cart_data = [
        {
            'id': item.id,
            'product_name': item.product.p_name,
            'product_image': item.product.image.url if item.product.image else None,
            'user_name': item.user.email,
            'quantity': item.quantity,
            'total_amount': item.total_amount(),
            'created_at': item.created_at,
        }
        for item in cart_items
    ]
    
    context = {
        'cart_items': cart_data,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }
    
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(context, safe=False)
    
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
    # Get all cart items for the current user
    cart_items = Cart.objects.filter(customer=request.user)

    # Calculate total quantity by summing up quantities of all items
    total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    # Calculate total price by summing up the product of quantity and price for each item
    total_price = cart_items.annotate(item_total=F('quantity') * F('product__price')).aggregate(Sum('item_total'))['item_total__sum'] or 0
    total_price_in_paise = int(total_price * 100)

    # Prepare data dictionary
    data = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'sum': total_price_in_paise
    }

    if request.method == 'POST':
        # Integrate Razorpay payment logic here
        # Note: Ensure that you replace "your_key" and "your_secret" with your actual Razorpay key and secret
        client = razorpay.Client(auth=("rzp_test_VsNzgoQtqip5Wd", "rcn7optyjJTyzOsFlhJQ6GYX"))

        # You may need to modify the data dictionary based on your requirements
        data = {
            "amount": total_price_in_paise,
            "currency": "INR",
            "receipt": "order_rcptid_11"
        }

        payment = client.order.create(data)

    return render(request, 'view_cart.html', data)
@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id)
    cart_item.delete()
    messages.success(request, 'Product removed from cart.')
    return redirect('view_cart')

@login_required
@require_POST
def update_quantity(request, cart_item_id, action):
    cart_item = get_object_or_404(Cart, pk=cart_item_id, customer=request.user)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()  # Remove the item if the quantity becomes zero

    cart_item.save()

    return redirect('view_cart')  # Redirect to the cart page

def search_products(request):
    query = request.GET.get('query', None)
    if query:
        products = Product.objects.filter(Q(p_name__icontains=query))
    else:
        products = Product.objects.all()
    context = {'products': products}
    return render(request, 'category/product_detail.html', context)



def payment(request):
    if request.method == 'POST':
        amount = 50000  # Set your amount dynamically or as required
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_VsNzgoQtqip5Wd', 'rcn7optyjJTyzOsFlhJQ6GYX'))
        payment = client.order.create({'amount': amount, 'currency': order_currency, 'payment_capture': '1'})
        # Handle payment response
        return render(request, 'pay/payment.html', {'payment': payment})  # Render the payment HTML page with payment details
    return render(request, 'pay/payment.html')  


def success(request):
    return render(request, 'pay/success.html')

def process_payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        return HttpResponse("Payment processed successfully!") 
    else:
        return HttpResponse("Invalid request method")
    

def payment(request):
    if request.method == 'POST':
        user = request.user
        total_amount = Cart.objects.filter(user=user).aggregate(Sum('product__price'))['product__price__sum']
        
        if total_amount is None:
            # Set a default amount if there are no products in the cart
            total_amount = 0

        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_VsNzgoQtqip5Wd', 'rcn7optyjJTyzOsFlhJQ6GYX'))
        payment = client.order.create({'amount': total_amount * 100, 'currency': order_currency, 'payment_capture': '1'})
        # Handle payment response
        # Redirect to success page on successful payment
        return render(request, 'pay/payment.html', {'payment': payment,'total_amount': total_amount})
    return render(request, 'pay/payment.html')

def success(request):
    return render(request, 'pay/success.html')

def process_payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        return redirect('success')  # Redirect to success page on successful payment
    else:
        return HttpResponse("Invalid request method")
    
def sample_report(request):
    return render(request, 'category/sample_report.html')


@login_required
def addSample_test(request):
    if request.method == 'POST':
        form = SampleTestReportForm(request.POST)
        if form.is_valid():
            sample_test = form.save(commit=False)
            sample_test.seller = request.user
            sample_test.save()
            messages.success(request, 'Sample test report added successfully.')
            return redirect('all_milk_details')  # Redirect to the milk details page
        else:
            messages.error(request, 'Error in the form submission. Please check the data.')
    else:
        form = SampleTestReportForm()

    context = {'form': form}
    return render(request, 'admin/addSample_test.html', context)

def milk_parameters(request):
    return render(request, 'other/milk_parameters.html')