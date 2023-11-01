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
from .models import SellerEditProfile
from .forms import SellerProfileEditForm,CattleForm  # Import your SellerProfileEditForm
from .models import CattleType


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

def s_prof_edit(request, user_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    # Check if the user object is available and has the correct user_id
    if request.user.id != user_id:
        raise Http404("User does not exist or you don't have permission to edit this profile.")
    # Get the current user
    user = request.user

    # Check if a SellerEditProfile object exists for the user
    try:
        seller_profile = SellerEditProfile.objects.get(user=user)
    except SellerEditProfile.DoesNotExist:
        # If it doesn't exist, create a new SellerEditProfile object
        seller_profile = SellerEditProfile(user=user)

    if request.method == 'POST':
        form = SellerProfileEditForm(request.POST, request.FILES, instance=seller_profile)
        if form.is_valid():
            form.save()  # This should save the pin_code as well
            return redirect('s_view')  # Redirect to a success page or another appropriate URL
    else:
        form = SellerProfileEditForm(instance=seller_profile)

    return render(request, 'profile_edit/s_prof_edit.html', {'form': form})


    
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
    
def add_cattle(request):
    if request.method == 'POST':
        form = CattleForm(request.POST, request.FILES)

        if form.is_valid():
            # Create and save the cattle object
            cattle = form.save(commit=False)

            # Get the selected cattle type and breed name from the form
            cattle_type = request.POST.get('cattle_type')
            breed_name = request.POST.get('breed_name')

            # Retrieve the cattle type and breed objects from the database
            cattle_type_obj = cattleType.objects.get(cattle_type=cattle_type)
            breed_obj = Breed.objects.get(breed_name=breed_name)

            # Set the cattle type and breed for the cattle object
            cattle.cattle_type = cattle_type_obj
            cattle.breed_name = breed_obj

            # Fetch health status options from the Health table
            health_status_options = Health.objects.values_list('health_status', flat=True).distinct()

            cattle.save()
            return redirect('add_cattle')
    else:
        form = CattleForm()

        # Retrieve cattle types from the database
        cattle_types = cattleType.objects.all()

        # Initialize health status options as empty
        health_status_options = []

    return render(request, 'cattle_details/add_cattle.html', {'form': form, 'cattle_types': cattle_types, 'health_status_options': health_status_options})

def cattle_view(request, user_id):
    # Retrieve the specific seller using the provided user_id
    seller = get_object_or_404(CustomUser, id=user_id, role='Seller')

    # Retrieve the cattles associated with the seller
    seller_cattles = Cattle.objects.filter(seller=seller)

    # Pass the seller and their cattles to the template
    context = {
        'seller': seller,
        'seller_cattles': seller_cattles,
    }

    # Render the cattle_view.html template with the context data
    return render(request, 'cattle_details/cattle_view.html', context)

    
    