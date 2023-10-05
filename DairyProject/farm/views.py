from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth import logout as auth_logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
# from .helpers import send_forget_password_mail
# from .forms import PatientProfileForm

# Create your views here.
def index(request):
    return render(request,'index.html')

# # @login_required
# def userpage(request):
#     if 'username' in request.session:
#         response = render(request, 'userpage.html')
#         response['Cache-Control'] = 'no-store, must-revalidate'
#         return response
#     else:
#         return redirect('login')
def loginn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            request.session['username']=username
            return redirect('userpage')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    response = render(request,'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response

    # return render(request,'login.html')
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
    try:
        del request.session['username']
    except:
        return redirect('login')
    return redirect('login')
def c_dashboard(request):
    return render(request,'c_dashboard.html')
def s_dashboard(request):
    return render(request,'c_dashboard.html')