from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth import logout as auth_logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from django.http import JsonResponse
from django.urls import reverse

# from .helpers import send_forget_password_mail
# from .forms import PatientProfileForm

# Create your views here.
def index(request):
    return render(request,'index.html')


def loginn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            request.session['email'] = email
            messages.success(request, "Login successful!")
            return redirect("c_dashboard")  # Replace 'phome' with the name of your home page URL
        else:
            messages.error(request, "Invalid login credentials")

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response
def registration(request):
    if request.method == "POST":
        firstname=request.POST.get('firstname') 
        lastname = request.POST.get('lastname')
        username=request.POST.get('username')
        email = request.POST.get('email')
        phone=request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
    
        if (CustomUser.objects.filter(email=email).exists()):
            messages.error(request, "Email already exists")
            return render(request,'login.html')
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request,'login.html')

        else:
            user = CustomUser.objects.create_user(first_name=firstname,last_name=lastname,email=email,phone=phone,username=username,role='CUSTOMER')  # Change role as needed
            user.set_password(password)
            user.save()
            messages.success(request, "Registered successfully")
            return redirect("login")
    return render(request,'registration.html')

def logout(request):
    auth_logout(request) # Use the logout function to log the user out
    return redirect('home')  # Redirect to the confirmation page

def c_dashboard(request):
   if 'email' in request.session:
       response = render(request, 'c_dashboard.html')
       response['Cache-Control'] = 'no-store, must-revalidate'
       return response
   else:
       return redirect('home')