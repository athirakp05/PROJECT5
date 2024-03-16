# views.py
import razorpay
from requests import request
from .models import Order, Payment, Product
from .forms import AddressConfirmationForm, ProductForm, SampleTestReportForm
from .models import MilkCollection,Cart
from .forms import MilkCollectionForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404  # Import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Sum,F
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_POST
from farm.models import CustomUser, CustomerEditProfile, Seller  # Import the Seller model
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

from datetime import date, timezone
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
    cart_items = Cart.objects.all()
    cart_data = [
        {
            'id': item.id,
            'product_name': item.product.p_name,
            'user_name': item.user.username,
        }
        for item in cart_items
    ]
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(cart_data, safe=False)
    return render(request, 'admin/view_carts.html', {'cart_data': cart_data})

def own_milk_details(request):
    seller = request.user.seller  # Assuming the seller is linked to the user
    seller_milk_details = MilkCollection.objects.filter(seller=seller)
    context = {'seller_milk_details': seller_milk_details}
    return render(request, 'category/own_milk_details.html', context)


@login_required
def add_to_cart(request, p_code):
    product = get_object_or_404(Product, pk=p_code)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, 'Product quantity updated in the cart.')
    else:
        messages.success(request, 'Product added to cart.')
        return redirect('view_cart')
    
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_price = cart_items.annotate(item_total=F('quantity') * F('product__price')).aggregate(Sum('item_total'))['item_total__sum'] or 0
    total_price_in_paise = int(total_price * 100)
    data = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'sum': total_price_in_paise
    }
    if request.method == 'POST':
        client = razorpay.Client(auth=("rzp_test_VsNzgoQtqip5Wd", "rcn7optyjJTyzOsFlhJQ6GYX"))
        data = {
            "amount": total_price_in_paise,
            "currency": "INR",
            "receipt": "order_rcptid_11"
        }
        payment = client.order.create(data)
    return render(request, 'category/view_cart.html', data)

@login_required
def remove_from_cart(request, p_code):
    cart_item = get_object_or_404(Cart, product__p_code=p_code, user=request.user)
    cart_item.delete()
    messages.success(request, 'Product removed from cart.')
    return redirect('view_cart')

@login_required
@require_POST
def update_quantity(request, cart_item_id, action):
    cart_item = get_object_or_404(Cart, pk=cart_item_id, user=request.user)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete() 
    cart_item.save()
    return redirect('view_cart') 

@login_required
def payment(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.total_price for item in cart_items)
        client = razorpay.Client(auth=('rzp_test_VsNzgoQtqip5Wd', 'rcn7optyjJTyzOsFlhJQ6GYX'))
        order_params = {
           'amount': int(total_price * 100),
            'currency': 'INR',
            'payment_capture': '1',
            'receipt': f'order_rcptid_{request.user.id}',  # Using user ID in the receipt for uniqueness
        }
        order = client.order.create(order_params)
        order_instance, created = Order.objects.get_or_create(
            user=request.user,
            defaults={
                'delivery_status': 'Pending',
            }
        )
        payment = Payment.objects.create(
            user=request.user,
            order=order_instance,
            amount=total_price,
        )
        return render(request, 'pay/payment.html', {'order': order, 'cart_items': cart_items})
    return render(request, 'pay/payment.html') 

@csrf_exempt
def success(request):
    if request.method == 'POST':
        order_id = request.POST.get('razorpay_order_id')
        try:
            order_instance = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return HttpResponseNotFound("Order not found")
        
        payment_id = request.POST.get('razorpay_payment_id')
        client = razorpay.Client(auth=('rzp_test_VsNzgoQtqip5Wd', 'rcn7optyjJTyzOsFlhJQ6GYX'))
        payment_status = client.payment.fetch(payment_id)['status']
        if payment_status == 'captured':
            order_instance.delivery_status = 'Delivered'
            order_instance.transaction_id = payment_id  
            order_instance.save()
            payment, created = Payment.objects.get_or_create(order=order_instance)
            payment.transaction_id = payment_id
            payment.is_paid = True
            payment.save()
            Cart.objects.filter(user=request.user).delete()
            return render(request, 'pay/success.html')
        else:
            payment, created = Payment.objects.get_or_create(order=order_instance)
            payment.transaction_id = payment_id
            payment.is_paid = False  
            payment.save()
            return HttpResponse("Payment Failed! Please try again or contact support.")
    else:
        return HttpResponse("Invalid Request")
def order_history(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-order_date')
    order_history = []
    for order in user_orders:
        payment = Payment.objects.filter(order=order).first()
        payment_status = "Payment Pending"  # Default to "Payment Pending"
        if payment and payment.order.order_id == order.order_id:
            payment_status = "Payment Completed"
        city = order.city
        house_name = order.house_name
        pincode = order.pincode
        product_name = order.items.first().product.p_name if order.items.exists() else "N/A"
        user_info = CustomerEditProfile.objects.filter(user_id=request.user.id).first()
        user_name = user_info.first_name + " " + user_info.last_name if user_info else "N/A"
        user_phone = user_info.mobile if user_info else "N/A"
        user_address = f"{house_name}, {city}, {pincode}" if house_name and city and pincode else "N/A"
        order_history.append((order, payment_status, product_name, user_name, user_phone, user_address))
    context = {'order_history': order_history}
    return render(request, 'pay/order_history.html', context)

def payment_history(request):
    user = request.user
    payments = Payment.objects.filter(user=user)
    return render(request, 'pay/payment_history.html', {'payments': payments})

def search_products(request):
    query = request.GET.get('query', None)
    if query:
        products = Product.objects.filter(Q(p_name__icontains=query))
    else:
        products = Product.objects.all()
    context = {'products': products}
    return render(request, 'category/product_detail.html', context)


def sample_report(request):
    return render(request, 'category/sample_report.html')


def address_confirmation(request):
    if request.method == 'POST':
        form = AddressConfirmationForm(request.POST)
        if form.is_valid():
            address_confirmation = form.save(commit=False)
            address_confirmation.user = request.user  
            address_confirmation.save()
            return redirect('payment')  
    else:
        form = AddressConfirmationForm()
    return render(request, 'pay/address_confirmation.html', {'form': form})

@login_required
def del_order_history(request):
    if not request.user.is_delivery_boy:
        return HttpResponseForbidden("You are not authorized to view this page.")

    orders = Order.objects.all().order_by('-order_date').select_related('user')
    context = {'orders': orders}
    return render(request, 'del/del_order_history.html', context)

@require_POST
def update_delivery_status(request, order_id):
    if not request.user.is_delivery_boy:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    order = Order.objects.get(order_id=order_id)
    new_status = request.POST.get('delivery_status')
    order.delivery_status = new_status
    order.save()
    return redirect('del_order_history')

@login_required
def addSample_test(request):
    if request.method == 'POST':
        form = SampleTestReportForm(request.POST)
        if form.is_valid():
            sample_test = form.save(commit=False)
            sample_test.seller = request.user
            sample_test.save()
            messages.success(request, 'Sample test report added successfully.')
            return redirect('all_milk_details')  
        else:
            messages.error(request, 'Error in the form submission. Please check the data.')
    else:
        form = SampleTestReportForm()

    context = {'form': form}
    return render(request, 'admin/addSample_test.html', context)

def milk_parameters(request):
    return render(request, 'other/milk_parameters.html')