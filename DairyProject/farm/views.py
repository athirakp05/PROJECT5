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

            if user.role == 'Admin':
                messages.success(request, "Login successful!")
                return redirect("a_dashboard")
            elif user.role == 'Customer':
                messages.success(request, "Login successful!")
                return redirect("c_dashboard")
            elif user.role == 'Seller':
                messages.success(request, "Login successful!")
                return redirect("s_dashboard")
    
    # Handle login failure
    messages.error(request, "Login failed. Please check your credentials.")
    return render(request, 'login.html')

# Customer registration view
def c_register(request):
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
            user = CustomUser.objects.create_user(email=email, password=password, role='Customer')
            customer = Seller(user=user, first_name=firstname, last_name=lastname, mobile=mobile)
            customer.save()
            messages.success(request, "Registered successfully")
            showAlert("Registered successfully");
            return redirect("login")  # Redirect to the login page

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
            return redirect("s_register")  # Redirect to the registration page


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
# views.py
from .models import Seller, Customer

# Other views
def s_view(request):
    sellers = Seller.objects.all()
    print(sellers)  # Add this line for debugging
    return render(request, 'view/s_view.html', {'sellers': sellers})

# Add a view to display customers
def c_view(request):
    customers = Customer.objects.all()
    print(customers)  # Add this line for debugging
    return render(request, 'view/c_view.html', {'customers': customers})

    
def profile(request):
    admin = CustomUser.objects.get(id=request.user.id)  # Assuming you have an 'id' field for the user

    # You can customize this based on your user model and how you store profile information
    context = {
        'admin': admin,
    }

    return render(request, 'profile.html', context)