# views.py

from django.contrib import admin
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import CustomUser, Customer, Seller
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import SellerForm
from .utils import generate_random_password
from django.db import transaction


def index(request):
    return render(request, 'index.html')

def loginn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            request.session['email'] = email
            messages.success(request, "Login successful!")

            if user.is_superuser:
                return redirect("admin_dashboard")
            elif user.is_customer:
                return redirect("c_dashboard")
            elif user.is_seller:
                return redirect("s_dashboard")
        else:
            messages.error(request, "Invalid login credentials")

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response

def registration(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user = CustomUser.objects.create_user(email=email, password=password, role='Customer', phone=phone)
            user.is_customer = True
            user.save()

            customer = Customer(user=user, firstname=firstname, lastname=lastname, phone=phone)
            customer.save()

            messages.success(request, "Registered successfully")
            return redirect("login")
    return render(request, 'registration.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def logout(request):
    # Clear the session
    request.session.clear()
    # Log out the user (if using Django's built-in authentication)
    auth_logout(request)
    return redirect('home')

def c_dashboard(request):
    if 'email' in request.session:
        response = render(request, 'c_dashboard.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('home')

def admin_dashboard(request):
    # Set a session variable to indicate admin login
    request.session['admin_logged_in'] = True
    return render(request, 'admin_dashboard.html')


def s_dashboard(request):
    # Your view code here
    return render(request, 's_dashboard.html')
from django.shortcuts import render
from .models import Seller

def view_sellers(request):
    sellers = Seller.objects.all()
    return render(request, 'view_sellers.html', {'sellers': sellers})
from django.shortcuts import render
from .models import Customer

def view_customers(request):
    customers = Customer.objects.all()
    return render(request, 'view_customers.html', {'customers': customers})

class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'  # Create an HTML template for displaying customer details
    context_object_name = 'customers'  # The variable name to use in the template

class SellerListView(ListView):
    model = Seller
    template_name = 'seller_list.html'  # Create an HTML template for displaying seller details
    context_object_name = 'sellers'  # The variable name to use in the template
from django.shortcuts import render
from .models import Customer

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})
from django.shortcuts import render
from .models import Customer

def seller_list(request):
    sellers = Seller.objects.all()
    return render(request, 'seller_list.html', {'sellers': sellers})

from .forms import SellerForm

def seller_login_details(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    # You can retrieve and display seller's login details here
    return render(request, 'seller_login_details.html', {'seller': seller})

def delete_seller(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    seller.delete()
    return redirect('seller-list')
from django.shortcuts import render, redirect
from .forms import SellerForm
from django.db import transaction

def add_seller(request):
    if request.method == "POST":
        seller_form = SellerForm(request.POST)
        if seller_form.is_valid():
            # Form is valid, save the data
            seller = seller_form.save()
            # You can also send a success message here if needed
            return redirect('seller-list')  # Redirect to the seller list page
        else:
            # Form is invalid, handle errors
            print(seller_form.errors)  # Print validation errors for debugging
            # Return the form with errors to the user
            return render(request, 'add_seller.html', {'seller_form': seller_form})
    else:
        seller_form = SellerForm()

    return render(request, 'add_seller.html', {'seller_form': seller_form})
def c_delete(request, customer_id):
    # Retrieve the customer to be deleted
    customer = get_object_or_404(Customer, id=customer_id)

    # Delete the customer
    customer.delete()

    # Redirect back to the customer list page
    return redirect('customer_list')

def update_s(request, seller_id):
    seller = get_object_or_404(Seller, pk=seller_id)

    if request.method == 'POST':
        form = SellerForm(request.POST, instance=seller)
        if form.is_valid():
            form.save()
            return redirect('seller_list')

    else:
        form = SellerForm(instance=seller)

    return render(request, 'update_s.html', {'form': form, 'seller': seller})
def delete_s(request, seller_id):
    seller = get_object_or_404(Seller, pk=seller_id)
    if request.method == 'POST':
        seller.delete()
        return redirect('seller_list')

    return render(request, 'delete_s.html', {'seller': seller})

