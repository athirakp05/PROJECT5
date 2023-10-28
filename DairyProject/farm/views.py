from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser, Customer, Seller
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Permission
from .forms import CustomerRegistrationForm, SellerRegistrationForm

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

            if user.role == 'Admin':
                return redirect("a_dashboard")
            elif user.role == 'Customer':
                return redirect("c_dashboard")
            elif user.role == 'Seller':
                return redirect("s_dashboard")

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response
# views.py
# Import necessary modules and models

# Customer registration view
def c_register(request):
    if request.method == "POST":
        # Retrieve customer registration data
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        # Validate and save customer registration data
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            # Create a user with the role 'Customer'
            user = CustomUser.objects.create_user(email=email, password=password, role='Customer')
            customer = Customer(user=user, first_name=firstname, last_name=lastname, phone=phone)
            customer.save()
            messages.success(request, "Registered successfully")
            return redirect("loginn")  # Redirect to the login page

    return render(request, 'c_register.html')

# Seller registration view
def s_register(request):
    if request.method == "POST":
        # Retrieve seller registration data
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        # Validate and save seller registration data
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            # Create a user with the role 'Seller' and save first name, last name, and mobile
            user = CustomUser.objects.create_user(email=email, password=password, role='Seller')
            seller = Seller(user=user, first_name=firstname, last_name=lastname, mobile=mobile)
            seller.save()
            messages.success(request, "Registered successfully")
            return redirect("s_register")  # Redirect to the login page

    return render(request, 's_register.html')
def logout(request):
    auth_logout(request)
    return redirect('home')

def c_dashboard(request):
    if 'email' in request.session:
        response = render(request, 'dash/c_dashboard.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('home')

#@user_passes_test(lambda u: u.is_authenticated and u.is_seller)
def s_dashboard(request):
    if 'email' in request.session:
        response = render(request, 'dash/s_dashboard.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('home')

# Admin dashboard view
#@user_passes_test(lambda u: u.is_authenticated and u.is_admin)
def a_dashboard(request):
    if 'email' in request.session:
        response = render(request, 'dash/a_dashboard.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('home')
