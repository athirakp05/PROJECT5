from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import render, redirect,HttpResponse
from .models import CustomUser, Customer, Seller,CattleType
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.models import Permission
from .forms import CustomerRegistrationForm, SellerRegistrationForm,SellerEditProfileForm
from .models import Cattle,Login_Details,SellerEditProfile,Breed,Insurance,Vaccination
from .forms import CattleForm, VaccinationForm, InsuranceForm,SellerProfileForm,BreedForm
from django.shortcuts import render, redirect, get_object_or_404  # Import get_object_or_404

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
                return redirect("admindash")  # Redirect to the admin dashboard
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
            seller_edit_profile = SellerEditProfile(user=user, seller=seller, first_name=firstname, last_name=lastname, mobile=mobile, email=email, farmer_license=farmer_license)
            seller_edit_profile.save()
            # Save login details to the Login model
            login = Login_Details(email=email, password=password, role='Seller')
            login.save()
            messages.success(request, "Registered successfully")
            return redirect("login")  # Redirect to the registration page
    
    return render(request, 's_register.html')

@login_required(login_url='login')
def s_profile(request):
    # Get the logged-in user
    user = request.user

    # Check if the user is a seller
    if user.is_seller:
        # Retrieve the seller profile details from SellerEditProfile model
        seller_profile = SellerEditProfile.objects.get(user=user)

        return render(request, 'profile_edit/s_profile.html', {'seller_profile': seller_profile})
    else:
        # Redirect to a different page for non-seller users
        return redirect('home')  # Change 'home' to the appropriate URL for your home page

@login_required
def complete_s_profile(request):
    user = request.user
    seller_profile, created = SellerEditProfile.objects.get_or_create(user=user.seller.user)

    if request.method == 'POST':
        form = SellerEditProfileForm(request.POST, request.FILES, instance=seller_profile)
        if form.is_valid():
            form.save()
            return redirect('seller_profile')  # Replace 's_dashboard' with your desired redirect URL after profile completion
    else:
        form = SellerEditProfileForm(instance=seller_profile)
    return render(request, 'profile_edit/complete_s_profile.html', {'form': form})

def seller_profile(request):
    seller_profile = SellerEditProfile.objects.get(user=request.user.seller.user)
    return render(request, 'profile_edit/seller_profile.html', {'seller_profile': seller_profile})

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
def admindash(request):
    if 'email' in request.session:
        response = render(request, 'dash/admindash.html')
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
        seller_profile = SellerEditProfile.objects.get(user=user.seller.user)

        # Check if the form is submitted
        if request.method == 'POST':
            form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)
            if form.is_valid():
                form.save()
                # Redirect to a success page or stay on the current page
                return redirect('seller_profile')
        else:
            # Populate the form with the seller's data
            form = SellerProfileForm(instance=seller_profile)
        context = {
            'seller_profile': seller_profile,
            'form': form,
        }
        return render(request, 'dash/s_dashboard.html', context)
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
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

@login_required
def add_cattle(request):
    if request.method == 'POST':
        cattle_form = CattleForm(request.POST, request.FILES)
        vaccination_form = VaccinationForm(request.POST)
        insurance_form = InsuranceForm(request.POST)
        
        if cattle_form.is_valid():
            cattle = cattle_form.save(commit=False)
            cattle.user = request.user
            cattle.seller = request.user.seller
            if 'vaccination_checkbox' in request.POST:
                cattle.vaccination = True
            else:
                cattle.vaccination = False
            if 'insurance_checkbox' in request.POST:
                cattle.insurance = True
            else:
                cattle.insurance = False
            cattle.save()
            
            if 'vaccination_checkbox' in request.POST:
                if vaccination_form.is_valid():
                    vaccination = vaccination_form.save(commit=False)
                    vaccination.cattle = cattle
                    vaccination.status = True  # Set vaccination status as True
                    vaccination.save()

            if 'insurance_checkbox' in request.POST:
                if insurance_form.is_valid():
                    insurance = insurance_form.save(commit=False)
                    insurance.cattle = cattle
                    insurance.status = True  # Set insurance status as True
                    insurance.save()

            return redirect('view_cattle')
    else:
        cattle_form = CattleForm()
        vaccination_form = VaccinationForm()
        insurance_form = InsuranceForm()

    return render(request, 'cattle/add_cattle.html', {
        'cattle_form': cattle_form,
        'vaccination_form': vaccination_form,
        'insurance_form': insurance_form,
    })

@login_required
def view_cattle(request):
    user_cattle = Cattle.objects.filter(seller=request.user.seller)
    paginator = Paginator(user_cattle, 5)  # Show 5 cattle per page
    page_number = request.GET.get('page')
    user_cattle = paginator.get_page(page_number)
    return render(request, 'cattle/view_cattle.html', {'user_cattle': user_cattle})
    
@login_required
def edit_cattle(request, cattle_id):
    cattle = get_object_or_404(Cattle, pk=cattle_id)
    if request.method == 'POST':
        cattle_form = CattleForm(request.POST, request.FILES, instance=cattle)
        if cattle_form.is_valid():
            cattle = cattle_form.save()
            return redirect('view_cattle')
    else:
        cattle_form = CattleForm(instance=cattle)
    return render(request, 'cattle/edit_cattle.html', {'cattle_form': cattle_form})

@login_required
def delete_cattle(request, cattle_id):
    cattle = get_object_or_404(Cattle, pk=cattle_id)
    if request.method == 'POST':
        cattle.delete()
        return redirect('view_cattle')
    return render(request, 'cattle/delete_cattle.html', {'cattle': cattle})
@login_required
def vaccination(request, cattle_id):
    cattle = get_object_or_404(Cattle, pk=cattle_id)

    if request.method == 'POST':
        vaccination_form = VaccinationForm(request.POST)
        if vaccination_form.is_valid():
            vaccination = vaccination_form.save(commit=False)
            vaccination.cattle = cattle
            vaccination.save()
            return redirect('add_cattle')  # Redirect to success page after successful submission
    else:
        vaccination_form = VaccinationForm()

    context = {
        'vaccination_form': vaccination_form,
        'cattle_id': cattle_id,
    }
    return render(request, 'cattle/vaccination.html', context)
@login_required
def insurance(request, cattle_id):
    cattle = get_object_or_404(Cattle, pk=cattle_id)

    if request.method == 'POST':
        insurance_form = InsuranceForm(request.POST)
        if insurance_form.is_valid():
            insurance = insurance_form.save(commit=False)
            insurance.cattle = cattle
            insurance.save()
            return redirect('add_cattle')  # Redirect to success page after successful submission
    else:
        insurance_form = InsuranceForm()

    context = {
        'insurance_form': insurance_form,
        'cattle_id': cattle_id,
    }
    return render(request, 'cattle/insurance.html', context)
@login_required
def vac_details(request, cattle_id):
    cattle = get_object_or_404(Cattle, pk=cattle_id)
    vaccination = Vaccination.objects.filter(cattle=cattle).first()  # Fetch the vaccination entry for the cattle if it exists
    return render(request, 'cattle/vac_details.html', {'cattle': cattle, 'vaccination': vaccination})

@login_required
def ins_details(request, cattle_id):
    cattle = get_object_or_404(Cattle, pk=cattle_id)
    insurance = Insurance.objects.filter(cattle=cattle).first()  # Fetch the insurance entry for the cattle if it exists
    return render(request, 'cattle/ins_details.html', {'cattle': cattle, 'insurance': insurance})
@login_required
def add_breed(request):
    if request.method == 'POST':
        form = BreedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_breed')  # Redirect to view breed page
    else:
        form = BreedForm()
    
    return render(request, 'cattle/add_breed.html', {'form': form})
def view_breed(request):
    breeds = Breed.objects.all()
    return render(request, 'cattle/view_breed.html', {'breeds': breeds})

def delete_breed(request, breed_id):
    breed = get_object_or_404(Breed, pk=breed_id)
    if request.method == 'POST':
        breed.delete()
        return redirect('view_breed')  # Redirect to view breed page
    
    return render(request, 'cattle/delete_breed.html', {'breed': breed})
def fetch_breeds(request):
    cattle_type = request.GET.get('cattleType')
    # Query breeds based on cattle_type
    breeds = Breed.objects.filter(cattle_type__name=cattle_type).values_list('name', flat=True)
    return JsonResponse({'breeds': list(breeds)})