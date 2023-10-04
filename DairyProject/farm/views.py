from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import CustomUser

def index(request):
    return render(request, 'index.html')

def loginn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('c_dash')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already used!")
        else:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role='CUSTOMER'
            )
            messages.success(request, "Registered successfully")
            return redirect('login')

    return render(request, 'registration.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def c_dash(request):
    return render(request, 'c_dash.html')

def s_dash(request):
    return render(request, 's_dash.html')
