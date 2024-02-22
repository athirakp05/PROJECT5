from collections import OrderedDict
from random import random
import string
import stringprep
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect,HttpResponse
from product.models import Product
from .models import  CustomUser, Customer, Seller,CattleType
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q  # Import the Q object
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from .forms import  CustomerEditProfileForm, SellerEditProfileForm, SellerPasswordChangeForm
from .models import Cattle,Login_Details,SellerEditProfile,Breed,Insurance,Vaccination,ContactMessage,CustomerEditProfile,VetEditProfile,Veterinarian
from .forms import CattleForm, VaccinationForm, InsuranceForm,SellerProfileForm,BreedForm,ContactForm,VetEditProfileForm
from django.shortcuts import render, redirect, get_object_or_404  # Import get_object_or_404
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
from seller.models import DeliveryBoy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SellerPasswordChangeForm

def index(request):
    return render(request, 'index.html')

def loginn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:  # Check if the user is active
                auth_login(request, user)
                request.session['email'] = email

                if user.role == 'Admin':
                    messages.success(request, "Login successful!")
                    return redirect("admindash")  # Redirect to the admin dashboard
                elif user.role == 'Customer':
                    if user.customer.is_active:
                        messages.success(request, "Login successful!")
                        return redirect("c_dashboard")  # Redirect to the customer dashboard
                    else:
                        messages.warning(request, "Your account has been disabled. Please contact the administrator.")
                        return render(request, 'login.html')  # Render login page with a message

                elif user.role == 'Seller':
                    if user.seller.is_active:
                        messages.success(request, "Login successful!")
                        return redirect("s_dashboard")  # Redirect to the seller dashboard
                    else:
                        messages.warning(request, "Your account has been disabled. Please contact the administrator.")
                        return render(request, 'login.html')  # Render login page with a message
                elif user.role == 'Veterinarian':
                    if user.veterinarian.is_active:
                        messages.success(request, "Login successful!")
                        return redirect("v_dashboard") 
                elif user.role == 'DeliveryBoy':
                    if user.DeliveryBoy.is_active:
                        messages.success(request, "Login successful!")
                        return redirect("deliveryboy_dashboard") 
                    else:
                        messages.warning(request, "Your account has been disabled. Please contact the administrator.")
                        return render(request, 'login.html')  # Render login page with a message
                else:
                    # Handle unknown or unsupported roles here
                    messages.error(request, "Unknown user role or unsupported role.")
            else:
                messages.warning(request, "Your account has been disabled. Please contact the administrator.")
                return render(request, 'login.html')  # Render login page with a message
        else:
            messages.error(request, "Login failed. Please check your credentials.")
    return render(request, 'login.html')

@login_required
def pending_sellers(request):
    pending_sellers = Seller.objects.filter(is_approved=False)
    return render(request, 'admin/pending_sellers.html', {'pending_sellers': pending_sellers})

@login_required
def approve_seller(request, email):
    user = get_object_or_404(CustomUser, email=email)
    seller = Seller.objects.get(user=user)
    seller.is_approved = True
    seller.save()
    # Redirect to a success page or a relevant view
    return redirect('pending_sellers')
@login_required
def reject_seller(request, email):
    user = get_object_or_404(CustomUser, email=email)
    seller = Seller.objects.get(user=user)
    seller.delete()  
    return redirect('pending_sellers')

@login_required
def activate_customer(request, email):
    customer = get_object_or_404(CustomUser, email=email)
    customer.is_active = True
    customer.save()
    return redirect('c_view')  # Redirect to the customer view page

@login_required
def deactivate_customer(request, email):
    customer = get_object_or_404(CustomUser, email=email)
    customer.is_active = False
    customer.save()
    return redirect('c_view')  # Redirect to the customer view page

def activate_seller(request, email):
    seller = CustomUser.objects.get(email=email)
    seller.is_active = True
    seller.save()
    return redirect('s_view')  # Redirect to login page

def deactivate_seller(request, email):
    seller = CustomUser.objects.get(email=email)
    seller.is_active = False
    seller.save()
    return redirect('s_view')  # Redirect to login page


def c_register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user =CustomUser.objects.create_user(email=email, password=password, role='Customer')
            customer = Customer(user=user, first_name=firstname, last_name=lastname, mobile=mobile)
            customer.save()
            customer_edit_profile = CustomerEditProfile(user=user, customer=customer, first_name=firstname, last_name=lastname, mobile=mobile, email=email)
            customer_edit_profile.save()
            login = Login_Details(email=email, password=password, role='Customer')
            login.save()
            messages.success(request, "Registered successfully")
            return redirect("login") 
    return render(request, 'c_register.html')

def s_register(request):
    if request.method == "POST":
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
            login = Login_Details(email=email, password=password, role='Seller')
            login.save()
            messages.success(request, "Registered pending approval")
            return redirect("login") 
    return render(request, 's_register.html')

@login_required
def s_profile(request):
    user = request.user
    if user.is_seller:
        seller_profile = SellerEditProfile.objects.get(user=user)
        return render(request, 'profile_edit/s_profile.html', {'seller_profile': seller_profile})
    else:
        return redirect('home') 

@login_required
def complete_s_profile(request):
    user = request.user
    seller_profile, created = SellerEditProfile.objects.get_or_create(user=user.seller.user)
    if request.method == 'POST':
        form = SellerEditProfileForm(request.POST, request.FILES, instance=seller_profile)
        if form.is_valid():
            form.save()
            return redirect('seller_profile')  
    else:
        form = SellerEditProfileForm(instance=seller_profile)
    return render(request, 'profile_edit/complete_s_profile.html', {'form': form})

@login_required
def complete_c_profile(request):
    user = request.user
    customer_profile, created =CustomerEditProfile.objects.get_or_create(user=user.customer.user)
    if request.method == 'POST':
        form = CustomerEditProfileForm(request.POST, request.FILES, instance=customer_profile)
        if form.is_valid():
            form.save()
            return redirect('customer_profile')  
    else:
        form = CustomerEditProfileForm(instance=customer_profile)
    return render(request, 'profile_edit/complete_c_profile.html', {'form': form})

def seller_profile(request):
    seller_profile = SellerEditProfile.objects.get(user=request.user.seller.user)
    return render(request, 'profile_edit/seller_profile.html', {'seller_profile': seller_profile})
def customer_profile(request):
    customer_profile = CustomerEditProfile.objects.get(user=request.user.customer.user)
    return render(request, 'profile_edit/customer_profile.html', {'customer_profile': customer_profile})
def v_register(request):
    if request.method == "POST":
        doctor_name = request.POST.get('doctor_name')
        doctor_license = request.POST.get('doctor_license')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        start_year = request.POST.get('start_year')
        specialization = request.POST.get('specialization')  # Add this line

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif Veterinarian.objects.filter(doctor_license=doctor_license).exists():  # Update this line
            messages.error(request, "Veterinarian with this license already exists. Please use a different license.")
            return redirect("v_register")

        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user = CustomUser.objects.create_user(email=email, password=password, role='Veterinarian')
            veterinarian = Veterinarian(user=user,doctor_name=doctor_name,doctor_license=doctor_license,email=email,mobile=mobile,start_year=start_year, specialization=specialization)
            veterinarian.save()
            vet_edit_profile = VetEditProfile(user=user, veterinarian=veterinarian,doctor_name=doctor_name,doctor_license=doctor_license,email=email,mobile=mobile,start_year=start_year, specialization=specialization)
            vet_edit_profile.save()
            login_details = Login_Details(email=email, password=password, role='Veterinarian')
            login_details.save()
            messages.success(request, "Registered successfully. Pending approval.")
            return redirect("login")

    return render(request, 'v_register.html')


@login_required
def vet_profile(request):
    user = request.user
    if user.is_veterinarian:
        vet_profile = VetEditProfile.objects.get(user=request.user)
        return render(request, 'view/vet_profile.html', {'vet_profile': vet_profile})
    else:
        return redirect('v_dashboard')

@login_required
def complete_v_profile(request):
    user = request.user
    veterinarian = Veterinarian.objects.get(user=request.user)
    vet_profile, created = VetEditProfile.objects.get_or_create(user=user.veterinarian.user)

    # Fetch the start year from the Veterinarian table
    start_year = veterinarian.start_year

    # Pass the start_year as initial data to the form
    form = VetEditProfileForm(initial={'start_year': start_year})

    if request.method == 'POST':
        form = VetEditProfileForm(request.POST, request.FILES, instance=vet_profile)
        if form.is_valid():
            form.save()
            return redirect('vet_profile')
    else:
        form = VetEditProfileForm(instance=vet_profile)

    return render(request, 'profile_edit/complete_v_profile.html', {'form': form})


def logout_user(request):
    auth_logout(request)
    return redirect('home')

def admindash(request):
    if 'email' in request.session:
        response = render(request, 'dash/admindash.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('home')
def v_dashboard(request):
    if 'email' in request.session:
        response = render(request, 'dash/v_dashboard.html')
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
    
def s_view(request):
    sellers_list = SellerEditProfile.objects.all()
    paginator = Paginator(sellers_list, 10)  # Show 10 sellers per page
    page_number = request.GET.get('page')
    sellers = paginator.get_page(page_number)
    return render(request, 'view/s_view.html', {'sellers': sellers})

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
    
def search_sellers(request):
    query = request.GET.get('query')
    sellers = Seller.objects.all()
    if query:
        sellers = sellers.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    context = {'sellers': sellers, 'query': query}
    return render(request, 'other/team.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.name = request.user.get_full_name()
            contact_message.email = request.user.email
            contact_message.save()
            # Add success message and redirect if needed
            return redirect('success')  # Redirect to a success page
    else:
        initial_data = {'name': request.user.get_full_name(), 'email': request.user.email} if request.user.is_authenticated else {}
        form = ContactForm(initial=initial_data)

    return render(request, 'contact.html', {'form': form})

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

def admin_view_cattle(request):
    cattle_list = Cattle.objects.all()
    paginator = Paginator(cattle_list, 10)  # Show 10 cattle per page
    page_number = request.GET.get('page')
    cattle = paginator.get_page(page_number)
    return render(request, 'admin/admin_view_cattle.html', {'cattle': cattle})

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
    breed = get_object_or_404(Breed, id=breed_id)
    if request.method == 'POST':
        breed.delete()
        return redirect('view_breed')  # Redirect to view breed page
    
def fetch_breeds(request):
    cattle_type = request.GET.get('cattleType')
    breeds = Breed.objects.filter(cattle_type=cattle_type).values_list('name', flat=True)
    return JsonResponse({'breeds': list(breeds)})

def usercount(request):
    customer_count = Customer.objects.count()
    seller_count = Seller.objects.count()
    product_count = Product.objects.count()
    veterinarian_count = Veterinarian.objects.count()
    delivery_boy_count = DeliveryBoy.objects.count()

    data = {
        'customer_count': customer_count,
        'seller_count': seller_count,
        'product_count': product_count,
        'veterinarian_count': veterinarian_count,
        'delivery_boy_count': delivery_boy_count,
    }
    return render(request, 'view/usercount.html', data)

def team(request):
    sellers = SellerEditProfile.objects.all()
    return render(request, 'other/team.html', {'sellers': sellers})

def society_seller_count(request):
    sellers = SellerEditProfile.objects.all()
    society_count = {}
    for seller in sellers:
        society = seller.society
        if society in society_count:
            society_count[society] += 1
        else:
            society_count[society] = 1

    societies = list(society_count.keys())
    seller_counts = list(society_count.values())
    print("Societies:", societies)
    print("Seller Counts:", seller_counts)
    try:
        plt.figure(figsize=(8, 6))
        plt.bar(societies, seller_counts, color='skyblue')
        plt.xlabel('Society')
        plt.ylabel('Number of Sellers')
        plt.title('Number of Sellers in Each Society')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plot_path = 'path/to/save/plot.png'
        plt.savefig(plot_path)
        return render(request, 'other/society_seller_count.html', {'plot_path': plot_path})
    except Exception as e:
        print("Error:", e)  # Print the exact error message for further debugging
        return HttpResponse("Error occurred during plotting.")
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def message(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin/message.html', {'messages': messages})

def get_new_messages(request):
    new_messages = ContactMessage.objects.filter(is_read=False)  # Adjust this filter based on your logic
    serialized_messages = [
        {
            'name': message.name,
            'email': message.email,
            'subject': message.subject,
            'message': message.message,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in new_messages
    ]
    new_messages.update(is_read=True)
    return JsonResponse({'messages': serialized_messages})


class s_change_password(PasswordChangeView):
    form_class = SellerPasswordChangeForm
    template_name = 'profile_edit/s_change_password.html'  # Path to your change password template
    success_url = reverse_lazy('login')  # Replace with your success URL
    def form_valid(self, form):
        seller_profile = form.save()
        login_details = seller_profile.login_details
        login_details.password = seller_profile.password
        login_details.save()
        seller = seller_profile.seller
        seller.password = seller_profile.password
        seller.save()
        update_session_auth_hash(self.request, seller_profile)
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)
    
def veterinarians(request):
    veterinarians = Veterinarian.objects.all()
    paginator = Paginator(veterinarians, 10)  # Show 10 veterinarians per page
    page_number = request.GET.get('page')
    veterinarians = paginator.get_page(page_number)
    return render(request, 'admin/veterinarians.html', {'veterinarians': veterinarians})

