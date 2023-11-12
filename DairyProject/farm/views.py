from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import render, redirect,HttpResponse
from .models import CustomUser, Customer, Seller
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.models import Permission
from .forms import CustomerRegistrationForm, SellerRegistrationForm,SellerProfileForm
from .models import Cattle,Login_Details,SellerEditProfile
from .forms import CattleForm, CattleVaccinationForm, CattleInsuranceForm

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
                return redirect("a_dashboard")  # Redirect to the admin dashboard
            elif user.role == 'Customer':
                messages.success(request, "Login successful!")
                return redirect("c_dashboard")  # Redirect to the customer dashboard
            elif user.role == 'Seller':
                messages.success(request, "Login successful!")
                return redirect("s_dashboard")  # Redirect to the seller dashboard
            else:
                # Handle unknown or unsupported roles here
                messages.error(request, "Unknown user role or unsupported role.")
    
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

        if Login_Details.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user = CustomUser.objects.create_user(email=email, password=password, role='Customer')
            customer = Customer(user=user, first_name=firstname, last_name=lastname, mobile=mobile)
            customer.save()
            # Save login details to the Login model
            login = Login_Details(email=email, password=password, role='Customer')
            login.save()
            messages.success(request, "Registered successfully")
            return redirect("login")  # Redirect to the registration page
    
    return render(request, 'c_register.html')


# Seller registration view

def s_register(request):
    if request.method == "POST":
        # Retrieve seller registration data
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        farmer_license = request.POST.get('farmer_license')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        if Seller.objects.filter(farmer_license=farmer_license).exists():
            messages.error(request, "Seller with this farmer license already exists. Please use a different license.")
            return redirect("s_register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user = CustomUser.objects.create_user(email=email, password=password,role='Seller')
            seller = Seller(user=user, first_name=firstname, last_name=lastname,farmer_license=farmer_license,  mobile=mobile)
            seller.save()
            # Save login details to the Login model
            login = Login_Details(email=email, password=password, role='Seller')
            login.save()
            messages.success(request, "Registered successfully")
            return redirect("login")  # Redirect to the registration page
    
    return render(request, 's_register.html')

@login_required(login_url='login')
def s_profile(request):
    # Assuming the seller profile is associated with the logged-in user
    seller_profile = SellerEditProfile.objects.get(user=request.user)

    context = {
        'seller_profile': seller_profile,
    }
    return render(request, 'profile_edit/s_profile.html', context)

@login_required(login_url='login')  
@user_passes_test(lambda u: u.is_seller, login_url='login')  
def complete_prof(request):
    seller_profile = SellerEditProfile.objects.get(user=request.user.seller.user)

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)

        if form.is_valid():
            form.save()
            return redirect('s_profile')
    else:
        form = SellerProfileForm(instance=seller_profile, seller_profile=seller_profile)

    return render(request, 'profile_edit/complete_prof.html', {'form': form})
def logout(request):
    auth_logout(request)
    return redirect('home')
    
def a_dashboard(request):
    if 'email' in request.session:
        response = render(request, 'dash/a_dashboard.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('home')

def c_dashboard(request):
    if 'email' in request.session:
        response = render(request, 'dash/c_dashboard.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('home')
def s_dashboard(request):
    if 'email' in request.session:
        user = request.user
        seller_profile, created = SellerEditProfile.objects.get_or_create(user=user.seller.user)
        context = {
            'seller_profile': seller_profile,
        }

        return render(request, 'dash/s_dashboard.html', context)
        response['Cache-Control'] = 'no-store, must-revalidate'

    else:
        return redirect('home')
# def s_dashboard(request):
#     if 'email' in request.session:
#         response = render(request, 'dash/s_dashboard.html')
#         response['Cache-Control'] = 'no-store, must-revalidate'
#         return response
#     else:
#         return redirect('home')


# views.py

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
    context = {
        'admin': admin,
    }

    return render(request, 'profile.html', context)

def select(request):
    return render(request, 'select.html')
    



def add_cattle(request):
    if request.method == 'POST':
        form = CattleForm(request.POST, request.FILES)
        if form.is_valid():
            cattle = form.save(commit=False)  # Create an instance without saving to the database
            cattle.seller = request.user.seller  # Set the seller to the currently logged-in user
            cattle.save()  # Save the cattle object
            return redirect('view_cattle')
    else:
        form = CattleForm()
    
    return render(request, 'cattle/add_cattle.html', {'form': form})
def edit_cattle(request):
    if request.method == 'POST':
        # Retrieve the selected farmer_license from the form
        farmer_license = request.POST.get('farmer_license')
        cattle = Cattle.objects.get(farmer_license=farmer_license)

        form = CattleForm(request.POST, request.FILES, instance=cattle)
        vacc_form = CattleVaccinationForm(instance=cattle)
        insur_form = CattleInsuranceForm(instance=cattle)

        if form.is_valid():
            form.save()

        if 'vaccination' in request.POST:
            vacc_form = CattleVaccinationForm(request.POST, instance=cattle)
            if vacc_form.is_valid():
                vacc_form.save()

        if 'insurance' in request.POST:
            insur_form = CattleInsuranceForm(request.POST, instance=cattle)
            if insur_form.is_valid():
                insur_form.save()

        return redirect('view_cattle')

    else:
        # Retrieve a list of available cattle for the dropdown
        cattle_list = Cattle.objects.all()
        return render(request, 'cattle/edit_cattle.html', {'cattle_list': cattle_list})


def view_cattle(request):
    if request.user.is_authenticated:
        user = request.user
        cattle_list = Cattle.objects.filter(seller__user=user)  # Assuming seller is related to Cattle
        print(cattle_list)  # Add this line for debugging
        return render(request, 'cattle/view_cattle.html', {'cattle_list': cattle_list})
    else:
        return render(request, 'cattle/view_cattle.html', {'cattle_list': []})
     
def delete_cattle(request, cattle_id):
    cattle = get_object_or_404(Cattle, farmer_license=cattle_id)
    if request.method == 'POST':
        cattle.delete()
        return redirect('view_cattle')

    return render(request, 'cattle/delete_cattle.html', {'cattle': cattle})

def common_search(request):
        firstname = request.GET.get('name')
        if firstname is not None:
            results = Seller.objects.filter(firstname=firstname)  # Replace 'name' with the actual field you want to search
            return render(request, 'search_results.html', {'results': results})
    # If no search term provided, return to the dashboard or another appropriate page
        return redirect('a_dashboard') 
    
def contact(request):
    # Add your view logic here
    return render(request, 'contact.html')
def about(request):
    # Add your view logic here
    return render(request, 'about.html')