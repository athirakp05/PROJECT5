from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser, Customer, Seller, SellerEdit
from .forms import SellerForm, CustomerEdit, SellerEditForm
from django.views.generic import ListView


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
            # Create a new CustomUser
            user = CustomUser.objects.create_user(email=email, password=password, role='Customer', phone=phone)
            user.is_customer = True
            user.save()

            # Create a new Customer linked to the user
            customer = Customer(user=user, firstname=firstname, lastname=lastname, phone=phone)
            customer.save()

            messages.success(request, "Registered successfully")
            return redirect("login")
    return render(request, 'registration.html')

def add_seller(request):
    if request.method == "POST":
        form = SellerForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)  # Create the seller instance, but don't save it to the database yet
            # You can perform additional processing here if needed
            seller.save()  # Save the seller to the database
            messages.success(request, "Seller added successfully")
            return redirect("seller_list")  # Redirect to a login or dashboard page
        else:
            messages.error(request, "Seller registration failed. Please check the form data.")

    else:
        form = SellerForm()

    return render(request, 'add_seller.html', {'form': form})

def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")  # Add a logout message
    return redirect('login')
def admin_logout(request):
    auth_logout(request)  # Log the user out
    messages.info(request, "You have been logged out.")  # Add a logout message
    return redirect('login')  # Redirect to your login page

#@login_required
def c_dashboard(request):
    if 'email' in request.session:
        return render(request, 'c_dashboard.html')
    else:
        return redirect('index')

#@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

#@login_required
def s_dashboard(request):
    return render(request, 's_dashboard.html')

#@login_required
def view_sellers(request):
    sellers = Seller.objects.all()
    return render(request, 'view_sellers.html', {'sellers': sellers})

#@login_required
def view_customers(request):
    customers = Customer.objects.all()
    return render(request, 'view_customers.html', {'customers': customers})

#@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

#@login_required
def seller_list(request):
    sellers = Seller.objects.all()
    return render(request, 'seller_list.html', {'sellers': sellers})

#@login_required
def seller_login_details(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    # You can retrieve and display seller's login details here
    return render(request, 'seller_login_details.html', {'seller': seller})
    
class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'
    from django.views.generic import ListView
from .models import Seller  # Import the Seller model from your models.py

class SellerListView(ListView):
    model = Seller
    template_name = 'seller_list.html'  # Create an HTML template for displaying seller details
    context_object_name = 'sellers'  # The variable name to use in the template



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


def edit_customer(request):
    customer = request.user.customer  # Assuming you have a Customer model with a user field linking to CustomUser
    if request.method == 'POST':
        form = CustomerEdit(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            # Redirect to a success page or the customer dashboard
            return redirect('c_dashboard')
    else:
        form = CustomerEdit(instance=customer)

    return render(request, 'edit_customer.html', {'form': form})
def c_delete(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        # You can add additional logic here if needed before deleting the customer
        customer.delete()
        return redirect('customer_list')  # Replace 'customer_list' with the URL name of the customer list view

    return render(request, 'c_delete.html', {'customer': customer})


def edit_seller(request, seller_id):
    seller = get_object_or_404(SellerEdit, id=seller_id)

    if request.method == "POST":
        form = SellerEditForm(request.POST, request.FILES, instance=seller)
        if form.is_valid():
            form.save()
            return redirect("view_sellers")  # You can redirect to the seller list page or another URL
    else:
        form = SellerEditForm(instance=seller)

    return render(request, 'edit_seller.html', {'form': form, 'seller': seller})
