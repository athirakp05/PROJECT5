# views.py
import razorpay
from .models import Order, Payment, Product
from .forms import ProductForm, SampleTestReportForm
from .models import MilkCollection,Cart
from .forms import MilkCollectionForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404  # Import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Sum,F
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from farm.models import CustomerEditProfile, DeliveryBoy, Seller  # Import the Seller model
from django.contrib import messages
from django.db import transaction

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
    if request.method == 'POST':
        p_code = request.POST.get('p_code')
        product = get_object_or_404(Product, p_code=p_code)
        if product.quantity > 0:  # Check if the product is available
            user = request.user
            cart, created = Cart.objects.get_or_create(user=user, product=product)
            cart.quantity += 1
            cart.total_price = cart.quantity * product.price  # Update total price based on quantity and product price
            cart.save()
            product.quantity -= 1
            product.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Product out of stock.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})


@login_required
@require_POST
def update_quantity(request, cart_item_id, action):
    cart_item = get_object_or_404(Cart, pk=cart_item_id, user=request.user)
    if action == 'increase':
        if cart_item.product.quantity > cart_item.quantity:
            cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()  # Remove the item if the quantity becomes zero
    cart_item.total_price = cart_item.quantity * cart_item.product.price  # Update total price based on quantity and product price
    cart_item.save()    
    return redirect('view_cart')  # Redirect to the cart page

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)  # Change 'customer' to 'user'
    total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_price = cart_items.annotate(item_total=F('quantity') * F('product__price')).aggregate(Sum('item_total'))['item_total__sum'] or 0
    data = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }
    return render(request, 'category/view_cart.html', data)

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id)
    cart_item.delete()
    messages.success(request, 'Product removed from cart.')
    return redirect('view_cart')

def search_products(request):
    query = request.GET.get('query', None)
    if query:
        products = Product.objects.filter(Q(p_name__icontains=query))
    else:
        products = Product.objects.all()
    context = {'products': products}
    return render(request, 'category/product_detail.html', context)
def checkout(request):
    if request.method == 'POST':
        house_name = request.POST.get('house_name')
        city = request.POST.get('city')
        pin_code = request.POST.get('pin_code')
        phone_number = request.POST.get('phone_number')
        if not (house_name and city and pin_code and phone_number):
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('checkout')
        cart_items = Cart.objects.filter(user=request.user)
        total_price = cart_items.aggregate(Sum('total_price'))['total_price__sum'] or 0
        with transaction.atomic():
            order = Order.objects.create(user=request.user, house_name=house_name, city=city, pin_code=pin_code,phone_number=phone_number, total_price=total_price,delivery_status='Pending')           
            for cart_item in cart_items:
                order.cart.add(cart_item)
        return render(request, 'pay/payment.html', {'order': order})
    else:
        order = None  # Initialize order variable if it's a GET request
        return render(request, 'pay/checkout.html', {'order': order})

def payment(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        client = razorpay.Client(auth=("rzp_test_VsNzgoQtqip5Wd", "rcn7optyjJTyzOsFlhJQ6GYX"))
        total_price = int(order.total_price * 100)  # Convert total price to integer in paise
        data = {
            "amount": total_price,
            "currency": "INR",
            "receipt": f"order_rcptid_{order.id}"
        }
        payment = client.order.create(data)
        with transaction.atomic():
            payment_obj = Payment.objects.create(
                order=order,
                amount=order.total_price / 100,  # Convert back to rupees
                razorpay_order_id=payment['id'],
                transaction_id=payment['id'],  # Assuming transaction ID is same as razorpay order ID
                is_successful=True  # Assuming payment is always successful if reached this point
            )
            order.is_paid = True  # Mark the order as paid
            order.payment = payment_obj  # Associate payment with the order
            order.save()
            payment_obj.save()
            return redirect('success', order_id=order.id)
    else:
        return render(request, 'pay/payment.html', {'order': order})

def success(request, order_id):
    order = Order.objects.get(id=order_id)
    payments = order.payments.all()  # Retrieve all payments associated with the order
    return render(request, 'pay/success.html', {'order': order, 'payments': payments})

def update_delivery_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('new_status') 
        if request.user.is_authenticated and hasattr(request.user, 'deliveryboy'):
            delivery_boy = request.user.deliveryboy
            if order.delivery_boy == delivery_boy and new_status == 'Delivered':
                order.delivery_status = new_status
                order.delivery_boy_id = delivery_boy.id  # Save the delivery boy's ID to the order
                order.save()
                messages.success(request, 'Delivery status updated successfully.')
    return redirect('order')

def payment_history(request):
    orders = Order.objects.filter(user=request.user)
    payment_history = []
    for order in orders:
        for payment in order.payments.all():
            payment_history.append({
                'order': order,
                'payment': payment,
                'products': order.cart.all()  # Retrieve products associated with the order
            })
    return render(request, 'pay/payment_history.html', {'payment_history': payment_history})

def order_history(request):
    all_orders = Order.objects.all().order_by('-created_at')
    date_filter = request.GET.get('date')
    if date_filter:
        try:
            date_filter = datetime.strptime(date_filter, '%Y-%m-%d').date()
            all_orders = all_orders.filter(created_at__date=date_filter)
        except ValueError:
            pass
    paginator = Paginator(all_orders, 10)
    page_number = request.GET.get('page')
    try:
        orders = paginator.page(page_number)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context = {
        'orders': orders,
        'date_filter': date_filter,
    }
    return render(request, 'del/order_history.html', context)
def order(request):
    if request.user.is_authenticated and hasattr(request.user, 'deliveryboy'):
        delivery_boy = request.user.deliveryboy
        assigned_orders = Order.objects.filter(delivery_status='Pending').order_by('created_at')
        delivery_boy_count = DeliveryBoy.objects.filter(is_approved=True).count()
        total_orders = assigned_orders.count()
        orders_per_delivery_boy = total_orders // delivery_boy_count
        remainder_orders = total_orders % delivery_boy_count
        if delivery_boy.id <= remainder_orders:
            orders_to_take = orders_per_delivery_boy + 1
        else:
            orders_to_take = orders_per_delivery_boy
        start_index = (delivery_boy.id - 1) * orders_per_delivery_boy + min(delivery_boy.id, remainder_orders)
        end_index = start_index + orders_to_take
        my_orders = assigned_orders[start_index:end_index]
        
        # Allocate orders to the delivery boy one by one
        for order in my_orders:
            order.delivery_boy = delivery_boy  # Save the delivery boy's ID to the order
            order.save()

        page = request.GET.get('page', 1)
        paginator = Paginator(my_orders, 10)  # Show 10 orders per page

        try:
            my_orders = paginator.page(page)
        except PageNotAnInteger:
            my_orders = paginator.page(1)
        except EmptyPage:
            my_orders = paginator.page(paginator.num_pages)      
        
        context = {
            'delivery_boy': delivery_boy,
            'my_orders': my_orders,
        }
        return render(request, 'del/order.html', context)

    
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