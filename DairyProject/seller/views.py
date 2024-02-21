from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DeliveryBoyRegistrationForm
from .models import DeliveryBoy, DeliveryBoyEdit
from farm.models import CustomUser, Login_Details

def delivery_register(request):
    if request.method == 'POST':
        form = DeliveryBoyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            driving_license = form.cleaned_data['driving_license']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirmpassword']

            if DeliveryBoy.objects.filter(driving_license=driving_license).exists():
                messages.error(request, "Delivery boy with this driving license already exists. Please use a different license.")
            elif DeliveryBoy.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            elif password != confirm_password:
                messages.error(request, "Passwords do not match")
            else:
                user = CustomUser.objects.create_user(email=email, password=password, role='Delivery Boy')
                delivery_boy = DeliveryBoy(user=user, name=name, driving_license=driving_license, mobile=mobile)
                delivery_boy.save()

                delivery_edit_profile = DeliveryBoyEdit(
                    user=user,
                    delivery_boy=delivery_boy,
                    name=name,
                    mobile=mobile,
                    email=email,
                    driving_license=driving_license
                )
                delivery_edit_profile.save()

                login = Login_Details(email=email, password=password, role='Delivery Boy')
                login.save()

                messages.success(request, 'Registration successful. Please check your email to confirm.')
                return redirect("login")  # Update to the correct URL name for login page
    else:
        form = DeliveryBoyRegistrationForm()

    return render(request, 'delivery_register.html', {'form': form})  # Update to the correct template file name

def delivery_dashboard(request):
               response = render(request, 'dash/delivery_dashboard.html')
           

def delivery_boys(request):
    delivery_boys = DeliveryBoy.objects.all()
    return render(request, 'admin/delivery_boys.html', {'delivery_boys': delivery_boys})