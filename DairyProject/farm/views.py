from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Customer, Seller, SellerEdit
from .forms import SellerForm, CustomerRegistrationForm
import secrets
import string
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.contrib.auth.hashers import make_password  # Import make_password



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
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered.')
                return render(request, 'registration.html', {'form': form})

            user = get_user_model().objects.create_user(
                email=email,
                password=form.cleaned_data['password']
            )

            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            phone = form.cleaned_data['phone']
            customer = Customer(user=user, firstname=firstname, lastname=lastname, email=email, phone=phone)
            customer.save()

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        form = CustomerRegistrationForm()

    return render(request, 'registration.html', {'form': form})
def add_seller(request):
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            
            # Set the role attribute to "seller"
            seller.role = "seller"
            
            # Generate a random password
            temporary_password = generate_random_password()
            
            # Set the password
            seller.set_password(temporary_password)
            
            # Save the seller
            seller.save()

            return render(request, 'seller_password.html', {'temporary_password': temporary_password})
    else:
        form = SellerForm()

    return render(request, 'add_seller.html', {'form': form})

def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

def admin_logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

def c_dashboard(request):
    if 'email' in request.session:
        return render(request, 'c_dashboard.html')
    else:
        return redirect('index')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def s_dashboard(request):
    return render(request, 's_dashboard.html')

def view_sellers(request):
    sellers = Seller.objects.all()
    return render(request, 'view_sellers.html', {'sellers': sellers})
class SellerListView(ListView):
    model = Seller
    template_name = 'seller_list.html'
    context_object_name = 'sellers'  

def view_customers(request):
    customers = Customer.objects.all()
    return render(request, 'view_customers.html', {'customers': customers})
    
class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers' 

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

def seller_list(request):
    sellers = Seller.objects.all()
    return render(request, 'seller_list.html', {'sellers': sellers})

def seller_login_details(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    return render(request, 'seller_login_details.html', {'seller': seller})

def generate_random_password():
    password_length = 6
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(password_length))
    return password
