from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from social_django.utils import psa
from .models import CustomUser

def index(request):
    return render(request, 'index.html')

@psa('social:begin', 'social:complete')
def custom_login(request, backend):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')

@psa('social:complete')
def custom_complete(request, backend, *args, **kwargs):
    user = kwargs['user']
    if user:
        login(request, user)
        return redirect('home')
    else:
        # Handle the case when the user was not authenticated
        return redirect('login')

def loginn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            request.session['email'] = email
            messages.success(request, "Login successful!")
            return redirect("c_dashboard") 
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
            user = CustomUser.objects.create_user(email=email, password=password, role='CUSTOMER', phone=phone)
            user.set_password(password)
            user.save()
            messages.success(request, "Registered successfully")
            return redirect("login")
    return render(request, 'registration.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def c_dashboard(request):
    response = render(request, 'c_dashboard.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response
