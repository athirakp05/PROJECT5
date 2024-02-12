from pyexpat.errors import messages
from django.shortcuts import redirect, render
from farm.views import message
from farm.models import CustomUser, Login_Details
from .models import DeliveryBoy



def deliveryboy_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if CustomUser.objects.filter(email=email).exists():
            message.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user = CustomUser.objects.create_user(email=email, password=password, role='DeliveryBoy')
            deliveryboy = DeliveryBoy(user=user, name=name, mobile=mobile, email=email)
            deliveryboy.save()
            login_details = Login_Details(email=email, password=password, role='DeliveryBoy')
            login_details.save()
            messages.success(request, "Registered successfully")
            return redirect("login")
    return render(request, 'deliveryboy_register.html')